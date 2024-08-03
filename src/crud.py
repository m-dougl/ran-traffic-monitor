"""
This module provides functions for CRUD (creating, reading, updating, and deleting) data in a database.
"""

from database import get_session
from models import TowerModel, KPIModel
from schemas import TowerSchema, KPISchema
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from typing import Type, Union
import pandas as pd

ModelType = Union[TowerModel, KPIModel]
SchemaType = Union[TowerSchema, KPISchema]


def create_data(
    data: pd.DataFrame, model: Type[ModelType], schema: Type[SchemaType]
) -> None:
    """Create new data in the database."""
    with get_session() as session:
        try:
            for _, row in data.iterrows():
                val_data = schema(**row.to_dict())
                instance = model(**val_data.model_dump())
                session.add(instance)
            session.commit()
        except IntegrityError:
            print("This data already exists in the database")


def read_data(model: Type[ModelType]) -> pd.DataFrame:
    """Read data from the database."""
    with get_session() as session:
        result = session.execute(select(model)).scalars().all()
    data_dict = [
        {
            key: value
            for key, value in row.__dict__.items()
            if key != "_sa_instance_state"
        }
        for row in result
    ]
    return pd.DataFrame(data_dict)


def read_data_by_field(
    model: Type[ModelType], field_name: str, value: str
) -> pd.DataFrame:
    """Read data from the database based on a specific field."""
    with get_session() as session:
        result = (
            session.execute(select(model).where(getattr(model, field_name) == value))
            .scalars()
            .all()
        )
    data_dict = [
        {
            key: value
            for key, value in row.__dict__.items()
            if key != "_sa_instance_state"
        }
        for row in result
    ]
    return pd.DataFrame(data_dict)


def read_towers() -> pd.DataFrame:
    """Read tower data from the database."""
    return read_data(model=TowerModel)


def read_tower(tower_name: str) -> TowerModel:
    """Read a specific tower from the database."""
    with get_session() as session:
        result = session.execute(
            select(TowerModel).where(TowerModel.site_name == tower_name)
        ).first()
        return result[0] if result else None


def read_kpis() -> pd.DataFrame:
    """Read KPI data from the database."""
    return read_data(model=KPIModel)


def read_kpis_from_tower(tower_name: str) -> pd.DataFrame:
    """Read KPI data from a specific tower from the database."""
    return read_data_by_field(model=KPIModel, field_name="site_name", value=tower_name)


def update_data(model: Type[ModelType], identifier: dict, updates: dict):
    """Update data in the database."""
    with get_session() as session:
        result = session.execute(select(model).filter_by(**identifier)).first()
        if result:
            data = result[0]
            for key, value in updates.items():
                setattr(data, key, value)
            session.commit()


def update_tower(tower_name: str, updates: dict) -> None:
    """Update a specific tower in the database."""
    update_data(model=TowerModel, identifier={"site_name": tower_name}, updates=updates)


def delete_data(model: Type[ModelType], identifier: dict) -> None:
    """Delete data from the database."""
    with get_session() as session:
        result = session.execute(select(model).filter_by(**identifier)).first()
        if result:
            data = result[0]
            session.delete(data)
            session.commit()
        else:
            print(f"Record not found for {identifier} in {model.__name__}")


def delete_tower(tower_name: str) -> None:
    """Delete a specific tower from the database."""
    delete_data(model=TowerModel, identifier={"site_name": tower_name})


def delete_kpi_row(kpi_id: int) -> None:
    """Delete a specific KPI row from the database."""
    delete_data(model=KPIModel, identifier={"id": kpi_id})
