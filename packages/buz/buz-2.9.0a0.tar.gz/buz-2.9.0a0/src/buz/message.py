from abc import ABC
from dataclasses import field, dataclass
from datetime import datetime
from inspect import signature, Parameter
from types import MappingProxyType
from typing import Any, ClassVar, Dict, get_origin, get_args, Union
from uuid import uuid4


@dataclass(frozen=True)
class Message(ABC):
    DATE_TIME_FORMAT: ClassVar[str] = "%Y-%m-%d %H:%M:%S.%f"

    id: str = field(init=False, default_factory=lambda: str(uuid4()))
    created_at: str = field(
        init=False, default_factory=lambda: datetime.strftime(datetime.now(), Message.DATE_TIME_FORMAT)
    )

    @classmethod
    def fqn(cls) -> str:
        return f"{cls.__module__}.{cls.__name__}"

    @classmethod
    def restore(cls, **kwargs: Any) -> "Message":  # type: ignore[misc]
        message_id = kwargs.pop("id")
        created_at = kwargs.pop("created_at")

        instance = cls.__from_dict(kwargs)  # type: ignore

        object.__setattr__(instance, "id", message_id)
        object.__setattr__(instance, "created_at", created_at)
        return instance

    @classmethod
    def __from_dict(cls, data: Dict[str, Any]) -> "Message":
        expected_params = signature(cls).parameters
        actual_params = {key: value for key, value in data.items() if key in expected_params}
        if len(actual_params) == len(expected_params):
            return cls(**actual_params)  # type: ignore[call-arg]

        filled_optional_attributes = cls.__fill_optional_attributes(actual_params, expected_params)
        return cls(**filled_optional_attributes, **actual_params)  # type: ignore[call-arg]

    @classmethod
    def __fill_optional_attributes(
        cls, actual_params: Dict[str, Any], expected_params: MappingProxyType
    ) -> Dict[str, None]:
        filled_optional_attributes: Dict[str, None] = {}
        for key, parameter in expected_params.items():
            if key not in actual_params and cls.__is_optional(parameter) is True:
                filled_optional_attributes[key] = None
        return filled_optional_attributes

    @classmethod
    def __is_optional(cls, parameter: Parameter) -> bool:
        return get_origin(parameter.annotation) is Union and any(
            (arg is type(None) for arg in get_args(parameter.annotation))  # noqa E721
        )

    def parsed_created_at(self) -> datetime:
        return datetime.strptime(self.created_at, self.DATE_TIME_FORMAT)
