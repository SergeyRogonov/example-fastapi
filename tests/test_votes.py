import pytest

from app import models


@pytest.fixture
def test_vote(test_posts, test_user, session):
    new_vote = models.Vote(post_id=test_posts[1].id, user_id=test_user["id"])
    session.add(new_vote)
    session.commit()


def test_vote_on_post(authorized_client, test_posts):
    response = authorized_client.post(
        "/votes/", json={"post_id": test_posts[0].id, "dir": 1}
    )
    assert response.status_code == 201


def test_unauthorized_user_vote_on_post(client, test_posts):
    response = client.post("/votes/", json={"post_id": test_posts[0].id, "dir": 1})
    assert response.status_code == 401


def test_vote_on_another_user_post(authorized_client, test_posts):
    response = authorized_client.post(
        "/votes/", json={"post_id": test_posts[2].id, "dir": 1}
    )
    assert response.status_code == 201


def test_vote_twice_on_post(authorized_client, test_posts, test_vote):
    response = authorized_client.post(
        "/votes/", json={"post_id": test_posts[1].id, "dir": 1}
    )
    assert response.status_code == 409


def test_delete_vote(authorized_client, test_posts, test_vote):
    response = authorized_client.post(
        "/votes/", json={"post_id": test_posts[1].id, "dir": 0}
    )
    assert response.status_code == 201


def test_delete_nonexisting_vote(authorized_client, test_posts):
    response = authorized_client.post(
        "/votes/", json={"post_id": test_posts[0].id, "dir": 0}
    )
    assert response.status_code == 404


def test_vote_post_not_exist(authorized_client, test_posts):
    response = authorized_client.post("/votes/", json={"post_id": 99999, "dir": 1})
    assert response.status_code == 404
