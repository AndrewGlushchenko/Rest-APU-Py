# (C) Andrew Glushchenko 2020
# REST API project v0.1
# Set of fixtures
#
import pytest
import sys

sys.path.append('..')

from api_rest_serv import app, Base, engine, session as db_session
from api_rest_serv.models import User

@pytest.yield_fixture(scope='function')
def test_app():
    _app = app

    Base.metadata.create_all(bind=engine)
    _app.connection = engine.connect()

    yield app

    Base.metadata.drop_all(bind=engine)
    _app.connection.close()


@pytest.yield_fixture(scope='function')
def session(test_app):
    ctx = app.app_context()
    ctx.push()

    yield db_session

    db_session.close_all()
    ctx.pop()


@pytest.yield_fixture(scope='function')
def user(session):
    user = User(
        name='tst23User',
        email='tst@23User.ru',
        password='123123'
    )
    session.add(user)
    session.commit()
    return user



