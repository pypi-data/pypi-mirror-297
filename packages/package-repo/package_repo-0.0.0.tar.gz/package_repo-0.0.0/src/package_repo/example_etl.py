"""This file contains an example of an ETL-operation on the Bag AO dataset."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import pandas as pd

if TYPE_CHECKING:
    from sqlalchemy import Connection

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def bag_ao_etl(sql_connection: Connection) -> None:
    """Execute an ETL-operation on the BAG AO dataset.

    Uses a generic sql-connection.
    """
    dataset = extract(sql_connection=sql_connection)
    dataset = transform(dataset)
    load(dataset)


def extract(sql_connection: Connection) -> pd.DataFrame:
    """Extract the BAG AO dataset."""
    sql = "SELECT * FROM [Current].[LVBAG2_0_ADRES]"
    dtpye_dict = {
        "openbare_ruimte_id": str,
        "nummeraanduiding_id": str,
        "woonplaats_id": str,
        "naam_van_openbare_ruimte": str,
        "huisnummer": float,
        "postcode": str,
        "huisletter": str,
        "huisnummertoevoeging": str,
        "begin_geldigheid": str,
        "eind_geldigheid": str,
        "current_indicator": int,
    }
    dataset = pd.DataFrame()
    for connection_attempt in range(1, 6):
        try:
            dataset = pd.read_sql(sql=sql, con=sql_connection, dtype=dtpye_dict)

            if dataset is None or len(dataset) == 0:
                continue

            return dataset

        except Exception as error:
            errormsg = f"An error occured during attempt {connection_attempt}: {error!r}"
            logger.warning(errormsg)
            continue

    errormsg = f"Failed to load data rows for {sql}"
    logger.error(errormsg)
    raise Exception(errormsg)


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Transform the dataset."""
    # Verwijder duplicate nummers
    df = df.drop_duplicates(subset="nummeraanduiding_id", keep="last")

    # Geldigheid altijd in de toekomst
    now = pd.Timestamp("today")
    df["begin_geldigheid"] = pd.to_datetime(df["begin_geldigheid"])
    df["eind_geldigheid"] = pd.to_datetime(df["eind_geldigheid"], errors="coerce")
    mask = df["begin_geldigheid"].notna()
    mask &= df["begin_geldigheid"] < now
    mask &= df["eind_geldigheid"].isna() | (df["eind_geldigheid"] > now)
    df = df[mask]

    # Geldig huisnummer
    df = df[df["huisnummer"].notna()]
    df = df.astype({"huisnummer": int})

    return df


def load(df: pd.DataFrame) -> None:
    """Load the dataset to the target.

    Throws an exception if the dataset is empty.
    """
    if len(df) == 0:
        errormsg = "Mayday! We have found an empty database."
        raise Exception(errormsg)
    logger.info("Dataframe is now ready to be loaded!")


if __name__ == "__main__":
    # Do not import this from the head of the file
    # A reference to a production sql-connection(/engine) should not be made unless necesarry
    # For example, unit tests will fail when this import is made.
    # Ideally, such a reference should be imported from within the project_repo application
    # For sake of the example, this will suffice.
    from dotenv import find_dotenv, load_dotenv
    from example_sql_connection import create_connection_engine

    load_dotenv(find_dotenv())

    sql_engine = create_connection_engine()

    with sql_engine.connect() as sql_connection:
        bag_ao_etl(sql_connection=sql_connection)
