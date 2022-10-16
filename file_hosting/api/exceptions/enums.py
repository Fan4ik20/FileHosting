from enum import Enum


class PlaceEnum(str, Enum):
    path = 'path'
    body = 'body'
    query = 'query'
