import os
import json
from dotenv import load_dotenv
from typing import Type, Any, TypeVar, Dict

load_dotenv()

T = TypeVar("T")


class EnvLoaderMeta(type):
    def __new__(
        cls: Type["EnvLoaderMeta"], name: str, bases: tuple, dct: Dict[str, Any]
    ) -> "EnvLoaderMeta":
        annotations: Dict[str, Type[Any]] = dct.get("__annotations__", {})
        for key, type_ in annotations.items():
            env_value: str = os.getenv(key, "")
            if not env_value:
                raise ValueError(f"{key} environment variable is not set")

            try:
                if (
                    type_ is list
                    or hasattr(type_, "__origin__")
                    and type_.__origin__ is list
                ):
                    if not hasattr(type_, "__args__") or not type_.__args__:  # type: ignore
                        raise TypeError(
                            f"{key} must specify a type for the list, e.g. list[int] or list[str]"
                        )

                    element_type = type_.__args__[0]  # type: ignore
                    dct[key] = [element_type(i) for i in json.loads(env_value)]
                else:
                    dct[key] = type_(env_value)
            except (ValueError, json.JSONDecodeError):
                raise ValueError(
                    f"Cannot convert {key} to {type_.__name__}. {key}={env_value}"
                )

        def __repr__(self) -> str:
            dcts: Dict[str, Any] = self.__class__.__dict__
            keys = [
                f"{key}={value!r}"
                for key, value in dcts.items()
                if not key.startswith("__")
            ]
            return f"{self.__class__.__name__}({', '.join(keys)})"

        def __setattr__(self, key: str, value: Any) -> None:
            if key in self.__class__.__dict__:
                raise AttributeError(f"Cannot reassign {key}, it is a constant")
            super(self.__class__, self).__setattr__(key, value)

        dct["__repr__"] = __repr__
        dct["__setattr__"] = __setattr__

        return super().__new__(cls, name, bases, dct)
