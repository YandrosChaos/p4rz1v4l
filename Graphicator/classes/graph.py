import pandas
import pandas_ta
from plotly.graph_objs import Figure
from plotly.subplots import make_subplots

from Graphicator.classes.graph_builder import *
from Graphicator.classes.markers import *


class Graph:
    def __init__(self, dataset):
        self.dataset = dataset
        self._figure = None

    # Transform the dataframe. Then creates the figures and
    # show it.
    def show(self):
        self._transform_dataframe()
        self._create_figure()
        self._figure.show()

    # Creates all figures to draw. Includes price, volume, ema 100,
    # ema 20 and operation markers. Layout config is included too.
    def _create_figure(self):
        self._figure: Figure = make_subplots(
            rows=2, cols=1, row_heights=[0.7, 0.3],
            shared_xaxes=True
        )

        self._draw_price()
        self._draw_volume()
        self._draw_ema_100()
        self._draw_ema_20()
        self._draw_operations()
        self._configure_layout()

    # Draws the prices main figure.
    def _draw_price(self):
        self._figure.add_trace(build_price_graph(self.dataset), row=1, col=1)

    # Draws the volume figure.
    def _draw_volume(self):
        self._figure.add_trace(build_volume_graph(self.dataset), row=2, col=1)

    # Draws EMA100 figure.
    def _draw_ema_100(self):
        self._figure.add_trace(build_ema100_graph(self.dataset), row=1, col=1)

    # Draws EMA20 figure.
    def _draw_ema_20(self):
        self._figure.add_trace(build_ema20_graph(self.dataset), row=1, col=1)

    # Draws Operations figures (short, long, stoploss).
    def _draw_operations(self):
        self._draw_short_ops()
        self._draw_long_ops()
        self._draw_stoploss_ops()

    def _draw_long_ops(self):
        open_ops = self.dataset[self.dataset['operation'] == OperationType.LONG_OPEN]
        close_ops = self.dataset[self.dataset['operation'] == OperationType.LONG_CLOSE]

        conf: MarkerConfigOps = get_config_by_operation(OperationType.LONG)

        self._draw_markers(open_ops, conf.open)
        self._draw_markers(close_ops, conf.close)

    def _draw_short_ops(self):
        open_ops = self.dataset[self.dataset['operation'] == OperationType.SHORT_OPEN]
        close_ops = self.dataset[self.dataset['operation'] == OperationType.SHORT_CLOSE]

        conf: MarkerConfigOps = get_config_by_operation(OperationType.SHORT)

        self._draw_markers(open_ops, conf.open)
        self._draw_markers(close_ops, conf.close)

    def _draw_stoploss_ops(self):
        long_ops = self.dataset[self.dataset['operation'] == OperationType.LONG_STOPLOSS_CLOSE]
        short_ops = self.dataset[self.dataset['operation'] == OperationType.SHORT_STOPLOSS_CLOSE]

        conf: MarkerConfigOps = get_config_by_operation(OperationType.STOPLOSS)

        self._draw_markers(long_ops, conf.open)
        self._draw_markers(short_ops, conf.close)

    def _draw_markers(self, dataset, config: MarkerConfig):
        self._figure.add_trace(build_marker_graph(dataset, config), row=1, col=1)

    # Main configuration 4 the graphs.
    def _configure_layout(self):
        self._figure.layout.yaxis.color = 'red'
        self._figure.update_layout(
            xaxis_rangeslider_visible=False,
            showlegend=True,
            template="plotly_dark"
        )

    # Adds EMA100 and EMA20 columns to dataset.
    def _transform_dataframe(self):
        self.dataset['date'] = pandas.to_datetime(self.dataset['date'])
        self.dataset = self.dataset.set_index('date')

        self.dataset['ema100'] = pandas_ta.ema(self.dataset['close'], length=100, offset=None, append=True)
        self.dataset['ema20'] = pandas_ta.ema(self.dataset['close'], length=20, offset=None, append=True)
