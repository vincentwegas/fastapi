from passlib.utils.compat import bascii_to_str
from pydantic.main import BaseModel
from sqlalchemy.orm import relation, relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP, Boolean, Integer
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean 
from sqlalchemy.sql.expression import null, text

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key= True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="True",nullable=False )
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    #SQLalchemy Relationship update schema as well
    owner = relationship("User")


class User(Base):
    __tablename__ ="users"

    id = Column(Integer, primary_key= True, nullable=False)
    email = Column(String, nullable=False, unique=True )
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    phone_number = Column(String)
    #alembic revision --autogenerate -m "add Phone Number"


class Vote(Base):
    __tablename__ ="votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
