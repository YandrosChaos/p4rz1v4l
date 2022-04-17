import pandas
import plotly.graph_objects as graph_objects


class Graph:
    def __init__(self, dataset):
        self.dataset = dataset
        self._figure = None

    def show(self):
        self._transform_date()
        self._create_figure()
        self._figure.show()

    def _create_figure(self):
        self._figure = graph_objects.Figure()
        self._figure.add_trace(graph_objects.Scatter(
            x=self.dataset.index,
            y=self.dataset['close']
        ))

    def _transform_date(self):
        self.dataset['date'] = pandas.to_datetime(self.dataset['date'])
        self.dataset = self.dataset.set_index('date')
        print(self.dataset)
