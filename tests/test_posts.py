
def test_post_post_unauthorized(clear_collections, get_posts, test_client):
    post1 = get_posts[0]
    response_post = test_client.post("/posts/", json=post1)
    assert response_post.status_code == 401


def test_post_correct(clear_collections, get_posts, login_user1, test_client):
    header_dict = {"Authorization": f"Bearer {login_user1}"}
    post1 = get_posts[0]
    response_post = test_client.post(
        "/posts/", headers=header_dict, json=post1)
    assert response_post.status_code == 201

    response_get = test_client.get("/posts/", params={"title": post1["title"]})
    assert response_get.json()["Posts"][0]["content"] == post1["content"]


def test_delete_unauthorized(clear_collections, get_posts, test_client):
    post1 = get_posts[0]
    delete_response = test_client.delete("/posts/fakeObjectID/")
    assert delete_response.status_code == 401


def test_delete_not_post_owner(clear_collections, get_posts, login_user1, login_user2, test_client):
    assert login_user1 != login_user2
    header_dict1 = {"Authorization": f"Bearer {login_user1}"}
    header_dict2 = {"Authorization": f"Bearer {login_user2}"}
    post1 = get_posts[0]

    # First, post the post
    test_client.post("/posts/", headers=header_dict1, json=post1)
    get_post = test_client.get(
        '/posts/', params={"title": post1["title"]})
    postID = get_post.json()["Posts"][0]["postID"]

    # First, try to delete logged in as user2
    delete_attempt1 = test_client.delete(
        f"/posts/{postID}/", headers=header_dict2)
    assert delete_attempt1.status_code == 403


def test_delete_post_owner(clear_collections, get_posts, login_user2, test_client):
    header_dict2 = {"Authorization": f"Bearer {login_user2}"}
    post2 = get_posts[1]

    # First, post the post
    test_client.post("/posts/", headers=header_dict2, json=post2)
    get_post = test_client.get("/posts/", params={"title": post2["title"]})
    postID = get_post.json()["Posts"][0]["postID"]

    # Now delete correctly
    delete_attempt = test_client.delete(
        f"/posts/{postID}/", headers=header_dict2)
    assert delete_attempt.status_code == 200

    # Ensure that the post is gone from the database
    get_post2 = test_client.get("/posts/", params={"title": post2["title"]})
    assert len(get_post2.json()["Posts"]) == 0


def test_patch_unauthorized(clear_collections, test_client):
    update_json = {"title": "This test should fail with 401"}
    patch_response = test_client.patch("/posts/fakePostID/", json=update_json)
    assert patch_response.status_code == 401


def test_patch_not_post_owner(clear_collections, get_posts, login_user1, login_user2, test_client):
    assert login_user1 != login_user2
    header_dict1 = {"Authorization": f"Bearer {login_user1}"}
    header_dict2 = {"Authorization": f"Bearer {login_user2}"}
    update_json = {"title": "This test should fail with 403"}
    post1 = get_posts[0]

    # First, post the post
    test_client.post("/posts/", headers=header_dict1, json=post1)
    get_post = test_client.get(
        '/posts/', params={"title": post1["title"]})
    postID = get_post.json()["Posts"][0]["postID"]

    # First, try to delete logged in as user2
    patch_attempt = test_client.patch(
        f"/posts/{postID}/", headers=header_dict2, json=update_json)
    assert patch_attempt.status_code == 403


def test_patch_post_owner(clear_collections, get_posts, login_user1, test_client):
    header_dict1 = {"Authorization": f"Bearer {login_user1}"}
    update_json = {"title": "This test should pass"}
    post1 = get_posts[0]

    # First, post the post
    test_client.post("/posts/", headers=header_dict1, json=post1)
    get_post = test_client.get(
        '/posts/', params={"title": post1["title"]})
    postID = get_post.json()["Posts"][0]["postID"]

    # First, try to delete logged in as user2
    patch_attempt = test_client.patch(
        f"/posts/{postID}/", headers=header_dict1, json=update_json)
    assert patch_attempt.status_code == 200

    # Now check that the post is still there, but updated
    get_post = test_client.get(
        '/posts/', params={"title": update_json["title"]})

    assert get_post.json()["Posts"][0]["title"] == update_json["title"]
