from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import numpy as np

PLOT_START = pd.Timestamp('2020-03-24')

def plot_rt(result, name, fig, nrows=1, ncols=1, i=0):
    # 80% Confidence shading
    fig.add_trace(
        go.Scatter(
            x=result.index.append(result.index[::-1]),
            y=np.append(result['High_80'].values, result['Low_80'].values[::-1]),
            fill='toself',
            fillcolor='rgba(0, 0 , 0, 0.1)',
            line_color='rgba(255,255,255,0)',
            showlegend=False,
            name='80% Confidence Interval'
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

    fig = make_subplots(
        rows=nrows, 
        cols=ncols, 
        horizontal_spacing=0.04,
        vertical_spacing=0.1,
        subplot_titles=counties
    )
    fig.update_layout(
        template='plotly_white', 
        height=800, 
        width=1000,
        margin={'l': 5, 't': 50, 'r': 5, 'b': 50},
        font={'color': 'rgb(0,0,0)'},
        titlefont={'size': 12},
    )
    fig.update_yaxes(range = [.5, 1.5])
    fig.update_xaxes(
        range = [
            PLOT_START,
            next(iter(final_results.values())).index[-1] + pd.Timedelta(days=1),
        ],
        tickformat = '%m/%d'
    )

    for i, county in enumerate(counties):
        fig = plot_rt(final_results[county], county, 
                       fig, nrows=nrows, ncols=ncols, i=i)

    return fig

def plot_new_cases(result, name, fig):
    ''' Create generic view of historical cases

        Paramters:
            original (pd.Series):
            smoothed (pd.Series):
            county (str):
        
        Returns:
            fig (go.Figure):
    '''
    new_cases = result.diff()

    smoothed = new_cases.rolling(7,
        win_type='gaussian',
        min_periods=1,
        center=True).mean(std=2).round()

    fig.add_trace(
        go.Bar(
            x=result.index,
            y=new_cases, 
            marker = {'color': 'rgb(200, 200, 255)', 'opacity': .5},
            name='Daily Cases',
        ),
        row=2, col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=result.index, 
            y=smoothed,                   
            mode='lines', 
            line_color='royalblue',
            name='Moving Average'
        ),
        row=2, col=1,
    )

    return fig

def county_detail_view(df, final_results, county):
    ''' County-by-county view
    '''

    fig = make_subplots(
        rows=2, 
        cols=1, 
        horizontal_spacing=0.04,
        vertical_spacing=0.15,
        subplot_titles=[
            f'{county} County Rt', 
            f'{county} County New Cases'
        ]
    )
    fig.update_layout(
        template='plotly_white', 
        height=800, 
        width=600,
        margin={'l': 5, 't': 50, 'r': 5, 'b': 50},
        font={'color': 'rgb(0,0,0)'},
        titlefont={'size': 12},
        yaxis1={'range': [.5, 1.5]},
        showlegend=False,
    )
    fig.update_xaxes(
        range = [
            PLOT_START,
            next(iter(final_results.values())).index[-1] + pd.Timedelta(days=1),
        ],
        tickformat = '%m/%d'
    )

    fig = plot_rt(final_results[county], county, 
                  fig, nrows=2, i=0)
    fig = plot_new_cases(df.loc[county], county, fig)

    return fig