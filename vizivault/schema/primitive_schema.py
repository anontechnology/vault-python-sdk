from enum import Enum


class PrimitiveSchema(Enum):
    STRING = 'string',
    INTEGER = 'int',
    BOOLEAN = 'boolean',
    FILE = 'file',
    FLOAT = 'float',
    DATE = 'date'
