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

def plot_horizontal_bar(labels, values, title, xaxis_title, yaxis_title, figsize: tuple = (800,900)):
    """  
    labels: The labels for on the y axis
    values: The corresponding values (length) of the bars.
    title: Title of the plot
    xaxis_title: Tile of the x-axis
    yaxis_title: Tile of the y-axis
    figsize: (width, height)
    """
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            y=labels,
            x=values,
            orientation='h'
        )
    )
    fig.update_layout(
            width=figsize[0], 
            height=figsize[1],
            title=title,
            title_x=0.5,
            template='simple_white',
            xaxis_title=xaxis_title,
            yaxis_title=yaxis_title,
            yaxis=dict(
                tickfont=dict(size=10),
                tickvals=labels
        )
    )
    return fig

def plot_heatmap(z,x,y,title,figsize: tuple = (600,600)):
    """  
    z: The values, a 2d-array or 2d-list
    x: Labels for the x-axis
    y: Labels for the y-axis
    title: Title of the plot
    figsize: (width, height)
    """
    
    fig = go.Figure(data=go.Heatmap(
                       z=z,
                       x=x,
                       y=y,
        colorscale='YlOrRd',
        zmid = 0
        )
    )
    fig.update_layout(
        title=title,
        title_x=0.5,
        width=figsize[0],
        height=figsize[1],
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig