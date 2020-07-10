# Develop vmgabriel

# Libraries
from typing import List, TypeVar, Generic, Any, Tuple

# Models
from user.domain.user import User

# Interfaces
from domain.models.database_interface import Database_Interface
from domain.models.db_connection import Db_Connection
from domain.models.db.entity_conversor import Conversor_Type
from domain.models.filter_interface import Attribute_Filter, Filter_Interface

## Interfaces of Actions
from domain.models.actions.count import Count
from domain.models.actions.create import Create
from domain.models.actions.get_all import Get_All
from domain.models.actions.update import Update
from domain.models.actions.get_one import Get_One
from domain.models.actions.delete import Delete
from domain.models.actions.filter import Filter

# Connections
from utils.db.postgres.postgres import Postgres_Connection
from utils.db.postgres.postgres_type import Postgres_Type

# Actions
## Postgres
from user.infraestructures.postgres.actions.count import Count_User as Count_Postgres
from user.infraestructures.postgres.actions.get_all import Get_All_User as Get_All_Postgres
from user.infraestructures.postgres.actions.create import Create_User as Create_Postgres
from user.infraestructures.postgres.actions.get_one import Get_One_User as Get_One_Postgres
from user.infraestructures.postgres.actions.update import Update_User as Update_Postgres
from user.infraestructures.postgres.actions.delete import Delete_User as Delete_Postgres
from user.infraestructures.postgres.actions.filter import Filter_User as Filter_Postgres

## Mongo

## Schema

class Database_User(Database_Interface[User]):
    def __init__(self, type_data: str):
        self.name_table = 'tbl_user'
        self.connection: Db_Connection = None
        self.conversor: Conversor_Type = None

        self.get_all_user: Get_All = None
        self.count_user: Count = None
        self.create_user: Create = None
        self.get_one_user: Get_One = None
        self.update_user: Update = None
        self.delete_user: Delete = None
        self.filter_user: Filter = None

        self.builder(type_data)


    def count(self, query: str) -> int:
        return self.count_user.execute(query)


    def get_all(self, limit, offset) -> (List[User], int):
        return (self.get_all_user.execute(limit, offset), self.count('all'))


    def filter(
            self,
            filters: Filter_Interface,
            attributes: List[Attribute_Filter],
            joins: Any,
            limit: int,
            offset: int
    ) -> (List[User], int):
        (data, query_count) = self.filter_user.execute(
            filters,
            attributes,
            joins,
            limit,
            offset
        )
        return (data, self.count(query_count))


    def get_one(self, id: int) -> User:
        return self.get_one_user.execute(id)


    def create(self, data: User) -> User:
        return self.create_user.execute(data)


    def update(self, data: User, id: int) -> User:
        return self.update_user.execute(data, id)


    def delete(self, id: int) -> User:
        return self.delete_user.execute(id)


    def builder(self, definition: str) -> None:
        if (definition == 'postgres'):
            self.connection = Postgres_Connection()
            self.conversor = Postgres_Type()

            self.get_all_user = Get_All_Postgres(self.name_table, self.connection)
            self.count_user = Count_Postgres(self.name_table, self.connection)
            self.create_user = Create_Postgres(self.name_table, self.connection, self.conversor)
            self.get_one_user = Get_One_Postgres(self.name_table, self.connection)
            self.update_user = Update_Postgres(self.name_table, self.connection, self.conversor)
            self.delete_user = Delete_Postgres(self.name_table, self.connection, self.conversor)
            self.filter_user = Filter_Postgres(self.name_table, self.connection, self.conversor)

        if (definition == 'mongo'):
            pass

        if (definition == 'schema'):
            pass
