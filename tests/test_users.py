
def test_post_user(clear_collections, get_users, test_client):
    json_body = get_users[0]
    response = test_client.post("/users/", json=json_body)
    assert response.status_code == 201
    assert response.json() == {
        "Message": "Successfully created new user",
        "email": "Tevye@gmail.com",
        "Name": "Shalom Aleichem",
        "username": "TevyeTheMilkman"
    }

# Check that if you try to post a user with a username that already exists, the operation fails


def test_duplicate_username(clear_collections, get_users, test_client):
    user1, user2 = get_users
    user1_username = user1["username"]
    user2["username"] = user1_username
    post_user1 = test_client.post("/users/", json=user1)
    assert post_user1.status_code == 201

    post_user2 = test_client.post("/users/", json=user2)
    assert post_user2.status_code == 403


def test_delete_user_unauthorized(clear_collections, get_users, test_client):
    # Try to delete the post without being signed in
    delete_response = test_client.delete("/users/")
    assert delete_response.status_code == 401


def test_delete_user(clear_collections, login_user1, test_client):
    header_dict = {"Authorization": f"Bearer {login_user1}"}
    delete_response = test_client.delete("/users/", headers=header_dict)
    assert delete_response.status_code == 200
    get_response = test_client.get(
        "/users/search/", params={"username_search": "Tevye"})
    assert len(get_response.json()["Users"]) == 0


def test_patch_user_unauthorized(clear_collections, test_client):
    update_body = {"username": "Perchik"}
    patch_response = test_client.patch("/users/", json=update_body)
    assert patch_response.status_code == 401


def test_patch_user(clear_collections, login_user1, test_client):
    update_body = {"username": "Perchik"}
    patch_response = test_client.patch(
        "/users/", json=update_body, headers={"Authorization": f"Bearer {login_user1}"})
    assert patch_response.status_code == 200
    get_response = test_client.get(
        "/users/search/", params={"username_search": "Perchik"})
    assert len(get_response.json()["Users"]) > 0
    assert get_response.json()["Users"][0]["first_name"] == "Shalom"


def test_search_get(clear_collections, login_user1, test_client):
    response_search1 = test_client.get(
        "/users/search/", params={"username_search": "Tevye"})
    response_search2 = test_client.get(
        "/users/search/", params={"username_search": "Milkman"})
    assert response_search1.status_code == 200
    assert response_search2.status_code == 200
    assert response_search1.json()["Users"][0]["username"] == "TevyeTheMilkman"
    assert response_search2.json()["Users"][0]["username"] == "TevyeTheMilkman"


def test_get_one_user(clear_collections, login_user1, test_client):
    header_dict = {"Authorization": f"Bearer {login_user1}"}
    standard_get = test_client.get("/users/", headers=header_dict)
    assert standard_get.status_code == 200
    assert standard_get.json()["Users"]["username"] == "TevyeTheMilkman"
    assert standard_get.json()["Users"]["email"] == "Tevye@gmail.com"
