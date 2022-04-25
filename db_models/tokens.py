import datetime
import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from db_utils.db_session import SqlAlchemyBase


class Token(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'tokens'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    abbreviation = sqlalchemy.Column(sqlalchemy.String)
    full_name = sqlalchemy.Column(sqlalchemy.String)
    blockchain = sqlalchemy.Column(sqlalchemy.String, index=True)
    blockchain_gecko_id = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    contract_address = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    current_price = sqlalchemy.Column(sqlalchemy.Float, default=0)
    color = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    def update_current_price(self, new_price: int):
        self.current_price = new_price
