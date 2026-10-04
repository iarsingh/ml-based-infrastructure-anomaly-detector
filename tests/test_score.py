from fastapi.testclient import TestClient
from infraanom.main import app

client = TestClient(app)


def test_high_and_low():
    assert client.post("/score", json={'cpu': 96, 'memory': 94, 'restarts': 4}).json()["label"]
    high = client.post("/score", json={'cpu': 96, 'memory': 94, 'restarts': 4}).json()
    low = client.post("/score", json={'cpu': 12, 'memory': 20, 'restarts': 0}).json()
    assert high["label"] != low["label"]
    assert high["score"] > low["score"]


def test_missing_is_refused():
    body = dict({'cpu': 96, 'memory': 94, 'restarts': 4})
    body.pop("cpu")
    assert client.post("/score", json=body).status_code == 422
