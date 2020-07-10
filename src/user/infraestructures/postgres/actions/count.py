# Develop: Vmgabriel

# Libraries
from typing import List, TypeVar, Generic, Any, Tuple

# Interfaces
from domain.models.actions.count import Count
from domain.models.db_connection import Db_Connection

# Configuration Data
from config.server import configuration as conf

class Count_User(Count):
    def __init__(self, name_table: str, database: Db_Connection):
        self.name_table = name_table
        self.schema = conf['db_name_schema']
        self.__database = database

    def query_definition(self, data: str) -> str:
        if (data == 'all'):
            return 'SELECT COUNT(*) FROM {}.{}'.format(self.schema, self.name_table)
        else:
            return data

    def execute(self, query: str) -> int:
        proc = self.query_definition(query)
        cursor = self.__database.get_cursor()
        cursor.execute(proc)
        data = cursor.fetchone()
        return data[0]

