# Develop: vmgabriel

# Libraries
import inject
from typing import List, TypeVar, Generic, Any, Tuple

# Interfaces
from user.domain.user import User
from domain.models.db_connection import Db_Connection
from domain.models.db.entity_conversor import Conversor_Type

# Super Class
from domain.models.actions.create import Create

# Environment
from config.server import configuration as conf

class Create_User(Create[User]):
    def __init__(self, name_table: str, database: Db_Connection, conversor: Conversor_Type):
        self.conversor = conversor
        self.__database = database
        self.query = 'INSERT INTO {}.{} '.format(conf['db_name_schema'], name_table)

        self.minimize = lambda x: x.strip() if (type(x) == str) else x

    def minimize_str(self, data: List[Any]):
        if (len(data) == 1):
            return [self.minimize(data[0])]
        return [self.minimize(data[0])] + self.minimize_str(data[1:])

    def execute(self, data: User) -> User:
        query_data = self.query + self.to_query(data)

        cursor = self.__database.get_cursor()
        cursor.execute(query_data)
        new_user = cursor.fetchone()
        self.__database.get_connection().commit()
        cursor.close()

        new_user = self.minimize_str(new_user)
        return User(*new_user)

    def to_entity(self, data: User) -> (str, str):
        datas = str(data)
        query = definitions = ''

        for i in datas.split(','):
            temp = data.to_dict().get(i.strip())
            if (temp):
                type_data = data.define_type(i.strip())
                query += self.conversor.to_entity(type_data, temp)
                definitions += i.strip()
                query += ','
                definitions += ','

        query = query[:-1]
        definitions = definitions[:-1]
        return (query, definitions)

    def to_query(self, data: User) -> str:
        (datas, values) = self.to_entity(data)
        query = '({}) VALUES ({}) RETURNING *;'.format(values, datas)
        return query

