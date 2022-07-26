from jose import jwt
from app.routers.connectDB import settings


def test_login_no_user(clear_collections, test_client):
    login_response = test_client.post(
        "/login/", data={"username": "does not exist", "password": "password123"})
    assert login_response.status_code == 401


def test_login_bad_password(clear_collections, get_users, login_user1, test_client):
    user1 = get_users[0]
    user1_password_form = {key: value for key, value in user1.items() if key in [
        "username", "password"]}
    user1_password_form["password"] = "incorrectpassword"
    login_response = test_client.post("/login/", data=user1_password_form)
    assert login_response.status_code == 401


def test_correct_login(clear_collections, get_users, login_user1, test_client):
    user1 = get_users[0]
    user1_password_form = {key: value for key, value in user1.items() if key in [
        "username", "password"]}
    login_response = test_client.post("/login/", data=user1_password_form)
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]
    payload = jwt.decode(token, settings.auth_secret_key,
                         algorithms=[settings.auth_algorithm])
    userID = payload.get("userID")
    user_from_token = test_client.get(
        "/users/search/", params={"username_search": user1["username"]})
    assert user_from_token.json()["Users"][0]["userID"] == userID
