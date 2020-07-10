# Develop: vmgabriel

# Libraries
from functools import reduce
from typing import TypeVar, Generic, Any, List

# Interfaces
from domain.models.actions.filter import Filter
from domain.models.db_connection import Db_Connection
from domain.models.db.entity_conversor import Conversor_Type

# Structures
from user.domain.user import User
from domain.models.filter_interface import Filter_Interface, Column_Filter, Attribute_Filter

# Configuration
from config.server import configuration as conf

class Filter_User(Filter[User]):
    def __init__(self, name_table: str, database: Db_Connection, conversor: Conversor_Type):
        self.name_table = name_table
        self.__database = database
        self.conversor = conversor
        self.query = 'SELECT '

    def minimize_str(self, data: List[Any]):
        minimize = lambda x: x.strip() if (type(x) == str) else x
        if (len(data) == 1):
            return [minimize(data[0])]
        return [minimize(data[0])] + self.minimize_str(data[1:])


    def execute(
            self,
            filters: Filter_Interface,
            attributes: List[Attribute_Filter],
            joins: Any,
            limit: int,
            offset: int
    ) -> (List[User], str):
        query_filter = query_count = self.query
        query_filter += self.convert_attributes(attributes)
        query_count += self.convert_attributes(attributes, is_count=True)
        query_filter += ' FROM '
        query_count += ' FROM '
        query_filter += self.definitor()
        query_count += self.definitor()
        query_filter += self.convert_joins(joins)
        query_count += self.convert_joins(joins)
        query_filter += ' WHERE '
        query_count += ' WHERE '
        query_filter += self.convert_filter(filters)
        query_count += self.convert_filter(filters)
        query_filter += self.convert_limit_offset(limit, offset)

        cursor = self.__database.get_cursor()
        cursor.execute(query_filter)
        rows = cursor.fetchall()
        rows = list(map(self.minimize_str, rows))

        return ([User(*row) for row in rows], query_count)


    def convert_column(self, column_filter: Column_Filter) -> str:
        if (column_filter['op'] == 'between'):
            return '({} BETWEEN {} AND {})'.format(
                column_filter['column'],
                self.conversor.to_entity(column_filter['type_data'], column_filter['value'][0]),
                self.conversor.to_entity(column_filter['type_data'], column_filter['value'][1])
            )
        if (column_filter['op'] == 'like'):
            return '({} LIKE {})'.format(
                column_filter['column'],
                self.conversor.to_entity(
                    column_filter['type_data'],
                    '%' + column_filter['value'] + '%'
                )
            )
        if (column_filter['op'] == 'in'):
            return '({} IN {})'.format(
                column_filter['column'],
                self.conversor.to_entity(column_filter['type_data'], column_filter['value'])
            )
        return '({} {} {})'.format(
            column_filter['column'],
            column_filter['op'],
            self.conversor.to_entity(column_filter['type_data'], column_filter['value'])
        )


    def convert_filter(self, filters: Filter_Interface) -> str:
        query = ''
        default = filters['default'] if ('default' in filters) else ''

        if not(filters):
            return query

        if ('and_data' in filters):
            if (type(filters['and_data']) == dict):
                new_filter = dict(filters)
                new_filter['default'] = 'and_data'
                query += '({})'.format(self.convert_filter(new_filter))
            else:
                filter_definitions = list(map(lambda x: self.convert_column(x), filters['and_data']))
                query += '({})'.format(
                    ' AND '.join(filter_definitions)
                )

        query += ' '
        query += default

        if ('or_data' in filters):
            if (type(filters['or_data']) == dict):
                new_filter = dict(filters)
                new_filter['default'] = 'or_data'
                query += '({})'.format(self.convert_filter(new_filter))
            else:
                filter_definitions = list(map(lambda x: self.convert_column(x), filters['or_data']))
                query += '({})'.format(
                    ' OR '.join(filter_definitions)
                )

        return query


    def convert_limit_offset(self, limit: int, offset: int) -> str:
        return 'OFFSET {} LIMIT {}'.format(offset, limit)


    def convert_attributes(self, attributes: List[Attribute_Filter], is_count: bool = False) -> str:
        convert_attribute = lambda x: '{} "{}"'.format(x['column'], x['as_name']) if ('as_name' in x) else x['column']
        if (is_count):
            return 'COUNT(*)'

        if (len(attributes) == 0):
            return '*'
        list_attributes = list(map(convert_attribute, attributes))
        return ','.join(list_attributes)


    def convert_joins(self, joins: Any) -> str:
        return ''


    def definitor(self) -> str:
        return '{}.{}'.format(conf['db_name_schema'], self.name_table)
