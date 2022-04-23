from app.schemas import UserResponse, Token
from app.config import settings
from jose import jwt
import pytest


def test_create_user(client):
    response = client.post(
        "/users/", 
        json={"email" : "dinoman@gmail.com", "password" : "dinos4ever"}
    )
    new_user = UserResponse(**response.json())
    assert new_user.email == "dinoman@gmail.com"
    assert response.status_code == 201


def test_login_user(test_user1, client):
    response = client.post(
        "/login", 
        data={"username": test_user1['email'], "password": test_user1['password']}
    )
    
    login_response = Token(**response.json())
    
    payload = jwt.decode(
        login_response.access_token, 
        settings.secret_key, 
        algorithms=[settings.hashing_algorithm]
    )
    
    user_id = payload.get("user_id")
    
    assert user_id == test_user1['id']
    assert login_response.token_type == 'bearer'
    assert response.status_code == 201


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'dinos4ever', 403),
    ('dinoman@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'dinos4ever', 422),
    ('dinoman@gmail.com', None, 422)
])
def test_incorrect_login(test_user1, client, email, password, status_code):
    response = client.post(
        "/login",
        data={"username" : email, "password" : password}
    )
    assert response.status_code == status_code
