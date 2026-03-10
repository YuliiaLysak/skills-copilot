import pytest


def test_root_redirect(client):
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_root_redirect_follow(client):
    response = client.get("/", follow_redirects=True)
    assert response.status_code == 200
