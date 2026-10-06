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
XANO_VEHICLE_URL = f"{XANO_API_BASE}/api:vehicle"

CLIENT_EMAIL = os.getenv("CLIENT_EMAIL", "pytest_client_estacionamento@example.com")
CLIENT_PASSWORD = os.getenv("CLIENT_PASSWORD", "ClientPassword123")

@pytest.fixture(scope="session")
def client_token():
    with httpx.Client(timeout=30.0) as client:
        time.sleep(2)
        client.post(
            f"{XANO_AUTH_URL}/auth/signup",
            json={"name": "Client Test Vehicle", "email": CLIENT_EMAIL, "password": CLIENT_PASSWORD, "role": "cliente"}
        )
        time.sleep(2)
        resp = client.post(f"{XANO_AUTH_URL}/auth/login", json={"email": CLIENT_EMAIL, "password": CLIENT_PASSWORD})
        assert resp.status_code == 200, f"Client login failed: {resp.text}"
        data = resp.json()
        token = data.get("authToken")
        assert token, "Client auth token not returned"
        return token

def test_vehicle_management_workflow(client_token):
    with httpx.Client(timeout=30.0) as client:
        headers = {"Authorization": f"Bearer {client_token}"}
        vehicle_id = None
        plate = f"TST-{int(time.time() % 10000):04d}"

        try:
            time.sleep(2)
            # Create vehicle
            resp = client.post(
                f"{XANO_VEHICLE_URL}/vehicle",
                headers=headers,
                json={"plate": plate, "brand": "Toyota", "model": "Corolla", "color": "Branco", "year": 2022}
            )
            assert resp.status_code == 200, f"Create vehicle failed: {resp.text}"
            vehicle_id = resp.json().get("id")

            time.sleep(2)
            # List vehicles
            list_resp = client.get(f"{XANO_VEHICLE_URL}/vehicle", headers=headers)
            assert list_resp.status_code == 200
            vehicles = list_resp.json()
            assert any(v.get("id") == vehicle_id for v in vehicles)

            time.sleep(2)
            # Edit vehicle
            edit_resp = client.put(
                f"{XANO_VEHICLE_URL}/vehicle/{vehicle_id}",
                headers=headers,
                json={"id": vehicle_id, "plate": plate, "brand": "Toyota", "model": "Camry", "color": "Prata", "year": 2023}
            )
            assert edit_resp.status_code == 200, f"Edit vehicle failed: {edit_resp.text}"
            assert edit_resp.json().get("model") == "Camry"

        finally:
            if vehicle_id:
                try:
                    time.sleep(2)
                    client.delete(f"{XANO_VEHICLE_URL}/vehicle/{vehicle_id}", headers=headers)
                except Exception:
                    pass
