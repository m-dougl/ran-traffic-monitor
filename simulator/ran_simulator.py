"""
Synthetic data generator module for telecommunications towers and their KPIs.

This module includes two main classes: `TowerDataGenerator` and `KPIDataGenerator`.
The `TowerDataGenerator` class generates synthetic data for telecommunications towers,
including site names, geographic coordinates, and city/state information.
The `KPIDataGenerator` class generates synthetic data for KPIs related to telecommunications towers.

The provided code demonstrates the usage of these classes by creating instances of the classes, generating synthetic data for towers and KPIs, and saving the generated data to CSV files.
"""

import random
import pandas as pd 

from datetime import datetime, timedelta
from dataclasses import dataclass
from faker import Faker

class TowerDataGenerator:
    """
    Telecom tower infos generator
    """
    
    def __init__(self, n_towers: int)-> None:
        """
        Tower constructor.
        
        Args:
            n_towers (int): Number of towers to generate.
        """
        self.n_towers = n_towers
        self.faker = Faker()
        
    def _generate_tower_id(self) -> list:
        """
        Generate tower id
        
        Returns:
            list: List with all towers ids.
        """
        return [f"tower_{i + 1}" for i in range(self.n_towers)]
    
    def _generate_locations(self, country_code: str = 'BR') -> tuple:
        """
        Generate geographic data for each tower.
        
        Args:
            country_code (str, optional): Code for the country. Defaults to 'BR'.
        
        Returns:
            latitudes (list): List with all latitudes.
            longitudes (list): List with all longitudes.
            cities (list): List with all cities.
            states (list): List with all states.
        """
        
        locations = set()
        latitudes, longitudes, cities, states = [], [], [], []
        
        while len(locations) < self.n_towers:
            lat, lng, city,_ , state = self.faker.local_latlng(country_code=country_code)
        
            if (lat, lng) not in locations:
                locations.add(lat, lng)
                latitudes.append(lat)
                longitudes.append(lng)
                cities.append(city)
                states.append(state)
        return latitudes, longitudes, cities, states
    
    def generate_towers(self) -> pd.DataFrame:
        """
        Generate synthetic data for telecom towers.
        
        Returns:
            df (pd.DataFrame): Dataframe with all generated towers.
        """
        towers_ids = self._generate_tower_id()
        latitudes, longitudes, cities, states = self._generate_locations()
        
        df = pd.DataFrame(
            {
                'tower_id': towers_ids,
                'latitude': latitudes,
                'longitude': longitudes,
                'city': cities,
                'state': states 
            }
        )
        
        return df 
    
@dataclass
class TelecomKPI:
    """
    All KPIs to generate.

    Attributes:
    tower_id: str
        Identifier of the telecommunications tower site.
    layer: int
        Layer of the telecommunications tower site.
    timestamp: datetime
        Timestamp of the KPI data.
    rsrp: float
        Received Signal Strength Power (RSRP) in dBm.
    rsrq: float
        Received Signal Quality Measure (RSRQ) in dB.
    cqi: int
        Channel Quality Indicator (CQI) value.
    latency: float
        Latency in milliseconds.
    packet_loss: float
        Packet loss percentage.
    throughput: float
        Throughput in Mbps.
    bandwidth_usage: float
        Bandwidth usage in Mbps.
    simultaneous_connections: int
        Number of simultaneous connections.
    uptime: float
        Uptime percentage.
    downtime: float
        Downtime percentage.
    failures: int
        Number of failures.
    mttr: float
        Mean Time to Repair (MTTR) in hours.
    preventive_maintenance: int
        Number of preventive maintenance actions.
    data_traffic: float
        Data traffic in GB.
    voice_traffic: float
        Voice traffic in minutes.
    energy_consumption: float
        Energy consumption in kWh.
    total_call_volume: int
        Total call volume.
    successful_calls: int
        Number of successful calls.
    failed_calls: int
        Number of failed calls.
    """

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


class KPIDataGenerator:
    def generate_layer(self):
        return random.choice([700, 1800, 2600])

    def generate_rsrp(self):
        return round(random.uniform(-120, -70), 2)

    def generate_rsrq(self):
        return round(random.uniform(-20, -3), 2)

    def generate_cqi(self, rsrp, rsrq):
        return min(max(int((rsrp + 140) / 10 + (20 + rsrq) / 2), 1), 15)

    def generate_latency(self, rsrp):
        if rsrp > -70:
            return round(random.uniform(10, 30), 2)
        elif rsrp > -85:
            return round(random.uniform(30, 60), 2)
        else:
            return round(random.uniform(60, 100), 2)

    def generate_packet_loss(self, latency):
        if latency < 30:
            return round(random.uniform(0, 1), 2)
        elif latency < 60:
            return round(random.uniform(1, 3), 2)
        else:
            return round(random.uniform(3, 5), 2)

    def generate_throughput(self, latency):
        if latency < 30:
            return round(random.uniform(50, 300), 2)
        elif latency < 60:
            return round(random.uniform(20, 150), 2)
        else:
            return round(random.uniform(10, 50), 2)

    def generate_bandwidth_usage(self, throughput):
        return round(throughput * random.uniform(0.8, 1.2), 2)

    def generate_simultaneous_connections(self):
        return random.randint(100, 1000)

    def generate_uptime(self):
        return round(random.uniform(99.5, 100), 2)

    def generate_downtime(self, uptime):
        return round(100 - uptime, 2)

    def generate_failures(self, uptime):
        if uptime >= 99.9:
            return random.randint(0, 1)
        elif uptime >= 99.7:
            return random.randint(1, 2)
        else:
            return random.randint(2, 3)

    def generate_mttr(self):
        return round(random.uniform(1, 4), 2)

    def generate_preventive_maintenance(self):
        return random.randint(0, 2)

    def generate_data_traffic(self):
        return round(random.uniform(50, 500), 2)

    def generate_voice_traffic(self):
        return round(random.uniform(1000, 10000), 2)

    def generate_energy_consumption(self):
        return round(random.uniform(1000, 5000), 2)

    def generate_total_call_volume(self):
        return random.randint(100, 1000)

    def generate_successful_calls(self, total_call_volume):
        return random.randint(int(total_call_volume * 0.8), total_call_volume)

    def generate_failed_calls(self, total_call_volume, successful_calls):
        return total_call_volume - successful_calls

    def generate_kpi_record(self, tower_id) -> TelecomKPI:

        layer = self.generate_layer()
        timestamp = datetime.now() - timedelta(minutes=random.randint(0, 60))
        rsrp = self.generate_rsrp()
        rsrq = self.generate_rsrq()
        cqi = self.generate_cqi(rsrp, rsrq)
        latency = self.generate_latency(rsrp)
        packet_loss = self.generate_packet_loss(latency)
        throughput = self.generate_throughput(latency)
        bandwidth_usage = self.generate_bandwidth_usage(throughput)
        simultaneous_connections = self.generate_simultaneous_connections()
        uptime = self.generate_uptime()
        downtime = self.generate_downtime(uptime)
        failures = self.generate_failures(uptime)
        mttr = self.generate_mttr()
        preventive_maintenance = self.generate_preventive_maintenance()
        data_traffic = self.generate_data_traffic()
        voice_traffic = self.generate_voice_traffic()
        energy_consumption = self.generate_energy_consumption()
        total_call_volume = self.generate_total_call_volume()
        successful_calls = self.generate_successful_calls(total_call_volume)
        failed_calls = self.generate_failed_calls(total_call_volume, successful_calls)

        return TelecomKPI(
            tower_id,
            layer,
            timestamp,
            rsrp,
            rsrq,
            cqi,
            latency,
            packet_loss,
            throughput,
            bandwidth_usage,
            simultaneous_connections,
            uptime,
            downtime,
            failures,
            mttr,
            preventive_maintenance,
            data_traffic,
            voice_traffic,
            energy_consumption,
            total_call_volume,
            successful_calls,
            failed_calls,
        )

    def generate_kpis_data_for_site(self, site_name, n_records):
        records = [self.generate_kpi_record(site_name) for _ in range(n_records)]
        return pd.DataFrame([record.__dict__ for record in records])

    def generate_kpis_data(self, tower_ids, n_records_per_site):
        all_kpis = pd.DataFrame()
        for tower_id in tower_ids:
            tower_kpis = self.generate_kpis_data_for_site(tower_id, n_records_per_site)
            all_kpis = pd.concat([all_kpis, tower_kpis], ignore_index=True)
        return all_kpis