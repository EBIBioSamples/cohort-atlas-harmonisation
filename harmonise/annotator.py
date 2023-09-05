import abc


class Annotator(abc.ABC):
    @abc.abstractmethod
    def annotate(self, dataframe):
        return

    @abc.abstractmethod
    def load_model(self):
        return
