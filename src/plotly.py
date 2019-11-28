import plotly.graph_objs as go
from typing import List

def plot_histogram(x, title, xaxis_title, yaxis_title, params: dict = None):
    """
    Returns a plotly histogram.
    x: x values,
    title: Title of the plot
    xaxis_title: Tile of the x-axis
    yaxis_title: Tile of the y-axis
    params: Other params to pass to go.Histogram()
    """
    fig = go.Figure()
    fig.add_trace(
        go.Histogram(
            x=x,    
            **params,
        )
    )

    fig.update_layout(
        title=title,
        title_x=0.5,
        template = 'simple_white',
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title
    )
    return fig

def plot_timeline(x, y, title, xaxis_title, yaxis_title, annotations: List = None):
    """ 
    x: The x values
    y: The y values
    title: Title of the plot
    xaxis_title: Tile of the x-axis
    yaxis_title: Tile of the y-axis
    params: Other params to pass to go.Histogram()
    """
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode='lines',
            name='lines'
        )
    )
    fig.update_layout(
        title=title,
        title_x=0.5,
        template = 'simple_white',
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        annotations=annotations
    )
    return fig