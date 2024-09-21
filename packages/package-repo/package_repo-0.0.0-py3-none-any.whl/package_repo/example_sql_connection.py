"""Create a fully implemented sql connection engine."""

import os
import struct

from azure.identity import DefaultAzureCredential
from sqlalchemy import Engine, create_engine
from sqlalchemy.engine import URL


def create_connection_engine() -> Engine:
    """Create a fully implemented sql connection engine."""
    credentials = os.getenv("URL_AZURECLICREDENTIALTOKEN")
    tsql_driver = os.getenv("TRANSACTSQLDRIVER")
    tsql_server = os.getenv("TRANSACTSQLSERVER")
    tsql_database = os.getenv("TRANSACTSQLDATABASE")
    tsql_access_token = int(os.getenv("TRANSACTSQLACCESSTOKEN"))

    credential = DefaultAzureCredential()
    databaseToken = credential.get_token(credentials)
    token_bytes = bytes(databaseToken[0], "UTF-8")
    exptoken = b"\x00".join(bytes({i}) for i in token_bytes) + b"\x00"
    tokenstruct = struct.pack("=i", len(exptoken)) + exptoken

    connString = f"Driver={tsql_driver};Server={tsql_server};Database={tsql_database}"
    args_con = {"attrs_before": {tsql_access_token: tokenstruct}}
    connUrl = URL.create("mssql+pyodbc", query={"odbc_connect": connString})

    engine = create_engine(connUrl, connect_args=args_con)
    return engine
