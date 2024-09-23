from abc import abstractmethod

from octopus_common.model import result_detail


class Crawler:
    @abstractmethod
    def crawl(self, task) -> ResultDetail:
        pass
