# Develop: vmgabriel

# Structures
from typing import List, Any
from user.domain.user import User

# Interfaces
from domain.models.actions.update import Update
from domain.models.db_connection import Db_Connection
from domain.models.db.entity_conversor import Conversor_Type

# Configuration
from config.server import configuration as conf

class Update_User(Update[User]):
    def __init__(self, name_table: str, database: Db_Connection, conversor: Conversor_Type):
        self.__database = database
        self.conversor = conversor
        self.query = 'UPDATE {}.{} SET '.format(conf['db_name_schema'], name_table)
        self.minimize = lambda x: x.strip() if (type(x) == str) else x

    def minimize_str(self, data: List[Any]):
        if (len(data) == 1):
            return [self.minimize(data[0])]
        return [self.minimize(data[0])] + self.minimize_str(data[1:])

    def execute(self, data: User, id: int) -> User:
        query_data = self.query + self.to_query(data, id)

        cursor = self.__database.get_cursor()
        cursor.execute(query_data)
        updated_user = cursor.fetchone()
        self.__database.get_connection().commit()
        cursor.close()

        updated_user = self.minimize_str(updated_user)
        return User(*updated_user)

    def to_entity(self, data: User) -> str:
        datas = str(data)
        query = ''

        for i in datas.split(','):
            temp = data.to_dict().get(i.strip())
            if (temp):
                type_data = data.define_type(i.strip())
                query += '{} = {},'.format(i.strip(), self.conversor.to_entity(type_data, temp))

        query = query[:-1]
        return query

    def to_query(self, data: User, id: int) -> str:
        definitions = self.to_entity(data)
        user_temp = User(0,0,0,0,0,0,0,0,0)
        query = '{} WHERE {}={} RETURNING *;'.format(definitions, user_temp.id_name(), id)
        return query
