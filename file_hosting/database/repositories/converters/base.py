from typing import TypeVar, Iterable

Model = TypeVar('Model')
Repr = TypeVar('Repr')


__all__ = ['BaseConverter']


class BaseConverter:
    @classmethod
    def convert_to_repr_list(
            cls, model_list: Iterable[Model]
    ) -> Iterable[Repr]:
        return [cls.convert_to_repr(model) for model in model_list]

    @staticmethod
    def convert_to_repr(model: Model) -> Repr:
        raise NotImplementedError

    @staticmethod
    def convert_to_model(repr_obj: Repr) -> Model:
        raise NotImplementedError
