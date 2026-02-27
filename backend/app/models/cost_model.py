from sqlalchemy import Column, Integer, Float, String, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Cost(Base):
    __tablename__ = "costs"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, nullable=False)
    total_cost = Column(Float, nullable=False)
    anomaly = Column(Boolean, default=False)