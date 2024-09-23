import plotly.graph_objects as go


class PlotlyGraph:
    """One graph as one object"""

    def __init__(self) -> None:
        """
        G = PlotlyGraph()

        fig = G.fig

        fig.add_trace(...)

        G.add_line(x, y)

        fig.show()
        """

        # Start by passing the plotly.graph_objects.Figure in.
        # Why: add_trace did not support feature like "z-order" at this point.

        self.fig = go.Figure()

    # @staticmethod
    def add_line(self, x, y, **kwargs):
        """Line Chart

        Args:
            x (numpy.ndarray / list): 1d array / list of 1d array
            y (numpy.ndarray / list): 1d array / list of 1d array

            label (list): "name" of each y

            xlim (list): [low, up] of x-axis range (visualization)
            ylim (list): [low, up] of y-axis range

            title (string): opt. header
            xlabel (string): opt. x-axis title
            ylabel (string): opt. y-axis title

            mode (string): opt. 'lines' / 'lines+markers'

            fontsize (int): opt. default 16

            xticks_val (list): opt. x-axis ticks label's position
            xticks_label (list): opt. x-axis ticks labels's text

            autotickangles (list): opt. default [0, 90]

        Returns:
            plotly.graph_object
        """

        fig = self.fig  # fig = go.Figure()

        if not isinstance(y, list):
            y = [y]

        if not isinstance(x, list):
            x = [x]

        _labels = kwargs.get("label", [None for i in y])

        _xlim = kwargs.get("xlim")
        _ylim = kwargs.get("ylim")

        _title = kwargs.get("title")
        _xlabel = kwargs.get("xlabel")
        _ylabel = kwargs.get("ylabel")

        _mode = kwargs.get("mode", "lines")  # markers lines

        _fontsize = kwargs.get("fontsize", 16)

        _xticks_val = kwargs.get("xticks_val")
        _xticks_label = kwargs.get("xticks_label")

        _autotickangles = kwargs.get("autotickangles", [0, 90])

        xticks_dict = dict(
            tickfont=dict(
                size=_fontsize,
            )
        )
        if _xticks_val:
            xticks_dict = dict(
                showgrid=True,
                tickmode="array",
                tickvals=_xticks_val,
                ticktext=_xticks_label,
                tickfont=dict(
                    size=_fontsize,
                ),
            )

        for i in range(len(y)):
            fig.add_trace(
                go.Scatter(
                    x=x[i],
                    y=y[i],
                    name=_labels[i],
                    mode=_mode,
                )
            )

        fig.update_layout(
            title=dict(
                text=_title,
                font=dict(size=26),
            ),
            xaxis_title=dict(
                text=_xlabel,
                font=dict(
                    size=_fontsize,
                ),
            ),
            yaxis_title=dict(
                text=_ylabel,
                font=dict(
                    size=_fontsize,
                ),
            ),
            xaxis=xticks_dict,
            yaxis=dict(
                tickfont=dict(
                    size=_fontsize,
                ),
            ),
            xaxis_range=_xlim,
            yaxis_range=_ylim,
        )

        fig.update_xaxes(autotickangles=_autotickangles)

        return fig
