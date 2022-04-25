import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from db_utils.db_session import SqlAlchemyBase


class UsersToken(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'users_tokens'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    token_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('tokens.id'))
    user = orm.relation('User')
    token = orm.relation('Token')

