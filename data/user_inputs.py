import datetime
import sqlalchemy
# from .db_session import *
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase
from sqlalchemy import orm

class User_inputs(SqlAlchemyBase, UserMixin):
    __tablename__ = 'user_inputs'

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("user_login.id"),
                                primary_key=True, autoincrement=True, nullable=True)

    height = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    weight = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    # age = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    # gender = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)


    user_login = orm.relation('User_login')


