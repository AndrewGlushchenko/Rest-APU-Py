from flask import Flask, jsonify, request
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from flask_jwt_extended import JWTManager
from .config import Config
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec import APISpec
from flask_apispec.extension import FlaskApiSpec
import logging
from flask_cors import CORS

print("KEY:", Config.SECRET_KEY)

app = Flask(__name__)
app.config.from_object(Config)

client = app.test_client()

engine = create_engine('sqlite:///db/db.sqlite')
#engine = Config.SQLALCHEMY_DATABASE_URI


session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()

jwt = JWTManager()

docs = FlaskApiSpec()

cors = CORS(resources={
    r"/*":{"origins":"*"}
#    r"/*":{"origins": Config.CORS_ALOWED_LIST}
})


app.config.update({
    'APISPEC_SPEC': APISpec(
        title='netelements',
        version='v1',
        openapi_version='2.0',
        plugins=[MarshmallowPlugin()]
    ),
    'APISPEC_SWAGGER_URL':'/swagger/'
})


from .models import *


Base.metadata.create_all(bind=engine)


def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
    file_handler = logging.FileHandler('log/api.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


logger = setup_logger()


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()
    logger.warning(f'Close server.')


from .main.views import elements
from .users.views import users


app.register_blueprint(elements)
app.register_blueprint(users)

docs.init_app(app)
jwt.init_app(app)
