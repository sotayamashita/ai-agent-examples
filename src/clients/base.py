from abc import ABC, abstractmethod


class BaseClient(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def generate():
        pass
