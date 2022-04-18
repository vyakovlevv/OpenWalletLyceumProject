import datetime
import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from db_utils.db_session import SqlAlchemyBase
from flask_login import UserMixin


class User(SqlAlchemyBase, SerializerMixin, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    fingerprint = sqlalchemy.Column(sqlalchemy.String)
    mnemo = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    secured_code = sqlalchemy.Column(sqlalchemy.String)
