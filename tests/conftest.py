from tests.database import engine, TestingSessionLocal
from app.database import get_db
from app.database import Base

from fastapi.testclient import TestClient
from app.oauth2 import create_access_token
from app.main import app
from app import models
import pytest


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user1(client):
    # Create new user
    user_data = {"email":"dinoman@gmail.com", "password": "dinos4ever"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201

    # Gain access to their password (because it's hashed otherwise)
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def test_user2(client):
    # Create new user
    user_data = {"email":"dinoman2@gmail.com", "password": "dinos5ever"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201

    # Gain access to their password (because it's hashed otherwise)
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user1):
    return create_access_token({"user_id": test_user1['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization" : f'Bearer {token}'
    }

    return client
 

@pytest.fixture
def test_posts(session, test_user1, test_user2):

    def create_post_model(post):
        return models.Post(**post)
    
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user1['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user1['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user1['id']
    }, {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user2['id']
    }]

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)
    session.commit()

    posts = session.query(models.Post).all()
    return posts


@pytest.fixture()
def test_vote(test_posts, session, test_user1):
    """
    Test_user1 is "liking" test_user2's post.
    """
    new_vote = models.Vote(post_id=test_posts[3].id, user_id=test_user1['id'])
    session.add(new_vote)
    session.commit()