from sqlalchemy import Column, Integer, String, Sequence, DateTime, ForeignKey
import datetime
from sqlalchemy.orm import relationship
from database import connector

class Tweet(connector.Manager.Base):
    __tablename__='tweet'
    id = Column(String(22),primary_key=True)
    date =Column(DateTime)
    text =Column(String(300))
