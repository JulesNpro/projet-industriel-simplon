from sqlalchemy import Column, Integer, Float, String, Text
from sqlalchemy.orm import declarative_base

# Base de déclaration pour les modèles
Base = declarative_base()

class Datasasia(Base):
    __tablename__ = "losdatas"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    datetime = Column("Datetime", String(512), nullable=False)
    temperature = Column("Temperature", Float, nullable=False)
    humidity = Column("Humidity", Float, nullable=False)
    windspeed = Column("WindSpeed", Float, nullable=False)
    general_diffuse_flows = Column("GeneralDiffuseFlows", Float, nullable=False)
    diffuse_flows = Column("DiffuseFlows", Float, nullable=False)
    power_consumption_zone1 = Column("PowerConsumption_Zone1", Float, nullable=False)
    power_consumption_zone2 = Column("PowerConsumption_Zone2", Float, nullable=False)
    power_consumption_zone3 = Column("PowerConsumption_Zone3", Float, nullable=False)
