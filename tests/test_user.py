# -*- coding: utf-8 -*-
"""Registration tests to ensure registration works."""
from flask import url_for


class TestRegister:
    """Register tests."""

    def test_can_register_returns_201(self, testapp):
        """Register successful."""
        data = {
            'firstname': 'ayy',
            'lastname': 'lmao',
            'email': 'user999@email.com',
            'password': '12345678'
        }
        # Goes to homepage
        res = testapp.post_json(url_for('api.user_user_item'),
                                params=data)
        print(res)
        assert res.status_code == 201

    def test_too_short_password_returns_400(self, testapp):
        """Register Unsuccessful."""
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

    def test_user_already_registered_returns_400(self, testapp):
        """Register Unsuccessful."""
        data = {
            'firstname': 'ayy',
            'lastname': 'lmao',
            'email': 'user999@email.com',
            'password': '1234567'
        }
        # Goes to homepage
        res = testapp.post_json(url_for('api.user_user_item'),
                                params=data, expect_errors=True)
        print(res)
        assert res.status_code == 400


class TestLogin:
    """Login tests"""

    def test_login_successful_returns_200(self, testapp):
        """Login successful"""
        data = {
            'email': 'user999@email.com',
            'password': '12345678'
        }
        res = testapp.post_json('/auth', params=data)
        print(res)
        assert res.status_code == 200

    def test_login_email_not_in_db_returns_401(self, testapp):
        """Login unsuccessful"""
        data = {
            'email': 'notindb@email.com',
            'password': 'password'
        }
        res = testapp.post_json('/auth', params=data, expect_errors=True)
        print(res)
        assert res.status_code == 401

    def test_login_incorrect_password_returns_401(self, testapp):
        """Login unsuccessful"""
        data = {
            'email': 'user999@email.com',
            'password': 'wrongpassword'
        }
        res = testapp.post_json('/auth', params=data, expect_errors=True)
        print(res)
        assert res.status_code == 401
