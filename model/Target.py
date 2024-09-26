from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from config.base import Base

class Target(Base):
    __tablename__ = 'target'

    target_id = Column(Integer, primary_key=True, autoincrement=True)
    target_priority = Column(String(5))
    latitude = Column(Numeric(10, 6))
    longitude = Column(Numeric(10, 6))

    # Foreign Keys
    city_id = Column(Integer, ForeignKey('city.city_id'))
    target_type_id = Column(Integer, ForeignKey('target_type.target_type_id'))
    industry_id = Column(Integer, ForeignKey('target_industry.industry_id'))
    # Relationships
    city = relationship('City', back_populates='targets')
    target_type = relationship('TargetType', back_populates='targets')
    industry = relationship('TargetIndustry', back_populates='targets')


