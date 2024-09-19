from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class KafkaConsumerRecord(Generic[T]):
    value: T
    headers: dict[str, str]
