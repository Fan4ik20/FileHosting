from typing import TypeVar, Iterable, Generic

Model = TypeVar('Model')

DTO = TypeVar('DTO')
DTOUpdate = TypeVar('DTOUpdate')
DTOCreate = TypeVar('DTOCreate')


__all__ = ['BaseConverter']


class BaseConverter(Generic[Model, DTOCreate, DTO, DTOUpdate]):
    @classmethod
    def convert_to_repr_list(
            cls, model_list: Iterable[Model]
    ) -> Iterable[DTO]:
        return [cls.convert_to_repr(model) for model in model_list]

    @staticmethod
    def convert_to_repr(model: Model) -> DTO:
        raise NotImplementedError

    @staticmethod
    def convert_to_model_create(repr_obj: DTOCreate) -> Model:
        raise NotImplementedError

    @staticmethod
    def convert_to_model_update(repr_obj: DTOUpdate) -> Model:
        raise NotImplementedError
