import inspect
from collections.abc import Iterable, Iterator
from typing import Any, get_origin, get_args, Annotated, Union, Generic

from fastapi import Depends


class Singleton:
    def __init__(self, cls):
        self.__wrapped__ = cls
        self._instance = None

    def __call__(self, *args, **kwargs):
        if self._instance is None:
            self._instance = self.__wrapped__(*args, **kwargs)
        return self._instance


def singleton(cls):
    return Singleton(cls)


class IterableDependency[T](Iterable[T]):

    def __init__(self):
        self.collection: set[T] = set()
        self.args = ()
        self.kwargs = {}

    def add(self, item: type[T]):
        self.collection.update((item,))

    def __iter__(self) -> Iterator[T]:
        for item in self.collection:
            yield item(**self.kwargs)

    def __call__(self, *args, **kwargs):
        pass


class ServiceCollection:
    def __init__(self):
        self._container: dict[type, Any] = {ServiceCollection: self}

    def add_singleton(self, base_type: type, impl_type=None):
        self._container.update({base_type: Singleton(impl_type or base_type)})

    def add_instance(self, base_type: type, instance):
        self._container.update({base_type: lambda: instance})

    def add_scoped(self, base_type: type, impl_type=None):
        self._container.update({base_type: impl_type or base_type})

    def get(self, base_type: type):
        return self._container[base_type]

    def build(self):
        for cls in self._container.values():
            if isinstance(cls, ServiceCollection):
                continue

            signature = inspect.signature(cls)
            parameters = []

            for parameter in signature.parameters.values():
                if get_origin(parameter.annotation) is Annotated:
                    parameters.append(parameter)
                    continue

                if get_origin(parameter.annotation) in (Union, Generic,):
                    arg = get_args(parameter.annotation)[0]

                    if depends := self._container.get(arg):
                        parameters.append(parameter.replace(
                            annotation=Annotated[parameter.annotation, Depends(depends)]
                        ))
                    else:
                        parameters.append(parameter)
                else:
                    if depends := self._container.get(parameter.annotation):
                        parameters.append(parameter.replace(
                            annotation=Annotated[parameter.annotation, Depends(depends)]
                        ))
                    else:
                        parameters.append(parameter)

            cls.__signature__ = signature.replace(parameters=parameters)


services = ServiceCollection()
