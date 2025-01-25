from pydantic import BaseModel
from datetime import datetime


class TowerSchema(BaseModel):
    tower_id: str
    latitude: float
    longitude: float
    city: str
    state: str


class KPISchema(BaseModel):
    tower_id: str
    layer: int
    timestamp: datetime
    rsrp: float
    rsrq: float
    cqi: int
    latency: float
    packet_loss: float
    throughput: float
    bandwidth_usage: float
    simultaneous_connections: int
    uptime: float
    downtime: float
    failures: int
    mttr: float
    preventive_maintenance: int
    data_traffic: float
    voice_traffic: float
    energy_consumption: float
    total_call_volume: int
    successful_calls: int
    failed_calls: int
