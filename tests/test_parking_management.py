import os
import time
import pytest
import httpx

def _load_env_file():
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    if k.strip() not in os.environ:
                        os.environ[k.strip()] = v.strip()

_load_env_file()

XANO_API_BASE = os.getenv("XANO_API_BASE", "https://x8ki-letl-twmt.n7.xano.io")
XANO_AUTH_URL = f"{XANO_API_BASE}/api:o7T2IhYl"
XANO_PARKING_URL = f"{XANO_API_BASE}/api:parking"

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "pytest_admin_estacionamento@example.com")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "AdminPassword123")
CLIENT_EMAIL = os.getenv("CLIENT_EMAIL", "pytest_client_estacionamento@example.com")
CLIENT_PASSWORD = os.getenv("CLIENT_PASSWORD", "ClientPassword123")

@pytest.fixture(scope="session")
def admin_token():
    with httpx.Client(timeout=30.0) as client:
        time.sleep(4)
        client.post(
            f"{XANO_AUTH_URL}/auth/signup",
            json={"name": "Admin Test", "email": ADMIN_EMAIL, "password": ADMIN_PASSWORD, "role": "admin"}
        )
        time.sleep(4)
        resp = client.post(f"{XANO_AUTH_URL}/auth/login", json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD})
        assert resp.status_code == 200, f"Admin login failed: {resp.text}"
        data = resp.json()
        token = data.get("authToken")
        assert token, "Admin auth token not returned"
        return token

@pytest.fixture(scope="session")
def client_token():
    with httpx.Client(timeout=30.0) as client:
        time.sleep(4)
        client.post(
            f"{XANO_AUTH_URL}/auth/signup",
            json={"name": "Client Test", "email": CLIENT_EMAIL, "password": CLIENT_PASSWORD, "role": "cliente"}
        )
        time.sleep(4)
        resp = client.post(f"{XANO_AUTH_URL}/auth/login", json={"email": CLIENT_EMAIL, "password": CLIENT_PASSWORD})
        assert resp.status_code == 200, f"Client login failed: {resp.text}"
        data = resp.json()
        token = data.get("authToken")
        assert token, "Client auth token not returned"
        return token

def test_parking_management_workflow(admin_token, client_token):
    with httpx.Client(timeout=30.0) as client:
        admin_headers = {"Authorization": f"Bearer {admin_token}"}
        client_headers = {"Authorization": f"Bearer {client_token}"}

        vaga_numero = "TESTE-VAGA-01"
        vaga_tipo = "carro"
        vaga_tipo_edit = "moto"
        vaga_numero_edit = "TESTE-VAGA-01-ED"

        tarifa_tipo = "carro"
        tarifa_valor = 15.50
        tarifa_valor_edit = 20.00

        vaga_id = None
        tarifa_id = None
        loc_id = None

        try:
            time.sleep(4)
            # Cleanup any leftover test data first
            list_resp = client.get(f"{XANO_PARKING_URL}/vaga", headers=admin_headers)
            if list_resp.status_code == 200:
                for v in list_resp.json():
                    if v.get("numero", "").startswith("TESTE-"):
                        time.sleep(4)
                        client.delete(f"{XANO_PARKING_URL}/vaga/{v['id']}", headers=admin_headers)

            time.sleep(4)
            list_t_resp = client.get(f"{XANO_PARKING_URL}/tarifa", headers=admin_headers)
            if list_t_resp.status_code == 200:
                for t in list_t_resp.json():
                    if t.get("tipo_vaga") == tarifa_tipo:
                        time.sleep(4)
                        client.delete(f"{XANO_PARKING_URL}/tarifa/{t['id']}", headers=admin_headers)

            time.sleep(4)
            # Create a test location first with unique name
            loc_name = f"Test Unit Central {int(time.time() * 1000)}"
            loc_resp = client.post(
                f"{XANO_PARKING_URL}/location",
                headers=admin_headers,
                json={"name": loc_name, "address": "Rua A", "description": "Central"}
            )
            if loc_resp.status_code == 200:
                loc_id = loc_resp.json().get("id")
            else:
                pytest.fail(f"Failed to create test location: {loc_resp.status_code} - {loc_resp.text}")

            time.sleep(4)
            # Test location update success (PUT /location/{id})
            loc_edit_resp = client.put(
                f"{XANO_PARKING_URL}/location/{loc_id}",
                headers=admin_headers,
                json={"id": loc_id, "name": f"{loc_name} Updated", "address": "Rua A Updated", "description": "Central Updated"}
            )
            assert loc_edit_resp.status_code == 200, f"Edit location failed: {loc_edit_resp.text}"

            time.sleep(4)
            # 1. Admin creates vaga success
            resp = client.post(
                f"{XANO_PARKING_URL}/vaga",
                headers=admin_headers,
                json={"location_id": loc_id, "numero": vaga_numero, "tipo": vaga_tipo}
            )
            assert resp.status_code == 200, f"Create vaga failed: {resp.text}"
            vaga_data = resp.json()
            vaga_id = vaga_data["id"]

            time.sleep(4)
            # 2. Duplicate vaga numero rejection (inputerror)
            resp = client.post(
                f"{XANO_PARKING_URL}/vaga",
                headers=admin_headers,
                json={"location_id": loc_id, "numero": vaga_numero, "tipo": vaga_tipo}
            )
            assert resp.status_code == 400
            err_data = resp.json()
            assert "inputerror" in err_data.get("code", "").lower() or err_data.get("error_type") == "inputerror" or "existe" in err_data.get("message", "").lower()

            time.sleep(4)
            # 3. Client mutation access denied on vaga create
            resp = client.post(
                f"{XANO_PARKING_URL}/vaga",
                headers=client_headers,
                json={"location_id": loc_id, "numero": "TESTE-VAGA-CLIENT", "tipo": vaga_tipo}
            )
            assert resp.status_code in [401, 403]

            time.sleep(4)
            # 4. Admin edits vaga success
            resp = client.put(
                f"{XANO_PARKING_URL}/vaga/{vaga_id}",
                headers=admin_headers,
                json={"id": vaga_id, "location_id": loc_id, "numero": vaga_numero_edit, "tipo": vaga_tipo_edit, "status": "livre"}
            )
            assert resp.status_code == 200, f"Edit vaga failed: {resp.text}"

            time.sleep(4)
            # 5. Client listing with location_id success (GET)
            resp = client.get(f"{XANO_PARKING_URL}/vaga", params={"location_id": loc_id}, headers=client_headers)
            assert resp.status_code == 200

            time.sleep(4)
            # 6. Admin creates tarifa success (tipo_vaga: carro)
            resp = client.post(
                f"{XANO_PARKING_URL}/tarifa",
                headers=admin_headers,
                json={"location_id": loc_id, "tipo_vaga": tarifa_tipo, "valor_hora": tarifa_valor}
            )
            if resp.status_code == 400:
                time.sleep(4)
                t_list = client.get(f"{XANO_PARKING_URL}/tarifa", params={"location_id": loc_id}, headers=admin_headers).json()
                for t in t_list:
                    if t.get("tipo_vaga") == tarifa_tipo:
                        time.sleep(4)
                        client.delete(f"{XANO_PARKING_URL}/tarifa/{t['id']}", headers=admin_headers)
                time.sleep(4)
                resp = client.post(
                    f"{XANO_PARKING_URL}/tarifa",
                    headers=admin_headers,
                    json={"location_id": loc_id, "tipo_vaga": tarifa_tipo, "valor_hora": tarifa_valor}
                )
            assert resp.status_code == 200, f"Create tarifa failed: {resp.text}"
            tarifa_data = resp.json()
            tarifa_id = tarifa_data["id"]

            time.sleep(4)
            # 7. Duplicate tarifa tipo_vaga rejection (inputerror)
            resp = client.post(
                f"{XANO_PARKING_URL}/tarifa",
                headers=admin_headers,
                json={"location_id": loc_id, "tipo_vaga": tarifa_tipo, "valor_hora": tarifa_valor}
            )
            assert resp.status_code == 400
            err_data = resp.json()
            assert "inputerror" in err_data.get("code", "").lower() or err_data.get("error_type") == "inputerror" or "existe" in err_data.get("message", "").lower()

            time.sleep(4)
            # 8. Admin edits tarifa success
            resp = client.put(
                f"{XANO_PARKING_URL}/tarifa/{tarifa_id}",
                headers=admin_headers,
                json={"id": tarifa_id, "location_id": loc_id, "tipo_vaga": tarifa_tipo, "valor_hora": tarifa_valor_edit}
            )
            assert resp.status_code == 200, f"Edit tarifa failed: {resp.text}"

            time.sleep(4)
            # 9. Client mutation access denied on tarifa edit
            resp = client.put(
                f"{XANO_PARKING_URL}/tarifa/{tarifa_id}",
                headers=client_headers,
                json={"id": tarifa_id, "location_id": loc_id, "tipo_vaga": tarifa_tipo, "valor_hora": 30.00}
            )
            assert resp.status_code in [401, 403]

        finally:
            if vaga_id:
                try:
                    time.sleep(2)
                    client.delete(f"{XANO_PARKING_URL}/vaga/{vaga_id}", headers=admin_headers)
                except Exception:
                    pass
            if tarifa_id:
                try:
                    time.sleep(2)
                    client.delete(f"{XANO_PARKING_URL}/tarifa/{tarifa_id}", headers=admin_headers)
                except Exception:
                    pass
            if loc_id:
                try:
                    time.sleep(2)
                    client.delete(f"{XANO_PARKING_URL}/location/{loc_id}", headers=admin_headers)
                except Exception:
                    pass


def test_multi_location_workflow(admin_token, client_token):
    with httpx.Client(timeout=30.0) as client:
        admin_headers = {"Authorization": f"Bearer {admin_token}"}
        client_headers = {"Authorization": f"Bearer {client_token}"}

        loc1_id = None
        loc2_id = None
        vaga1_id = None
        vaga2_id = None
        tarifa1_id = None
        tarifa2_id = None

        try:
            time.sleep(4)
            # 1. Admin creates Location A and Location B with unique names
            ts = int(time.time() * 1000)
            resp1 = client.post(
                f"{XANO_PARKING_URL}/location",
                headers=admin_headers,
                json={"name": f"Loc A Test {ts}", "address": "Rua 1", "description": "Unidade A"}
            )
            if resp1.status_code == 200:
                loc1_id = resp1.json().get("id")
            else:
                pytest.fail(f"Failed to create Location A: {resp1.status_code} - {resp1.text}")

            time.sleep(4)
            resp2 = client.post(
                f"{XANO_PARKING_URL}/location",
                headers=admin_headers,
                json={"name": f"Loc B Test {ts}", "address": "Rua 2", "description": "Unidade B"}
            )
            if resp2.status_code == 200:
                loc2_id = resp2.json().get("id")
            else:
                pytest.fail(f"Failed to create Location B: {resp2.status_code} - {resp2.text}")

            time.sleep(4)
            # 2. Client lists locations successfully
            locs_resp = client.get(f"{XANO_PARKING_URL}/location", headers=client_headers)
            assert locs_resp.status_code == 200

            time.sleep(4)
            # 3. Client tries to create location -> 401/403
            fail_resp = client.post(
                f"{XANO_PARKING_URL}/location",
                headers=client_headers,
                json={"name": f"Client Loc {ts}", "address": "Rua C", "description": "Fail"}
            )
            assert fail_resp.status_code in [401, 403]

            time.sleep(4)
            # 4. Create vaga in Loc A and Loc B with same number
            v1_resp = client.post(
                f"{XANO_PARKING_URL}/vaga",
                headers=admin_headers,
                json={"location_id": loc1_id, "numero": "VAGA-DUPLICATE", "tipo": "carro"}
            )
            assert v1_resp.status_code == 200
            vaga1_id = v1_resp.json().get("id")

            time.sleep(4)
            # Try deleting location with linked vaga -> should reject (400)
            del_fail_resp = client.delete(f"{XANO_PARKING_URL}/location/{loc1_id}", headers=admin_headers)
            assert del_fail_resp.status_code == 400

            time.sleep(4)
            v2_resp = client.post(
                f"{XANO_PARKING_URL}/vaga",
                headers=admin_headers,
                json={"location_id": loc2_id, "numero": "VAGA-DUPLICATE", "tipo": "carro"}
            )
            assert v2_resp.status_code == 200, f"Same number in different location should succeed: {v2_resp.text}"
            vaga2_id = v2_resp.json().get("id")

            time.sleep(4)
            # 5. Isolation check: query vagas filtered by loc1_id should only return Loc A vaga
            filtered_resp = client.get(f"{XANO_PARKING_URL}/vaga", params={"location_id": loc1_id}, headers=client_headers)
            assert filtered_resp.status_code == 200
            vagas_loc1 = filtered_resp.json()
            assert len(vagas_loc1) > 0
            for v in vagas_loc1:
                assert v.get("location_id") == loc1_id
                assert v.get("id") != vaga2_id  # Ensure vaga from loc2 does not appear in loc1

            time.sleep(4)
            # 6. Tarifa multi-location test: same tipo_vaga in two different locations should succeed; duplicate in same location should return 400
            t1_resp = client.post(
                f"{XANO_PARKING_URL}/tarifa",
                headers=admin_headers,
                json={"location_id": loc1_id, "tipo_vaga": "carro", "valor_hora": 10.0}
            )
            assert t1_resp.status_code == 200
            tarifa1_id = t1_resp.json().get("id")

            time.sleep(4)
            t2_resp = client.post(
                f"{XANO_PARKING_URL}/tarifa",
                headers=admin_headers,
                json={"location_id": loc2_id, "tipo_vaga": "carro", "valor_hora": 15.0}
            )
            assert t2_resp.status_code == 200, f"Tarifa for same type in different location should succeed: {t2_resp.text}"
            tarifa2_id = t2_resp.json().get("id")

            time.sleep(4)
            # Duplicate in loc1 should fail (400)
            t_dup_resp = client.post(
                f"{XANO_PARKING_URL}/tarifa",
                headers=admin_headers,
                json={"location_id": loc1_id, "tipo_vaga": "carro", "valor_hora": 12.0}
            )
            assert t_dup_resp.status_code == 400

        finally:
            if vaga1_id:
                try:
                    time.sleep(2)
                    client.delete(f"{XANO_PARKING_URL}/vaga/{vaga1_id}", headers=admin_headers)
                except Exception:
                    pass
            if vaga2_id:
                try:
                    time.sleep(2)
                    client.delete(f"{XANO_PARKING_URL}/vaga/{vaga2_id}", headers=admin_headers)
                except Exception:
                    pass
            if tarifa1_id:
                try:
                    time.sleep(2)
                    client.delete(f"{XANO_PARKING_URL}/tarifa/{tarifa1_id}", headers=admin_headers)
                except Exception:
                    pass
            if tarifa2_id:
                try:
                    time.sleep(2)
                    client.delete(f"{XANO_PARKING_URL}/tarifa/{tarifa2_id}", headers=admin_headers)
                except Exception:
                    pass
            if loc1_id:
                try:
                    time.sleep(2)
                    client.delete(f"{XANO_PARKING_URL}/location/{loc1_id}", headers=admin_headers)
                except Exception:
                    pass
            if loc2_id:
                try:
                    time.sleep(2)
                    client.delete(f"{XANO_PARKING_URL}/location/{loc2_id}", headers=admin_headers)
                except Exception:
                    pass
