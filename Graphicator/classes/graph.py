import pandas
import pandas_ta
import plotly.graph_objects as graph_objects
from plotly.subplots import make_subplots


class Graph:
    def __init__(self, dataset):
        self.dataset = dataset
        self._figure = None

    def show(self):
        self._transform_dataframe()
        self._create_figure()
        self._figure.show()

    def _create_figure(self):
        self._figure = make_subplots(
            specs=[[{"secondary_y": True}]]
        )

        self._draw_price()
        #self._draw_volume()
        self._draw_ema_9()
        self._draw_ema_20()
        self._configure_layout()

    def _draw_price(self):
        self._figure.add_trace(graph_objects.Candlestick(
            name='Open/Close',
            x=self.dataset.index,
            open=self.dataset['open'],
            high=self.dataset['high'],
            low=self.dataset['low'],
            close=self.dataset['close']
        ), secondary_y=True)

    def _draw_volume(self):
        self._figure.add_trace(graph_objects.Bar(
            name='Volume',
            x=self.dataset.index,
            y=self.dataset['volume']
        ), secondary_y=False)

    def _draw_ema_9(self):
        self._figure.add_trace(graph_objects.Scatter(
            name='EMA9',
            x=self.dataset.index,
            y=self.dataset['ema9'],
            line=dict(color='white', width=1)
        ))

    def _draw_ema_20(self):
        self._figure.add_trace(graph_objects.Scatter(
            name='EMA20',
            x=self.dataset.index,
            y=self.dataset['ema20'],
            line=dict(color='cyan', width=1)
        ))

    def _configure_layout(self):
        self._figure.layout.yaxis.color = 'red'
        self._figure.update_layout(
            xaxis_rangeslider_visible=False,
            showlegend=True,
            template="plotly_dark"
        )

    def _transform_dataframe(self):
        self.dataset['date'] = pandas.to_datetime(self.dataset['date'])
        self.dataset = self.dataset.set_index('date')

        self.dataset['ema9'] = pandas_ta.ema(self.dataset['close'], length=9, offset=None, append=True)
        self.dataset['ema20'] = pandas_ta.ema(self.dataset['close'], length=20, offset=None, append=True)
