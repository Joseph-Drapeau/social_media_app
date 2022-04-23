from app.schemas import Post, PostOut
from app import models
import pytest


# Test Get Posts
def test_get_all_posts(authorized_client, test_posts):
    
    def validate(post):
        return PostOut(**post)

    response = authorized_client.get("/posts/")
    assert response.status_code == 200
    
    post_map = map(validate, response.json())
    posts = list(post_map)
    assert len(response.json()) == len(test_posts)


def test_unauthorized_user_get_all_posts(client, test_posts):
    response = client.get("/posts/")
    assert response.status_code == 401


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title


def test_get_one_post_not_exist(authorized_client, test_posts):
    response = authorized_client.get("/posts/10000")
    assert response.status_code == 404


def test_unauthorized_user_get_one_post(client, test_posts):
    response = client.get(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401


# Test Create Posts
@pytest.mark.parametrize("title, content, published", [
    ("Hawaii", "volcanoes", True),
    ("Texas", "BBQ", False),
    ("indiana", "dunes", True),
])
def test_create_post(authorized_client, test_user1, test_posts, title, content, published):
    response = authorized_client.post(
        "/posts/", 
        json={"title": title, "content": content, "published": published}
    )
    created_post = Post(**response.json())
    assert response.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user1['id']


def test_create_post_default_published_true(authorized_client, test_user1, test_posts):
    response = authorized_client.post(
        "/posts/", 
        json={"title": "title", "content": "content"}
    )
    created_post = Post(**response.json())
    assert response.status_code == 201
    assert created_post.title == "title"
    assert created_post.content == "content"
    assert created_post.published == True
    assert created_post.owner_id == test_user1['id']


def test_unauthorized_user_create_post(client, test_user1, test_posts):
    response = client.post(
        "/posts/", 
        json={"title": "title", "content": "content"}
    )
    assert response.status_code == 401


# Test Delete Posts
def test_delete_post_success(authorized_client, test_user1, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 204
    

def test_delete_post_non_exist(authorized_client, test_user1, test_posts):
    response = authorized_client.delete("/posts/10000")
    assert response.status_code == 404


def test_unauthorized_user_delete_Post(client, test_user1, test_posts):
    response = client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401


def test_delete_other_user_post(authorized_client, test_user1, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert response.status_code == 403


# Test Update posts
def test_update_post(authorized_client, test_user1, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[0].id
    }
    response = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = Post(**response.json())
    assert response.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']


def test_update_post_non_exist(authorized_client, test_user1, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[3].id
    }
    response = authorized_client.put(f"/posts/10000", json=data)
    assert response.status_code == 404


def test_unauthorized_user_update_post(client, test_user1, test_posts):
    res = client.put(
        f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_update_other_user_post(authorized_client, test_user1, test_user2, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[3].id
    }
    response = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert response.status_code == 403
