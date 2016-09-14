# -*- coding: utf-8 -*-
"""Registration tests to ensure registration works."""
from flask import url_for


class TestRegister:
    """Register tests."""

    def test_can_register_returns_201(self, testapp):
        """Login successful."""
        data = {
            'firstname': 'ayy',
            'lastname': 'lmao',
            'email': 'user222@email.com',
            'password': '12345678'
        }
        # Goes to homepage
        res = testapp.post_json(url_for('api.user_user_item'),
                                params=data)
        print(res)
        assert res.status_code == 201

    def test_too_short_password_returns_400(self, testapp):
        """Login Unsuccessful."""
        data = {
            'firstname': 'ayy',
            'lastname': 'lmao',
            'email': 'user333@email.com',
            'password': '1234567'
        }
        # Goes to homepage
        res = testapp.post_json(url_for('api.user_user_item'),
                                params=data, expect_errors=True)
        print(res)
        assert res.status_code == 400
