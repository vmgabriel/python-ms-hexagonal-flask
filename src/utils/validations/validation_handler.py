# Develop: vmgabriel

# Libraries
import re, sys, functools
from typing import List, TypeVar, Generic, Any

from config.server import configuration as conf

class Validate_Handler:
    def __init__(self):
        pass

    def compose(self, *functions):
        return functools.reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)

    def compose_and(self, *functions):
        def define(x):
            compositor = True
            for func in functions:
                compositor = func(x) and compositor
            return compositor
        return lambda x: define(x)

    def compose_or(self, *functions):
        def define(x):
            compositor = False
            for func in functions:
                compositor = func(x) or compositor
            return compositor
        return lambda x: define(x)

    def exist(self):
        return lambda x: x != None if (type(x) != bool) else True

    def min(self, data: int):
        return lambda x:  x > data if (type(x) == int) else len(x) > data if x else False

    def max(self, data: int):
        return lambda x:  x < data if (type(x) == int) else len(x) < data if x else False

    def max_eq(self, data: int):
        return lambda x:  x <= data if (type(x)==int) else len(x) <= data if x else False

    def min_eq(self, data: int):
        return lambda x:  x >= data if (type(x)==int) else len(x) >= data if x else False

    def regex(self, data: str):
        return lambda x: bool(re.search(data, x)) if (x) else False

    def max_data(self):
        return self.max(conf['limit_max'])

    def min_eq_data(self):
        return self.min_eq(conf['limit_min'])

    def email(self):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        return self.regex(regex)

    def url(self):
        regex = '^http[s]?:\/\/[a-zA-Z0-9:]\S+.\w\S{2,}$'
        return self.regex(regex)

    def data_order_validate(self, data: str):
        if (len(data[1:]) <= 1):
            return 'no valid order'
        return 'ok'


    def data_filter_content(self, limit: int, offset: int) -> str:
        if (compose(max_data, min_eq_data)(limit)):
            return 'limit no valid'
        return 'ok'


    def data_order_content(self, order: List[str]) -> bool:
        if (len(order) == 1):
            return self.data_order_validate(order[0]) == 'ok'
        return self.data_order_validate(order[0]) == 'ok' and self.data_order_content(order[1:])
