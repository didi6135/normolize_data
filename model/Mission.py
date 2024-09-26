from sqlalchemy import Column, Integer, Date, String, ForeignKey
from sqlalchemy.orm import relationship
from config.base import Base

# class Mission(Base):
#     __tablename__ = 'mission'
#
#     mission_id = Column(Integer, primary_key=True)
#     mission_date = Column(Date)
#     air_force = Column(String(100))
#

from sqlalchemy import Integer, Column, Date, String, Numeric
from config.base import Base

class Mission(Base):
    __tablename__ = 'mission'

    mission_id = Column(Integer, primary_key=True)
    mission_date = Column(Date)
    theater_of_operations = Column(String(100))
    air_force = Column(String(100))
    mission_type = Column(String(100))
    target_country = Column(String(100))
    target_city = Column(String(100))
    target_type = Column(String(100))
    airborne_aircraft = Column(Integer)
    bomb_damage_assessment = Column(String(255))

    def __repr__(self):
        return f"<Mission(id={self.mission_id}, date={self.mission_date}, theater={self.theater_of_operations}, air_force={self.air_force})>"
