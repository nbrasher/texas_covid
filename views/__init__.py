from plotly.subplots import make_subplots
import plotly.graph_objects as go

from scipy.interpolate import interp1d
from matplotlib.dates import date2num
import pandas as pd
import numpy as np

PLOT_START = pd.Timestamp('2020-03-24')

def plot_rt(result, name, fig, nrows=1, ncols=1, i=0):
    # Aesthetically, extrapolate credible interval by 1 day either side
    lowfn = interp1d(date2num(result.index),
                     result['Low_90'].values,
                     bounds_error=False,
                     fill_value='extrapolate')

    highfn = interp1d(date2num(result.index),
                      result['High_90'].values,
                      bounds_error=False,
                      fill_value='extrapolate')

    extended = pd.date_range(start=PLOT_START-pd.Timedelta(days=7),
                             end=result.index[-1]+pd.Timedelta(days=1))

    low_bound = lowfn(date2num(extended))
    high_bound = highfn(date2num(extended))

    # Build Plotly plot

    # 90% Confidence shading
    fig.add_trace(
        go.Scatter(
            x=extended.append(extended[::-1]),
            y=np.append(high_bound, low_bound[::-1]),
            fill='toself',
            fillcolor='rgba(0, 0 , 0, 0.1)',
            line_color='rgba(255,255,255,0)',
            showlegend=False,
            name='90% Confidence Interval'
        ),
        row=i//ncols+1, col=i%ncols+1,
    )

    # Most Likely Rt
    fig.add_trace(
        go.Scatter(
            x=result.index, y=result['ML'], 
            line_color='rgba(0,0,0,.2)', 
            marker={'size': 10,
                    'line': {'width': 1, 'color': 'rgb(50, 50, 50)'},
                    'color': result['ML'], 
                    'cmid': 1.0, 
                    'colorscale': 'RdYlGn', 
                    'reversescale': True},
            mode='lines+markers',
            showlegend=False,
            name='Rt'
        ),
        row=i//ncols+1, col=i%ncols+1,
    )
    
    # Add shape zeroline
    fig.add_shape(
        {'type': 'line', 
         'x0': PLOT_START, 
         'x1': result.index[-1]+pd.Timedelta(days=1), 
         'y0': 1.0, 
         'y1': 1.0, 
         'xref': 'x'+str(i+1), 'yref': 'y'+str(i+1), 
         'layer': 'below', 'opacity': .2}
    )
    
    return fig

def all_counties_view(final_results, counties):
    ''' Generate all counties Rt view
    '''
    # Plot all counties on a 4x3 grid
    ncols = 4
    nrows = int(np.ceil(len(final_results.keys()) / ncols))

    fig = make_subplots(rows=nrows, cols=ncols, subplot_titles=counties)
    fig.update_layout(template='plotly_white', 
                    height=800, 
                    width=1200)
    fig.update_yaxes(range = [0, 5])
    fig.update_xaxes(range = [
        PLOT_START,
        next(iter(final_results.values())).index[-1] + pd.Timedelta(days=1)
    ])

    for i, county in enumerate(counties):
        fig = plot_rt(final_results[county], county, 
                       fig, nrows=nrows, ncols=ncols, i=i)

    return fig

def new_cases_view(original, smoothed, county):
    ''' Create generic view of historical cases

        Paramters:
            original (pd.Series):
            smoothed (pd.Series):
            county (str):
        
        Returns:
            fig (go.Figure):
    '''
    # Use Plotly to plot daily new cases
    fig = go.Figure()

    fig.update_layout(template='plotly_white', 
                    height=600,
                    width=800,
                    title_text=f'{county} County covid-19 cases')

    fig.add_trace(
        go.Bar(
            x=original.index,
            y=original, 
            marker = {'color': 'rgb(200, 200, 200)', 'opacity': .5},
            name='Daily Cases',
        )
    )

    fig.add_trace(
        go.Scatter(
            x=original.index, 
            y=smoothed,                   
            mode='lines', 
            line_color='royalblue',
            name='Moving Average'
        )
    )

    return fig