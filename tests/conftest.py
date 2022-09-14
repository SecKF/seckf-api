# -*- coding: utf-8 -*-
"""Defines fixtures available to all tests."""

import logging

import pytest
from webtest import TestApp

import seckf.db_tools as db_tools
from seckf.app import create_app
from seckf.database import db as _db
from seckf.database.privileges import Privilege
from seckf.database.users import User
from tests import settings


@pytest.fixture
def app():
    """Create application for the tests."""
    _app = create_app(settings)
    _app.logger.setLevel(logging.CRITICAL)
    ctx = _app.test_request_context()
    ctx.push()
    if settings.REGENERATE_DATABASE:
        initialize_database()

    yield _app

    ctx.pop()


@pytest.fixture
def testapp(app):
    """Create Webtest app."""
    return TestApp(app)


@pytest.fixture
def db(app):
    """Create database for the tests."""
    _db.app = app
    with app.app_context():
        if settings.REGENERATE_DATABASE:
            initialize_database()

    yield _db

    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()


def initialize_database():
    """Create database for the tests."""
    db_tools.clean_db(_db)
    try:
        p = Privilege('edit:read:manage:delete')
        _db.session.add(p)
        _db.session.add(Privilege('edit:read:delete'))
        _db.session.add(Privilege('edit:read'))
        _db.session.add(Privilege('read'))

        user = User(username='testadmin', accessToken=12345, email="test-example@owasp.org", activated=True,
                    password="$2b$04$fE268V4i6uPiJP3npOcJmuv0aTniLP4raRhPkaAVv2Kf2TzwuLp.q", access=True)
        user.privilege = p
        _db.session.add(user)
        _db.session.commit()
    except Exception as e:
        _db.session.rollback()
        raise
