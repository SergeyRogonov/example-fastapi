import pytest

from app import schemas


def test_user_get_all_posts(client, test_posts):
    response = client.get("posts/")
    posts = [schemas.PostOut(**post) for post in response.json()]
    assert response.status_code == 200
    assert len(posts) == len(test_posts)


def test_user_get_one_post(client, test_posts):
    response = client.get(f"posts/{test_posts[0].id}")
    post = schemas.PostOut(**response.json())
    assert response.status_code == 200
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content
    assert post.Post.owner_id == test_posts[0].owner_id


def test_user_get_one_post_not_exist(client, test_posts):
    response = client.get("posts/9999")
    assert response.status_code == 404


@pytest.mark.parametrize(
    "title, content, published",
    [
        ("test_title_1", "test_content_1", True),
        ("test_title_2", "test_content_2", True),
        ("test_title_3", "test_content_3", False),
    ],
)
def test_create_post(authorized_client, test_user, title, content, published):
    response = authorized_client.post(
        "posts/", json={"title": title, "content": content, "published": published}
    )

    created_post = schemas.Post(**response.json())
    assert response.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user["id"]


def test_unauthorized_user_create_post(client, test_user, test_posts):
    response = client.post(
        "/posts/", json={"title": "some title", "content": "some content"}
    )
    assert response.status_code == 401


def test_unauthorized_user_delete_post(client, test_user, test_posts):
    response = client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401


def test_authorized_user_delete_post(authorized_client, test_user, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 204


def test_delete_nonexisting_post(authorized_client, test_user):
    response = authorized_client.delete("/posts/9999")
    assert response.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[2].id}")
    assert response.status_code == 403


def test_update_post(authorized_client, test_user, test_posts):
    data = {"title": "updated title", "content": "updated_content"}
    response = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**response.json())

    assert response.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]


def test_update_other_user_post(authorized_client, test_user, test_posts):
    data = {"title": "updated title", "content": "updated_content"}
    response = authorized_client.put(f"/posts/{test_posts[2].id}", json=data)
    assert response.status_code == 403


def test_unauthorized_user_update_post(client, test_posts):
    data = {"title": "updated title", "content": "updated_content"}
    response = client.put(f"/posts/{test_posts[0].id}", json=data)
    assert response.status_code == 401


def test_update_nonexisting_post(authorized_client, test_user, test_posts):
    data = {"title": "updated title", "content": "updated_content"}
    response = authorized_client.put("/posts/99999", json=data)
    assert response.status_code == 404
