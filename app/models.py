from sqlalchemy import Column, Integer, String, Float, JSON
from app.database import Base

class Athlete(Base):
    __tablename__ = "athletes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String)
    age = Column(Integer)
    country = Column(String)
    achievements = Column(JSON, default=[])  # Guardará tu lista de strings
    records = Column(JSON, default=[])       # Guardará tu lista de objetos Lift