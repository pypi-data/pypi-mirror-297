from datetime import datetime
import os
import pytest

import pythonlemmy as plemmy
from pythonlemmy.responses import CommentResponse, PostResponse


COMMUNITY_ID: int = int(os.environ.get("COMMUNITY_ID"))
COMMUNITY_NAME: str = os.environ.get("COMMUNITY_NAME")
INSTANCE_URL: str = os.environ.get("INSTANCE_URL")
PASSWORD: str = os.environ.get("PASSWORD")
USERNAME: str = os.environ.get("USERNAME")


def test_login() -> None:

    # initialize instance
    instance = plemmy.LemmyHttp(INSTANCE_URL)

    # login
    response = instance.login(USERNAME, PASSWORD)

    # check if successful
    if response.status_code != 200:
        pytest.fail(f"{response.reason}")


def test_get_community() -> None:

    # initialize instance
    instance = plemmy.LemmyHttp(INSTANCE_URL)

    # get community
    response = instance.get_community(name=COMMUNITY_NAME)

    # check if successful
    if response.status_code != 200:
        pytest.fail(f"{response.reason}")


def test_create_delete_comment_and_post() -> None:

    # initialize instance
    instance = plemmy.LemmyHttp(INSTANCE_URL)

    # login
    instance.login(USERNAME, PASSWORD)

    # create post
    response_post_create = instance.create_post(
        f"Plemmy unit test {datetime.utcnow()}",
        COMMUNITY_ID,
        body="Unit test body text"
    )

    if response_post_create.status_code != 200:
        pytest.fail(f"{response_post_create.reason}")

    # parse post response
    post_response = PostResponse(response_post_create)

    # create comment
    response_comment_create = instance.create_comment(
        f"Unit test comment {datetime.utcnow()}",
        post_response.post_view.post.id
    )

    # check if successful
    if response_comment_create.status_code != 200:
        pytest.fail(f"{response_comment_create.reason}")

    # parse comment response
    comment_response = CommentResponse(response_comment_create)

    # delete comment
    response_comment_delete = instance.delete_comment(
        comment_response.comment_view.comment.id, True
    )

    # check if successful
    if response_comment_delete.status_code != 200:
        pytest.fail(f"{response_comment_delete.reason}")

    # delete post
    response_post_delete = instance.delete_post(
        post_response.post_view.post.id, True
    )

    if response_post_delete.status_code != 200:
        pytest.fail(f"{response_post_delete.reason}")