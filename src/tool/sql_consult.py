import sqlite3
from pydantic.v1 import BaseModel
from typing import List
from langchain.tools import Tool

def get_connection():
    """Cria e retorna uma nova conexão SQLite."""
    return sqlite3.connect("./files/local.db")

def list_tables():
    """Lista todas as tabelas do banco de dados."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    rows = c.fetchall()
    conn.close()
    return "\n".join(row[0] for row in rows if row[0] is not None)

def run_sqlite_query(query: str):
    """Executa uma query no banco de dados SQLite."""
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute(query)
        result = c.fetchall()
    except sqlite3.OperationalError as err:
        result = f"The following error occurred: {str(err)}"
    finally:
        conn.close()
    return result

class RunQueryArgsSchema(BaseModel):
    query: str

run_query_tool = Tool.from_function(
    name="run_sqlite_query",
    description="Run a sqlite query.",
    func=run_sqlite_query,
    args_schema=RunQueryArgsSchema
)

def describe_tables(table_names: List[str]):
    """Retorna o schema das tabelas fornecidas."""
    conn = get_connection()
    c = conn.cursor()
    tables = ', '.join(f"'{table}'" for table in table_names)
    try:
        rows = c.execute(f"SELECT sql FROM sqlite_master WHERE type='table' and name IN ({tables});")
        result = '\n'.join(row[0] for row in rows if row[0] is not None)
    finally:
        conn.close()
    return result

class DescribeTablesArgsSchema(BaseModel):
    tables_names: List[str]

describe_tables_tool = Tool.from_function(
    name="describe_tables",
    description="Given a list of table names, returns the schema of those tables",
    func=describe_tables,
    args_schema=DescribeTablesArgsSchema
)
