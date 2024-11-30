from typing import Protocol


class Filter(Protocol):
    def __init__(self):
        self._process = None

    @property
    def process(self):
        return self._process

    def run(self) -> None: ...
