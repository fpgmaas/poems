import plotly.graph_objs as go
from plotly.subplots import make_subplots
from typing import List
import numpy as np

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

def plot_scatter(x,y,text,title,xaxis_title,yaxis_title):
    """
    Returns a grouped plotly scatter plot. 
    x: x values
    y: y values
    text: numpy array with hover text for each observation
    title: Title of the plot
    xaxis_title: Tile of the x-axis
    yaxis_title: Tile of the y-axis
    marker: optional, to add as parameter to go.Scatter
    """
    
    fig = go.Figure(
            data=go.Scatter(
                x=x,
                y=y,
                mode='markers',
                marker=dict(
                    size = 8,
                    line_width=1,
                    opacity=0.7
                ),
                hoverinfo = 'text',
                text=text
            )
    )

    fig.update_layout(
        title=title,
        title_x=0.5,
        template='simple_white',
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title
    )
    return fig

def plot_grouped_scatter(x,y,groups,unique_groups,text,title,xaxis_title,yaxis_title,
                         marker=dict(size = 10,line_width=1,opacity=0.7)):
    """
    Returns a grouped plotly scatter plot. 
    x: x values
    y: y values
    groups: The group for each observation
    unique_groups: The unique groups. Used to make sure that legens is in same order as other plots.
    text: numpy array with hover text for each observation
    title: Title of the plot
    xaxis_title: Tile of the x-axis
    yaxis_title: Tile of the y-axis
    marker: optional, to add as parameter to go.Scatter
    """
    fig = go.Figure()

    for group in unique_groups:
        idx = groups==group
        fig.add_trace(go.Scatter(
            x=x[idx],
            y=y[idx],
            mode='markers',
            name=group,
            marker = marker,
            hoverinfo = 'text',
            text = np.array(text)[idx],
        )
     )

    fig.update_layout(
        title=title,
        title_x=0.5,
        template='simple_white',
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title
    )
    return fig

def plot_multiple_timelines(x,y,groups,unique_groups,text,title,xaxis_title,yaxis_title,figsize:tuple=(600,900)):
    """
    Returns a plot with multiple timelines, one for each group in unique_groups.
    x: x values
    y: y values
    groups: The group for each observation
    unique_groups: The unique groups. Used to make sure that legens is in same order as other plots.
    text: numpy array with hover text for each observation
    title: Title of the plot
    xaxis_title: Tile of the x-axis
    yaxis_title: Tile of the y-axis
    figsize: tuple (width, height) of plot.
    """
    fig = go.Figure()
    fig = make_subplots(rows=len(unique_groups), cols=1,
                               x_title=xaxis_title,
        y_title=yaxis_title)
    k=1
    for group in unique_groups:
        subset = groups==group
        fig.append_trace(
            go.Scatter(
                x=x[subset],
                y=y[subset],
                mode='lines',
                name=group,
                hoverinfo = 'text',
                text=text[subset]
            ),
        row=k, col=1)
        k+=1
    for i in range(len(unique_groups)):    
        fig.update_yaxes(range=[min(y), max(y)], row=i+1, col=1)

    fig.update_layout(
        width=figsize[0],
        height=figsize[1],
        title=title,
        title_x=0.5,
        template = 'simple_white'
    )
    return fig
