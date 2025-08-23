from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_docs():
    r = client.get('/docs')
    assert r.status_code == 200
