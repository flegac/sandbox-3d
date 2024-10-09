from abc import ABC, abstractmethod


class Switchable(ABC):
    def __init__(self):
        self.is_active = False

    def switch(self, status: bool = None):
        if status is None:
            status = not self.is_active
        # logger.info(f'{self.__class__.__name__}: is_active={status}')

        # TODO
        # self.is_active = status
        # if self.is_active:
        #     self._enable()
        # else:
        #     self._disable()
        return self

    @abstractmethod
    def _enable(self):
        ...

    @abstractmethod
    def _disable(self):
        ...
