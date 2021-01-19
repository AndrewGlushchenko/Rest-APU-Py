# (C) Andrew Glushchenko 2020
# REST API project v0.1
# Config module
#
import os
#import json


class Config:
    SECRET_KEY = "055375b7e1524fd4a41ee4196c6734cd"
    CORS_ALOWED_LIST = ['http://localhost:8080']
#    SECRET_KEY = os.environ.get('SECRET_KEY')
#    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
