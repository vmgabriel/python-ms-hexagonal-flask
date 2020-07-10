# Develop vmgabriel

# Libraries
import inject
import psycopg2
from typing import List, TypeVar, Generic, Any, Tuple

# Interfaces
from domain.models.actions.get_all import Get_All
from domain.models.db_connection import Db_Connection
from user.domain.user import User

# Configuration
from config.server import configuration as conf

class Get_All_User(Get_All[User]):
    def __init__(self, name_table: str, database: Db_Connection):
        self.__database = database
        self.query = 'SELECT * FROM {}.{};'.format(conf['db_name_schema'], name_table);

    def minimize_str(self, data: List[Any]):
        minimize = lambda x: x.strip() if (type(x) == str) else x
        if (len(data) == 1):
            return [minimize(data[0])]
        return [minimize(data[0])] + self.minimize_str(data[1:])

    def execute(
            self,
            limit: int,
            offset: int
    ) -> List[User]:
        cursor = self.__database.get_cursor()
        cursor.execute(self.query)
        rows = cursor.fetchall()
        rows = list(map(self.minimize_str, rows))
        return [User(*row) for row in rows]
