# Develi

from dataclasses import dataclass
from datetime import datetime

from dataclasses_json import dataclass_json, LetterCase


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class User:
    id: str
    name: str
    lastName: str
    email: str
    photoUrl: str
    isValid: bool
    createdAt: datetime
    updatedAt: datetime
    deletedAt: datetime

    def __str__(self):
        return 'name,lastName,email,photoUrl,isValid,createdAt,updatedAt'

    def define_type(self, type_val):
        if (
                type_val == 'name' or
                type_val == 'lastName' or
                type_val == 'email' or
                type_val == 'photoUrl'
        ):
            return 'str'
        if (type_val == 'isValid'):
            return 'bool'
        if (type_val == 'createdAt' or
            type_val == 'updatedAt'
            or type_val == 'deletedAt'
        ):
            return 'datetime'
        if (type_val == 'id'):
            return 'int'
        return ''

    def id_name(self):
        return 'id'

    def validation_name(self):
        return 'isValid'

    def delete_date_name(self):
        return 'deletedAt'
