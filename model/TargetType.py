from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from config.base import Base

class TargetType(Base):
    __tablename__ = 'target_type'

    target_type_id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(100), unique=True)

    targets = relationship('Target', back_populates='target_type')
