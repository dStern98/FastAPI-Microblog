

def test_vote_unauthorized(clear_collections, test_client):
    action = {"action": "like"}
    vote_response = test_client.post(
        "/vote/", params={"postID": "fakeUserID"}, json=action)
    assert vote_response.status_code == 401


def test_vote_invalid_action(clear_collections, login_user1, test_client):
    auth_header = {"Authorization": f"Bearer {login_user1}"}
    action = {"action": "fly a plane"}
    vote_response = test_client.post(
        "/vote/", json=action, headers=auth_header, params={"postID": "fakePostID"})
    assert vote_response.status_code == 422


def test_vote_like(clear_collections, login_user1, get_posts, test_client):
    header_dict = {"Authorization": f"Bearer {login_user1}"}
    post1 = get_posts[0]

    # Post the Post
    test_client.post("/posts/", headers=header_dict, json=post1)
    # Now get the postID
    get_post = test_client.get("/posts/", params={"title": post1["title"]})
    get_post_json = get_post.json()["Posts"][0]
    postID = get_post_json["postID"]

    # The first time liked, increase likes by 1
    test_client.post(
        "/vote/", params={"postID": postID}, json={"action": "like"}, headers=header_dict)
    get_post2 = test_client.get("/posts/", params={"title": post1["title"]})
    assert get_post2.json()["Posts"][0]["likes"] == 1

    # The second time, decrease the likes by 1
    test_client.post(
        "/vote/", params={"postID": postID}, json={"action": "like"}, headers=header_dict)
    get_post3 = test_client.get("/posts/", params={"title": post1["title"]})
    assert get_post3.json()["Posts"][0]["likes"] == 0


def test_vote_dislike(clear_collections, login_user1, get_posts, test_client):
    header_dict = {"Authorization": f"Bearer {login_user1}"}
    post1 = get_posts[0]

    # Post the Post
    test_client.post("/posts/", headers=header_dict, json=post1)
    # Now get the postID
    get_post = test_client.get("/posts/", params={"title": post1["title"]})
    get_post_json = get_post.json()["Posts"][0]
    postID = get_post_json["postID"]

    # Now try to vote on the post
    # The third time, dislike the post
    test_client.post(
        "/vote/", params={"postID": postID}, json={"action": "dislike"}, headers=header_dict)
    get_post3 = test_client.get("/posts/", params={"title": post1["title"]})
    assert get_post3.json()["Posts"][0]["dislikes"] == 1

    # the fourth time, dislike the post, total dislikes show return to 0
    test_client.post(
        "/vote/", params={"postID": postID}, json={"action": "dislike"}, headers=header_dict)
    get_post3 = test_client.get("/posts/", params={"title": post1["title"]})
    assert get_post3.json()["Posts"][0]["dislikes"] == 0


def test_vote_like_then_dislike(clear_collections, login_user1, get_posts, test_client):
    header_dict = {"Authorization": f"Bearer {login_user1}"}
    post1 = get_posts[0]

    # Post the Post
    test_client.post("/posts/", headers=header_dict, json=post1)
    # Now get the postID
    get_post = test_client.get("/posts/", params={"title": post1["title"]})
    get_post_json = get_post.json()["Posts"][0]
    postID = get_post_json["postID"]

    # Liking in this case should increase the likes count to 1
    test_client.post(
        "/vote/", params={"postID": postID}, json={"action": "like"}, headers=header_dict)
    get_post3 = test_client.get("/posts/", params={"title": post1["title"]})
    assert get_post3.json()["Posts"][0]["likes"] == 1
    assert get_post3.json()["Posts"][0]["dislikes"] == 0

    # the fourth time, dislike the post, dislikes show go to 1, likes to 0
    test_client.post(
        "/vote/", params={"postID": postID}, json={"action": "dislike"}, headers=header_dict)
    get_post3 = test_client.get("/posts/", params={"title": post1["title"]})
    assert get_post3.json()["Posts"][0]["likes"] == 0
    assert get_post3.json()["Posts"][0]["dislikes"] == 1


def test_vote_dislike_then_like(clear_collections, login_user1, get_posts, test_client):
    header_dict = {"Authorization": f"Bearer {login_user1}"}
    post1 = get_posts[0]

    # Post the Post
    test_client.post("/posts/", headers=header_dict, json=post1)
    # Now get the postID
    get_post = test_client.get("/posts/", params={"title": post1["title"]})
    get_post_json = get_post.json()["Posts"][0]
    postID = get_post_json["postID"]

    # Liking in this case should increase the likes count to 1
    test_client.post(
        "/vote/", params={"postID": postID}, json={"action": "dislike"}, headers=header_dict)
    get_post3 = test_client.get("/posts/", params={"title": post1["title"]})
    assert get_post3.json()["Posts"][0]["likes"] == 0
    assert get_post3.json()["Posts"][0]["dislikes"] == 1

    # the fourth time, dislike the post, dislikes show go to 1, likes to 0
    test_client.post(
        "/vote/", params={"postID": postID}, json={"action": "like"}, headers=header_dict)
    get_post3 = test_client.get("/posts/", params={"title": post1["title"]})
    assert get_post3.json()["Posts"][0]["likes"] == 1
    assert get_post3.json()["Posts"][0]["dislikes"] == 0


def test_vote_two_users(clear_collections, login_user1, login_user2, get_posts, test_client):
    assert login_user1 != login_user2
    header_dict1 = {"Authorization": f"Bearer {login_user1}"}
    header_dict2 = {"Authorization": f"Bearer {login_user2}"}
    post2 = get_posts[1]
    # Post the Post
    test_client.post("/posts/", headers=header_dict1, json=post2)
    # Now get the postID
    get_post = test_client.get("/posts/", params={"title": post2["title"]})
    get_post_json = get_post.json()["Posts"][0]
    postID = get_post_json["postID"]

    # Liking in this case should increase the likes count to 1
    test_client.post(
        "/vote/", params={"postID": postID}, json={"action": "dislike"}, headers=header_dict1)
    get_post3 = test_client.get("/posts/", params={"title": post2["title"]})
    assert get_post3.json()["Posts"][0]["likes"] == 0
    assert get_post3.json()["Posts"][0]["dislikes"] == 1

    # the fourth time, dislike the post, dislikes show go to 1, likes to 0
    test_client.post(
        "/vote/", params={"postID": postID}, json={"action": "like"}, headers=header_dict2)
    get_post4 = test_client.get("/posts/", params={"title": post2["title"]})
    assert get_post4.json()["Posts"][0]["likes"] == 1
    assert get_post4.json()["Posts"][0]["dislikes"] == 1


def test_check_user_actions(clear_collections, login_user1, get_posts, test_client):
    post1 = get_posts[0]
    header_dict = {"Authorization": f"Bearer {login_user1}"}
    test_client.post("/posts/", headers=header_dict, json=post1)
    postID = test_client.get("/posts/").json()["Posts"][0]["postID"]

    # Now vote on the post
    like_post = test_client.post(
        "/vote/", headers=header_dict, params={"postID": postID}, json={"action": "like"})

    # Now check the users vote on that post
    vote_action = test_client.post(
        "/vote/userVotes/", headers=header_dict, json={"postIDs": [postID]})
    assert vote_action.status_code == 200
    assert vote_action.json()["User_Votes"][0]["action"] == "like"


def test_check_post_actions(clear_collections, login_user1, get_posts, test_client):
    post1 = get_posts[0]
    header_dict = {"Authorization": f"Bearer {login_user1}"}
    test_client.post("/posts/", headers=header_dict, json=post1)
    postID = test_client.get("/posts/").json()["Posts"][0]["postID"]

    # Now vote on the post
    like_post = test_client.post(
        "/vote/", headers=header_dict, params={"postID": postID}, json={"action": "like"})

    # Now check the posts votes
    vote_action = test_client.post(
        "/vote/postVotes/", params={"postID": postID})
    assert vote_action.status_code == 200
    assert vote_action.json()["Post_Votes"][0]["action"] == "like"
