# (C) Andrew Glushchenko 2020
# REST API project v0.1
# Data models module
#
from . import db, session, Base
from sqlalchemy.orm import relationship
from flask_jwt_extended import create_access_token
from datetime import timedelta
from passlib.hash import bcrypt


class NW_Elements(Base):
    __tablename__ = 'elements'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    ip_address = db.Column(db.String(15), nullable=False)
    name = db.Column(db.String(80),nullable=False)
    description = db.Column(db.String(500),nullable=False)

    @classmethod
    def getElementList(cls, user_id):
        try:
            elements = cls.query.filter(cls.user_id == user_id).all()
            session.commit()
        except Exception:
            session.rollback()
            raise
        return elements
    pass

    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exception:
            session.rollback()
            raise
    pass

    @classmethod
    def get(cls, element_id, user_id):
        element = cls.query.filter(cls.id == element_id, cls.user_id == user_id).first()
        try:
            if not element:
                raise Exception('No element with this id')
        except Exception:
            session.rollback()
            raise
        return element
    pass

    def update(self, **kwargs):
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
            session.commit()
        except Exception:
            session.rollback()
            raise
    pass


    def delete(self):
        try:
            session.delete(self)
            session.commit()
        except Exception:
            session.rollback()
            raise
    pass



class User(Base):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    elements = relationship('NW_Elements', backref='user', lazy=True)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.email = kwargs.get('email')
        self.password = bcrypt.hash(kwargs.get('password'))
    pass

    def get_token(self, expire_time=24):
        expire_delta = timedelta(expire_time)
        token = create_access_token(
            identity=self.id, expires_delta=expire_delta)
        return token
    pass

    @classmethod
    def authenticate(cls, email, password):
        user = cls.query.filter(cls.email == email).one()
        if not bcrypt.verify(password, user.password):
            raise Exception('No user with this password')
        return user
    pass


def AddElements(id_el, id_us,  addr, name_el, decsr=''):
    v1 = NW_Elements(id=id_el, user_id=id_us, ip_address=addr, name=name_el, description=decsr)
    v1.save()
