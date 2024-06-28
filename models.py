from sqlalchemy import Column, String, Integer, Text
import sqlalchemy as sql
import datetime as _dt
import sqlalchemy.orm as orm
import passlib.hash as _hash
from config import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(120), unique=True, nullable=False)
    name = Column(String(120), nullable=True)
    hashed_password = Column(String(60), nullable=False)  # Adjusted length for bcrypt
    date_created = sql.Column(sql.DateTime(timezone=True), default=_dt.datetime.utcnow)
    products = orm.relationship("Product", back_populates="owner")

    def verify_password(self, password: str):
        return _hash.bcrypt.verify(password, self.hashed_password)


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    owner_id = Column(Integer, sql.ForeignKey("users.id"))
    title = Column(String(120), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Integer, nullable=False)
    owner = orm.relationship("User", back_populates="products")
