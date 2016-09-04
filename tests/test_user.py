# -*- coding: utf-8 -*-
"""Registration tests to ensure registration works."""
import json
from flask import url_for


class TestRegister:
    """Register tests."""

    def test_can_register_returns_200(self, testapp):
        """Login successful."""
        data = {
            'firstname': 'ayy',
            'lastname': 'lmao',
            'email': 'ayy@lmao.lmao',
            'password': 'ayylmaoayylmao'
        }
        # Goes to homepage
        res = testapp.post_json(url_for('public.login'),
                                params=data)
        print(res)
        assert res.status_code == 200
