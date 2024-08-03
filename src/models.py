from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime

Base = declarative_base()


class TowerModel(Base):
    __tablename__ = "towers_table"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tower_id = Column(String, unique=True, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)

    kpis = relationship("KPIModel", back_populates="tower")


class KPIModel(Base):
    __tablename__ = "kpi_table"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tower_id = Column(String, ForeignKey("towers_table.tower_id"), nullable=False)
    layer = Column(Integer, nullable=False)
    timestamp = Column(DateTime, unique=True, nullable=False)
    rsrp = Column(Float, nullable=False)
    rsrq = Column(Float, nullable=False)
    cqi = Column(Integer, nullable=False)
    latency = Column(Float, nullable=False)
    packet_loss = Column(Float, nullable=False)
    throughput = Column(Float, nullable=False)
    bandwidth_usage = Column(Float, nullable=False)
    simultaneous_connections = Column(Integer, nullable=False)
    uptime = Column(Float, nullable=False)
    downtime = Column(Float, nullable=False)
    failures = Column(Integer, nullable=False)
    mttr = Column(Float, nullable=False)
    preventive_maintenance = Column(Integer, nullable=False)
    data_traffic = Column(Float, nullable=False)
    voice_traffic = Column(Float, nullable=False)
    energy_consumption = Column(Float, nullable=False)
    total_call_volume = Column(Integer, nullable=False)
    successful_calls = Column(Integer, nullable=False)
    failed_calls = Column(Integer, nullable=False)

    tower = relationship("TowerModel", back_populates="kpis")
