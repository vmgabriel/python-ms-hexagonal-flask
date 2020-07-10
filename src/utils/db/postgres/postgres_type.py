# Develop: vmgabriel

# Libraries
from typing import List, TypeVar, Generic, Any
from datetime import datetime

# Interface
from domain.models.db.entity_conversor import Conversor_Type

# Configurations
from config.server import configuration as conf

class Postgres_Type(Conversor_Type):
    def __init__(self):
        self.format_datetime = '%Y-%m-%d %H:%M:%S'

    def str_to(self, data: str) -> str:
        return "'{}'".format(data)

    def int_to(self, data: int) -> str:
        return "{}".format(data)

    def datetime_to(self, data: datetime.date) -> str:
        return "'{}'".format(data.strftime(self.format_datetime))

    def bool_to(self, data: bool) -> str:
        return "{}".format('TRUE' if (data) else 'FALSE')

    def list_to(self, data: List[Any]) -> str:
        return str(data)

    def keyword_to(self, data: str) -> str:
        return '{}'.format(data)

    def to_entity(self, type_str: str, data: Any) -> str:
        if (type_str == 'str'):
            return self.str_to(data)
        if (type_str == 'int'):
            return self.int_to(data)
        if (type_str == 'datetime'):
            return self.datetime_to(data)
        if (type_str == 'bool'):
            return self.bool_to(data)
        if (type_str == 'list'):
            return self.list_to(data)
        if (type_str == 'keyword'):
            return self.keyword_to(data)
        return ''
