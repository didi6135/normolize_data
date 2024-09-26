from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from config.base import Base

class TargetIndustry(Base):
    __tablename__ = 'target_industry'

    industry_id = Column(Integer, primary_key=True, autoincrement=True)
    industry = Column(String(255), unique=True)

    targets = relationship('Target', back_populates='industry')

