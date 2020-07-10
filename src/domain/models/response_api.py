
# Develop vmgabriel

# DataClass
from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class Response_Api:
    code: int
    message: str
    error: str
    row: List['typing.Any']
