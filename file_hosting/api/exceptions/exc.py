from fastapi import status

from .enums import PlaceEnum

from .base_exc import ObjectNotExist, ObjectAlreadyExist, InvalidData


class ObjectNotExistInPath(ObjectNotExist):
    def __init__(
            self, model: str, place: str = PlaceEnum.path,
            status_code: int = status.HTTP_404_NOT_FOUND
    ) -> None:
        super().__init__(model, place, status_code)


class ObjectNotExistInBody(ObjectNotExist):
    def __init__(
            self, model: str, place: str = PlaceEnum.body,
            status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY
    ) -> None:
        super().__init__(model, place, status_code)


class ObjectAlreadyExistInBody(ObjectAlreadyExist):
    def __init__(
            self, model: str, attr: str, place: str = PlaceEnum.body,
            status_code: int = status.HTTP_409_CONFLICT
    ) -> None:
        super().__init__(model, attr, place, status_code)


class InvalidDataInBody(InvalidData):
    def __init__(
            self, model: str, attr: str, place: str = PlaceEnum.body,
            status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY
    ):
        super().__init__(model, attr, place, status_code)
