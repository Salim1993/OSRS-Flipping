from abc import ABC, abstractmethod
from typing import Any


class IPriceRepository(ABC):
    @abstractmethod
    def get_mapping(self) -> list[dict]:
        ...

    @abstractmethod
    def get_latest_prices(self) -> dict[str, Any]:
        ...

    @abstractmethod
    def get_hourly_prices(self) -> dict[str, Any]:
        ...
