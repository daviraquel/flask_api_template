#dataclass decorator for parsing model
from dataclasses import dataclass

# import need typing from sqlalchemy: Integer, String, etc
from sqlalchemy import (  
    Column,
    DateTime,
    Numeric,
    Integer,
    String,
)

#import sqlalchemy relation functions if needed
from sqlalchemy.orm import backref, relationship

#datetime for registering creation date
from datetime import datetime

#password utilitites from wekzeug
from werkzeug.security import check_password_hash, generate_password_hash
from app.configs.database import db

# import outher related models
# from app.models.another_model import AnotherModel

@dataclass
class UsersModel(db.Model):
    #these are the types for dataclass
    id: int
    user_name: str
    email: str
    balance: float
    create_date: str
    update_date: str

    #creating date object
    now = datetime.utcnow

    #declaring table name
    __tablename__ = "users"

    #adding columns to the table
    id = Column(Integer, primary_key=True)
    user_name = Column(String(50), nullable=False, unique=True)
    email = Column(String(50), nullable=False, unique=True)
    password_hash = Column(String(511), nullable=False)
    balance = Column(Numeric, default=0)
    create_date = Column(DateTime, default=now)
    update_date = Column(DateTime, default=now)

    # add relationships when needed
    # another = relationship("AnotherModel",backref(...))

    #defining password getter so it can't be accessed
    @property
    def password(self):
        raise AttributeError("can't access password")

    #defining password setter for hashed password
    @password.setter
    def password(self, password_to_hash):
        self.password_hash = generate_password_hash(password_to_hash)

    #special method for checking password from requests
    def check_password(self, password_to_compare):
        return check_password_hash(self.password_hash, password_to_compare)
