import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Soccer Team" in data


def test_signup_for_activity():
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    # Удалить если уже есть
    client.post(f"/activities/{activity}/unregister?email={email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]
    # Повторная регистрация должна вернуть ошибку
    response2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response2.status_code == 400


def test_unregister_from_activity():
    email = "removeme@mergington.edu"
    activity = "Soccer Team"
    # Зарегистрировать
    client.post(f"/activities/{activity}/signup?email={email}")
    # Удалить
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    assert f"{email} удалён из {activity}" in response.json()["message"]
    # Повторное удаление должно вернуть ошибку
    response2 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response2.status_code == 400
