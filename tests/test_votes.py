import pytest


vote_url = "/votes/"


# Recall "like" is a boolean of the Vote schema where True is a like and False is not a like

# Test Creating a like
def test_vote_unauthorized_user(client, test_posts):
    response = client.post(
        vote_url, 
        json={"post_id": f"{test_posts[3].id}", "like": "True"}
    )
    assert response.status_code == 401


def test_vote_on_post(authorized_client, test_posts, test_user1, test_user2):
    response = authorized_client.post(
        vote_url,
        json = {"post_id":f"{test_posts[3].id}", "like": "True"}
    )
    assert response.status_code == 201

def test_vote_twice_post(authorized_client, test_posts, test_vote):
    response = authorized_client.post(
        vote_url,
        json = {"post_id": test_posts[3].id, "like": True}
    )
    assert response.status_code == 409


def test_vote_post_non_exist(authorized_client, test_posts):
    response = authorized_client.post(
        vote_url,
        json = {"post_id": 30, "like": True}
    )
    assert response.status_code == 404


# Test Deleting a like
def test_delete_vote(authorized_client, test_posts, test_vote):
    response = authorized_client.post(
        vote_url,
        json = {"post_id": test_posts[3].id, "like": False})
    assert response.status_code == 201


def test_delete_vote_non_exist(authorized_client, test_posts):
    res = authorized_client.post(
        vote_url, 
        json={"post_id": test_posts[3].id, "like": False})
    assert res.status_code == 404
