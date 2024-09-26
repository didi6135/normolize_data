from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from config.base import Base


class Country(Base):
    __tablename__ = 'country'

    country_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True)

    cities = relationship('City', back_populates='country')