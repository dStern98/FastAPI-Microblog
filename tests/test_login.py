
def test_login_no_user(clear_collections, test_client):
    login_response = test_client.post(
        "/login/", data={"username": "does not exist", "password": "password123"})
    assert login_response.status_code == 403


def test_login_bad_password(clear_collections, get_users, login_user1, test_client):
    user1 = get_users[0]
    user1_password_form = {key: value for key, value in user1.items() if key in [
        "username", "password"]}
    user1_password_form["password"] = "incorrectpassword"
    login_response = test_client.post("/login/", data=user1_password_form)
    assert login_response.status_code == 403


def test_correct_login(clear_collections, get_users, login_user1, test_client):
    user1 = get_users[0]
    user1_password_form = {key: value for key, value in user1.items() if key in [
        "username", "password"]}
    login_response = test_client.post("/login/", data=user1_password_form)
    assert login_response.status_code == 200
    print(login_response.json())
