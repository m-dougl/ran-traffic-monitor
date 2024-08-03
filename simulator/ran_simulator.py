"""
Synthetic data generator module for telecommunications towers and their KPIs.

This module includes two main classes: `TowerDataGenerator` and `KPIDataGenerator`.
The `TowerDataGenerator` class generates synthetic data for telecommunications towers,
including site names, geographic coordinates, and city/state information.
The `KPIDataGenerator` class generates synthetic data for KPIs related to telecommunications towers.

The provided code demonstrates the usage of these classes by creating instances of the classes, generating synthetic data for towers and KPIs, and saving the generated data to CSV files.
"""

import random 
import os 
import pandas as pd 

from datetime import datetime, timedelta
from dataclasses import dataclass
from pathlib import Path 
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