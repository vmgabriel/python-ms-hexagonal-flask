# Develop: vmgabriel

# Libraries
from typing import TypeVar, Generic, Any, List

# Structures
from user.domain.user import User

# Interfaces
from domain.models.actions.get_one import Get_One
from domain.models.db_connection import Db_Connection
from domain.models.db.entity_conversor import Conversor_Type

# Configuration
from config.server import configuration as conf

class Get_One_User(Get_One[User]):
    def __init__(self, name_table: str, database: Db_Connection):
        self.__database = database

        self.query = 'SELECT * FROM {}.{}'.format(conf['db_name_schema'], name_table);
        self.minimize = lambda x: x.strip() if (type(x) == str) else x

    def minimize_str(self, data: List[Any]):
        if (len(data) == 1):
            return [self.minimize(data[0])]
        return [self.minimize(data[0])] + self.minimize_str(data[1:])

    def execute(self, id: int) -> User:
        query_data = self.query + self.to_query(id)
        print('query_data - {}'.format(query_data))

        cursor = self.__database.get_cursor()
        cursor.execute(query_data)
        get_user = cursor.fetchone()
        cursor.close()

        print('get_user - {}'.format(get_user))
        if not (get_user):
            return None

        get_user = self.minimize_str(get_user)
        return User(*get_user)


    def to_query(self, data: int) -> str:
        user_temp = User(0,0,0,0,0,0,0,0,0)
        return ' WHERE {} = {} AND {} = TRUE;'.format(user_temp.id_name(), data, user_temp.validation_name())
