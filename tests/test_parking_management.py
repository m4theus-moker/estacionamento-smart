import os
import time
import pytest
import httpx

XANO_API_BASE = os.getenv("XANO_API_BASE", "https://x8ki-letl-twmt.n7.xano.io")
XANO_AUTH_URL = f"{XANO_API_BASE}/api:o7T2IhYl"
XANO_PARKING_URL = f"{XANO_API_BASE}/api:parking"

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "pytest_admin_estacionamento@example.com")
ADMIN_PASSWORD = os.environ["ADMIN_PASSWORD"]
CLIENT_EMAIL = os.getenv("CLIENT_EMAIL", "pytest_client_estacionamento@example.com")
CLIENT_PASSWORD = os.environ["CLIENT_PASSWORD"]

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

        try:
            time.sleep(4)
            # Cleanup any leftover test data first
            list_resp = client.get(f"{XANO_PARKING_URL}/vaga", headers=admin_headers)
            if list_resp.status_code == 200:
                for v in list_resp.json():
                    if v.get("numero", "").startswith("TESTE-"):
                        time.sleep(4)
                        client.request("DELETE", f"{XANO_PARKING_URL}/vaga", json={"id": v["id"]}, headers=admin_headers)

            time.sleep(4)
            list_t_resp = client.get(f"{XANO_PARKING_URL}/tarifa", headers=admin_headers)
            if list_t_resp.status_code == 200:
                for t in list_t_resp.json():
                    if t.get("tipo_vaga") == tarifa_tipo:
                        time.sleep(4)
                        client.request("DELETE", f"{XANO_PARKING_URL}/tarifa", json={"id": t["id"]}, headers=admin_headers)

            time.sleep(4)
            # 1. Admin creates vaga success
            resp = client.post(
                f"{XANO_PARKING_URL}/vaga",
                headers=admin_headers,
                json={"numero": vaga_numero, "tipo": vaga_tipo}
            )
            assert resp.status_code == 200, f"Create vaga failed: {resp.text}"
            vaga_data = resp.json()
            vaga_id = vaga_data["id"]

            time.sleep(4)
            # 2. Duplicate vaga numero rejection (inputerror)
            resp = client.post(
                f"{XANO_PARKING_URL}/vaga",
                headers=admin_headers,
                json={"numero": vaga_numero, "tipo": vaga_tipo}
            )
            assert resp.status_code == 400
            err_data = resp.json()
            assert "inputerror" in err_data.get("code", "").lower() or err_data.get("error_type") == "inputerror" or "existe" in err_data.get("message", "").lower()

            time.sleep(4)
            # 3. Client mutation access denied on vaga create
            resp = client.post(
                f"{XANO_PARKING_URL}/vaga",
                headers=client_headers,
                json={"numero": "TESTE-VAGA-CLIENT", "tipo": vaga_tipo}
            )
            assert resp.status_code in [401, 403]

            time.sleep(4)
            # 4. Admin edits vaga success
            resp = client.put(
                f"{XANO_PARKING_URL}/vaga",
                headers=admin_headers,
                json={"id": vaga_id, "numero": vaga_numero_edit, "tipo": vaga_tipo_edit, "status": "livre"}
            )
            assert resp.status_code == 200, f"Edit vaga failed: {resp.text}"

            time.sleep(4)
            # 5. Client listing success (GET)
            resp = client.get(f"{XANO_PARKING_URL}/vaga", headers=client_headers)
            assert resp.status_code == 200

            time.sleep(4)
            # 6. Admin creates tarifa success (tipo_vaga: carro)
            resp = client.post(
                f"{XANO_PARKING_URL}/tarifa",
                headers=admin_headers,
                json={"tipo_vaga": tarifa_tipo, "valor_hora": tarifa_valor}
            )
            if resp.status_code == 400:
                time.sleep(4)
                t_list = client.get(f"{XANO_PARKING_URL}/tarifa", headers=admin_headers).json()
                for t in t_list:
                    if t.get("tipo_vaga") == tarifa_tipo:
                        time.sleep(4)
                        client.request("DELETE", f"{XANO_PARKING_URL}/tarifa", json={"id": t["id"]}, headers=admin_headers)
                time.sleep(4)
                resp = client.post(
                    f"{XANO_PARKING_URL}/tarifa",
                    headers=admin_headers,
                    json={"tipo_vaga": tarifa_tipo, "valor_hora": tarifa_valor}
                )
            assert resp.status_code == 200, f"Create tarifa failed: {resp.text}"
            tarifa_data = resp.json()
            tarifa_id = tarifa_data["id"]

            time.sleep(4)
            # 7. Duplicate tarifa tipo_vaga rejection (inputerror)
            resp = client.post(
                f"{XANO_PARKING_URL}/tarifa",
                headers=admin_headers,
                json={"tipo_vaga": tarifa_tipo, "valor_hora": tarifa_valor}
            )
            assert resp.status_code == 400
            err_data = resp.json()
            assert "inputerror" in err_data.get("code", "").lower() or err_data.get("error_type") == "inputerror" or "existe" in err_data.get("message", "").lower()

            time.sleep(4)
            # 8. Admin edits tarifa success
            resp = client.put(
                f"{XANO_PARKING_URL}/tarifa",
                headers=admin_headers,
                json={"id": tarifa_id, "tipo_vaga": tarifa_tipo, "valor_hora": tarifa_valor_edit}
            )
            assert resp.status_code == 200, f"Edit tarifa failed: {resp.text}"

            time.sleep(4)
            # 9. Client mutation access denied on tarifa edit
            resp = client.put(
                f"{XANO_PARKING_URL}/tarifa",
                headers=client_headers,
                json={"id": tarifa_id, "tipo_vaga": tarifa_tipo, "valor_hora": 30.00}
            )
            assert resp.status_code in [401, 403]

        finally:
            # 10. Cleanup: delete test vaga and test tarifa guaranteed
            if vaga_id:
                try:
                    time.sleep(3)
                    client.request("DELETE", f"{XANO_PARKING_URL}/vaga", json={"id": vaga_id}, headers=admin_headers)
                except Exception:
                    pass
            if tarifa_id:
                try:
                    time.sleep(3)
                    client.request("DELETE", f"{XANO_PARKING_URL}/tarifa", json={"id": tarifa_id}, headers=admin_headers)
                except Exception:
                    pass
