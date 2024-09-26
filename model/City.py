from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from config.base import Base

class City(Base):
    __tablename__ = 'city'

    city_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    country_id = Column(Integer, ForeignKey('country.country_id'))

    country = relationship('Country', back_populates='cities')

    targets = relationship('Target', back_populates='city')
