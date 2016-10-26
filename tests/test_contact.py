# -*- coding: utf-8 -*-
"""Contact tests to ensure contacting works."""

from flask import url_for


class TestContact:
    """Contact tests."""

    def test_message_send_returns_201(self, testapp):
        """Message successful."""
        data = {
            'email': 'user222@email.com',
            'content': '12345678'
        }
        res = testapp.post_json(url_for('api.contact_message_item'),
                                params=data)
        print(res)
        assert res.status_code == 201

    def test_get_messages_returns_201(self, testapp):
        """Get messages successful."""
        res = testapp.get(url_for('api.contact_message_item'))
        print(res)
        assert res.status_code == 201
