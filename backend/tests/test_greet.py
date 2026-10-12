from fastapi.testclient import TestClient

from app.main import app


def test_greet() -> None:
    res = TestClient(app).get("/greet?name=sam")
    assert res.status_code == 200
    assert res.json() == {"message": "hi sam"}


def test_get_greet_requires_name() -> None:
    res = TestClient(app).get("/greet")
    assert res.status_code == 422
    assert res.json()["detail"][0]["loc"] == ["query", "name"]


def test_greet_post() -> None:
    res = TestClient(app).post("/greet", json={"name": "sam", "excited": True})
    assert res.status_code == 200
    assert res.json() == {"message": "hi sam!"}


def test_post_greet_requires_name() -> None:
    res = TestClient(app).post("/greet", json={"excited": True})
    assert res.status_code == 422
    assert res.json()["detail"][0]["loc"] == ["body", "name"]
