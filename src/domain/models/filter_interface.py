# Develop: vmgabriel

# Develop vmgabriel

# DataClass
from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase
from typing import Any

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class Filter_Interface:
    and_data: Any
    or_data: Any
    default: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class Column_Filter:
    column: str
    op: str
    value: Any
    type_data: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class Attribute_Filter:
    column: str
    as_name: str
