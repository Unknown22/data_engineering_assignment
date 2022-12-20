import abc


class FileProcessor(abc.ABC):

    def __init__(self, filepath: str):
        self.filepath = filepath

    @abc.abstractmethod
    def transform(self):
        raise NotImplementedError
