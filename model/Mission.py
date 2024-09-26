from sqlalchemy import Column, Integer, Date, String, ForeignKey
from sqlalchemy.orm import relationship
from config.base import Base

class Mission(Base):
    __tablename__ = 'mission'

    mission_id = Column(Integer, primary_key=True)
    mission_date = Column(Date)
    air_force = Column(String(100))

    targets = relationship('Target', back_populates='mission')
