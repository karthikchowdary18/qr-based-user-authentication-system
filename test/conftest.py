import pytest
from unittest.mock import MagicMock

import rclpy


@pytest.fixture
def node():
    rclpy.init()
    from user_authorization.user_authorization import UserAuthorization

    n = UserAuthorization()
    n.pub_auth_done = MagicMock()
    n.pub_auth_done.publish = MagicMock()

    yield n

    n.destroy_node()
    rclpy.shutdown()
