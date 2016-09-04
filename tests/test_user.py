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
            'email': 'ayy@lmao.lmao',
            'password': 'ayylmaoayylmao'
        }
        # Goes to homepage
        res = testapp.post_json(url_for('api.user_user_item'),
                                params=data)
        print(res)
        assert res.status_code == 201
