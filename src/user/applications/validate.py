# Develop: vmgabriel
# Libraries
from typing import List, TypeVar, Generic, Any

# Domains
from domain.models.validation_interface import Validate_Interface
from utils.validations.validation_handler import Validate_Handler

from user.domain.user import User

class User_Validate(Validate_Interface[User]):
    def __init__(self):
        self.v = Validate_Handler()

        self.name_validation = self.v.compose_and(
            self.v.min(3),
            self.v.max(100)
        )
        self.lastname_validation = self.v.compose_and(
            self.v.min(3),
            self.v.max(100)
        )
        self.email_validation = self.v.compose_and(
            self.v.min(4),
            self.v.max(100),
            self.v.email()
        )
        self.is_valid_validation = lambda x: True
        self.photo_url_validation = lambda x: True
        self.created_at_validation = lambda x: True
        self.updated_at_validation = lambda x: True

        self.name_validation_valid = self.v.compose_and(
            self.v.exist(),
            self.v.min(3),
            self.v.max(100)
        )
        self.lastname_validation_valid = self.v.compose_and(
            self.v.exist(),
            self.v.min(3),
            self.v.max(100)
        )
        self.email_validation_valid = self.v.compose_and(
            self.v.exist(),
            self.v.min(4),
            self.v.max(100),
            self.v.email()
        )
        self.is_valid_validation_valid = self.v.compose_and(
            self.v.exist()
        )
        self.photo_url_validation_valid = self.v.compose_and(
            self.v.exist()
        )
        self.created_at_validation_valid = self.v.compose_and(
            self.v.exist()
        )
        self.updated_at_validation_valid = self.v.compose_and(
            self.v.exist()
        )

    def validate_object(self, data: Any) -> (str, User):
        id = data['id'] if ('id' in data) else None
        name = data['name'] if ('name' in data) else None
        lastName = data['lastName'] if ('lastName' in data) else None
        email = data['email'] if ('email' in data) else None
        isValid = data['isValid'] if ('isValid' in data) else None
        photoUrl = data['photoUrl'] if ('photoUrl' in data) else None
        createdAt = data['createdAt'] if ('createdAt' in data) else None
        updatedAt = data['updatedAt'] if ('updatedAt' in data) else None
        deletedAt = data['deletedAt'] if ('deletedAt' in data) else None

        if not (self.name_validation_valid(name)):
            return('name not valid', {})
        if not (self.lastname_validation_valid(lastName)):
            return('last name not valid', {})
        if not (self.email_validation_valid(email)):
            return('email not valid', {})
        if not (self.is_valid_validation_valid(isValid)):
            return('is valid not valid', {})
        if not (self.photo_url_validation_valid(photoUrl)):
            return('photo url not valid', {})
        if not (self.created_at_validation_valid(createdAt)):
            return('created at not valid', {})
        if not (self.updated_at_validation_valid(updatedAt)):
            return('updated at not valid', {})

        return ('done correctly', User(
            id,
            name,
            lastName,
            email,
            photoUrl,
            isValid,
            createdAt,
            updatedAt,
            deletedAt
        ))

    def validate_object_update(self, data: Any) -> (str, User):
        id = data['id'] if ('id' in data) else None
        name = data['name'] if ('name' in data) else None
        lastName = data['lastName'] if ('lastName' in data) else None
        email = data['email'] if ('email' in data) else None
        isValid = data['isValid'] if ('isValid' in data) else None
        photoUrl = data['photoUrl'] if ('photoUrl' in data) else None
        createdAt = data['createdAt'] if ('createdAt' in data) else None
        updatedAt = data['updatedAt'] if ('updatedAt' in data) else None
        deletedAt = data['deletedAt'] if ('deletedAt' in data) else None

        if not (self.name_validation(name) if (name) else True):
            return('name not valid', {})
        if not (self.lastname_validation(lastName) if (lastName) else True):
            return('last name not valid', {})
        if not (self.email_validation(email) if (email) else True):
            return('email not valid', {})
        if not (self.is_valid_validation(isValid) if (isValid) else True):
            return('is valid not valid', {})
        if not (self.photo_url_validation(photoUrl) if (photoUrl) else True):
            return('photo url not valid', {})
        if not (self.created_at_validation(createdAt) if (createdAt) else True):
            return('created at not valid', {})
        if not (self.updated_at_validation(updatedAt) if (updatedAt) else True):
            return('updated at not valid', {})

        return ('done correctly', User(
            id,
            name,
            lastName,
            email,
            photoUrl,
            isValid,
            createdAt,
            updatedAt,
            deletedAt
        ))


    def data_filter_content(self, limit: int, offset: int) -> str:
        return self.validation_base.data_filter_content(limit, offset)

    def data_order_content(self, order: List[str]) -> bool:
        return self.validation_base.data_order_content(order)
