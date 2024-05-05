import requests
import json
from pytest import fixture


@fixture
def base_url():
    return "http://localhost:5000/api/v1"


@fixture
def auth_headers(mocker):
    access_token = "_ACCESS_TOKEN"
    mocker.patch("requests.Session.auth", return_value=(None, access_token))
    return {"Authorization": f"Bearer {access_token}"}


def test_create_post(base_url, auth_headers):
    data = {"title": "Test Post", "content": "This is a test post"}
    response = requests.post(f"{base_url}/posts", json=data, headers=auth_headers)
    assert response.status_code == 201

    response_data = response.json()
    assert response_data["title"] == data["title"]


def test_read_post(base_url, auth_headers, create_test_post):
    post_id = create_test_post
    response = requests.get(f"{base_url}/posts/{post_id}", headers=auth_headers)
    assert response.status_code == 200

    response_data = response.json()
    assert response_data["id"] == post_id


@fixture
def create_test_post(base_url, auth_headers):
    data = {"title": "Test Post", "content": "This is a test post"}
    response = requests.post(f"{base_url}/posts", json=data, headers=auth_headers)
    assert response.status_code == 201

    response_data = response.json()
    return response_data["id"]  


def test_update_post(base_url, auth_headers, create_test_post):
    post_id = create_test_post
    data = {"title": "Updated Test Post", "content": "Content has been updated"}
    response = requests.put(f"{base_url}/posts/{post_id}", json=data, headers=auth_headers)
    assert response.status_code == 200

    response_data = response.json()
    assert response_data["title"] == data["title"]


def test_delete_post(base_url, auth_headers, create_test_post):
    post_id = create_test_post
    response = requests.delete(f"{base_url}/posts/{post_id}", headers=auth_headers)
    assert response.status_code == 204


def test_create_post_missing_title(base_url, auth_headers):
    data = {"content": "This is a test post for API testing"}
    response = requests.post(f"{base_url}/posts", json=data, headers=auth_headers)
    assert response.status_code == 400  


def test_create_post_unauthorized(base_url):
    data = {"title": "Test Post", "content": "This is a test post"}
    response = requests.post(f"{base_url}/posts", json=data)
    assert response.status_code == 401  
