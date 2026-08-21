
from sqlalchemy import Column, Integer, String, Date, DateTime, func
from app.database import Base


class Animal(Base):
    __tablename__ = "animales"

    id = Column(Integer, primary_key=True, index=True)
    tag = Column(String(50), unique=True, index=True, nullable=False)
    birth_date = Column(Date, nullable=True)
    sex = Column(String(10), nullable=True)
    breed = Column(String(50), nullable=True)
    status = Column(String(20), nullable=False, default="active")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
