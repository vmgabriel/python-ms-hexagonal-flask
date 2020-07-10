# Develop: vmgabriel

# Libraries
import datetime
from typing import List, Any

# Structures
from user.domain.user import User

# Interfaces
from domain.models.actions.delete import Delete
from domain.models.db_connection import Db_Connection
from domain.models.db.entity_conversor import Conversor_Type

# Configuration
from config.server import configuration as conf

class Delete_User(Delete[User]):
    def __init__(self, name_table: str, connection: Db_Connection, conversor: Conversor_Type):
        self.name_table = name_table
        self.__database = connection
        self.conversor = conversor

        self.query = 'UPDATE {}.{} SET '.format(conf['db_name_schema'], name_table)
        self.minimize = lambda x: x.strip() if (type(x) == str) else x

    def minimize_str(self, data: List[Any]):
        if (len(data) == 1):
            return [self.minimize(data[0])]
        return [self.minimize(data[0])] + self.minimize_str(data[1:])

    def execute(self, id: int) -> User:
        query_data = self.query + self.to_query(id)

        cursor = self.__database.get_cursor()
        cursor.execute(query_data)
        deleted_user = cursor.fetchone()
        self.__database.get_connection().commit()
        cursor.close()

        deleted_user = self.minimize_str(deleted_user)
        return User(*deleted_user)

    def to_query(self, id: int) -> str:
        user_temp = User(0,0,0,0,0,0,0,0,0)
        query = '{}=FALSE, {}={} WHERE {}={} RETURNING *;'.format(
            user_temp.validation_name(),
            user_temp.delete_date_name(),
            self.conversor.to_entity(
                user_temp.define_type(user_temp.delete_date_name()),
                datetime.datetime.now()
            ),
            user_temp.id_name(),
            id
        )
        return query
