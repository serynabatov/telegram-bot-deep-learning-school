from abc import ABC, abstractmethod


class Abstract_Strategy(ABC):

    @abstractmethod
    def send_to_net(self, *args):
        pass

