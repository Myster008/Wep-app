from sqlalchemy import Column, Integer, String, DateTime, func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)  # Telegram ID
    name = Column(String)
    purchases = Column(Integer, default=0)
    current_island = Column(Integer, default=0)
    last_purchase_date = Column(DateTime, nullable=True)
    status = Column(String, default="active")  # active, sunk, finished

class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    amount = Column(Integer)
    date = Column(DateTime, default=func.now())

class Reward(Base):
    __tablename__ = "rewards"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    reward_type = Column(String)  # Damas, Cobalt
    date = Column(DateTime, default=func.now())

class Reward(Base):
    __tablename__ = "rewards"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    reward_type = Column(String)
    date = Column(DateTime, default=func.now())
