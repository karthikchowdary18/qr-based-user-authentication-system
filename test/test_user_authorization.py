from std_msgs.msg import Bool, String


def test_auth_success(node):
    node.on_login_id(String(data='1234'))
    node.on_user_input(String(data='1234'))

    node.pub_auth_done.publish.assert_called_once()
    msg = node.pub_auth_done.publish.call_args[0][0]
    assert isinstance(msg, Bool)
    assert msg.data is True


def test_auth_failure(node):
    node.on_login_id(String(data='1234'))
    node.on_user_input(String(data='9999'))

    node.pub_auth_done.publish.assert_called_once()
    msg = node.pub_auth_done.publish.call_args[0][0]
    assert msg.data is False


def test_no_publish_when_state_does_not_change(node):
    node.on_login_id(String(data='1111'))
    node.on_user_input(String(data='2222'))
    node.on_user_input(String(data='2222'))

    assert node.pub_auth_done.publish.call_count == 1


def test_main_function(monkeypatch):
    import user_authorization.user_authorization as ua

    class FakeNode:
        def destroy_node(self):
            pass

    monkeypatch.setattr(ua.rclpy, 'init', lambda *a, **k: None)
    monkeypatch.setattr(ua.rclpy, 'spin', lambda *a, **k: None)
    monkeypatch.setattr(ua.rclpy, 'shutdown', lambda *a, **k: None)
    monkeypatch.setattr(ua, 'UserAuthorization', FakeNode)

    ua.main()
