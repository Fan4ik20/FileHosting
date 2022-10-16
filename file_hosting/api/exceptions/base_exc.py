class ObjectNotExist(Exception):
    def __init__(self, model: str, place: str, status_code: int):
        self.model = model
        self.place = place
        self.status_code = status_code


class ObjectAlreadyExist(Exception):
    def __init__(self, model: str, attr: str, place: str, status_code: int):
        self.model = model
        self.attr = attr
        self.place = place
        self.status_code = status_code


class InvalidData(Exception):
    def __init__(self, model: str, attr: str, place: str, status_code: int):
        self.model = model
        self.attr = attr
        self.place = place
        self.status_code = status_code
