from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Show plots since the start of reliable test results
PLOT_START = pd.Timestamp(year=2020, month=3, day=16)

def plot_rt(result, fig, nrows=1, ncols=1, i=0):
    ''' Plot individual counties Rt values along with shaded 80% confidence
        intervals

        Paramters:
            result (pd.Series): Calculated Rt values for a given county
            fig (go.Figure): Plotly figure with subplots
            nrows (int): Number of rows in plotly figure
            ncols (int): Number of columns in plotly figure
            i (int): Index of subplot to add Rt traces to, zero-indexed
        
        Returns:
            fig (go.Figure): Modified Plotly figure
    '''
    # 80% Confidence shading
    fig.add_trace(
        go.Scatter(
            x=result.index.append(result.index[::-1]),
            y=np.append(result['High_80'].values, result['Low_80'].values[::-1]),
            fill='toself',
            fillcolor='rgba(0, 0, 0, 0.1)',
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
            marker={'size': 9,
                    'line': {'width': 0.5, 'color': 'rgba(0, 0, 0, 0.4)'},
                    'color': result['ML'], 
                    'cmin': 0.75,
                    'cmid': 1.0,
                    'cmax': 1.25, 
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
    ''' Generate all counties view of calculated Rt value

        Paramters:
            final_results (dict[str: pd.DataFrame]): Dict with keys as county names, 
                values as DataFrame of Rt and 80% confidence bounds by day
            counties (list): List of county names
        
        Returns:
            fig (go.Figure): Modified Plotly figure
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
        fig = plot_rt(final_results[county], fig,
                      nrows=nrows, ncols=ncols, i=i)

    return fig

def plot_new_cases(cases, fig):
    ''' Adds a subplot to the given figure containing a bar chart of
        raw cases counts as well as a 7-day moving average

        Paramters:
            cases (pd.Series): Time series of cumulative reported cases
            fig (go.Figure): Plotly figure with one column and two rows 
                of subplots, function modifies the bottom subplot
        
        Returns:
            fig (go.Figure): Modified Plotly figure
    '''
    new_cases = cases.diff()

    smoothed = new_cases.rolling(7,
        win_type='gaussian',
        min_periods=1,
        center=True).mean(std=2).round()

    fig.add_trace(
        go.Bar(
            x=cases.index,
            y=new_cases, 
            marker = {'color': 'rgb(200, 200, 255)', 'opacity': .5},
            name='Daily Cases',
        ),
        row=1, col=2,
    )

    fig.add_trace(
        go.Scatter(
            x=cases.index, 
            y=smoothed,                   
            mode='lines', 
            line_color='royalblue',
            name='Moving Average'
        ),
        row=1, col=2,
    )

    return fig

def county_detail_view(result, cases, area):
    ''' Created a county-by-county view, with a plot of Rt on top 
        and a view of reported cases on bottom

        Paramters:
            result (pd.Series): Calculated Rt values for a given county
            cases (pd.Series): Time series of cumulative reported cases
            area (str): Name of metro area
            fig (go.Figure): Plotly figure with one column and two rows 
                of subplots, function modifies the bottom subplot
        
        Returns:
            fig (go.Figure): Modified Plotly figure


    '''
    # Build subplot framework
    fig = make_subplots(
        rows=1, 
        cols=2, 
        horizontal_spacing=0.04,
        vertical_spacing=0.15,
        subplot_titles=[
            f'{area} Area Rt', 
            f'{area} Area New Cases'
        ]
    )
    fig.update_layout(
        template='plotly_white', 
        height=400, 
        width=950,
        margin={'l': 5, 't': 50, 'r': 5, 'b': 50},
        font={'color': 'rgb(0,0,0)'},
        titlefont={'size': 12},
        yaxis1={'range': [.5, 1.5]}, 
        yaxis2={'range': [0, 1500]},
        showlegend=False,
    )
    fig.update_xaxes(
        range = [
            PLOT_START,
            result.index[-1] + pd.Timedelta(days=1),
        ],
        tickformat = '%m/%d'
    )

    # Fill with county Rt view on top, reported cases on bottom
    fig = plot_rt(result=result, fig=fig, ncols=2, i=0)
    fig = plot_new_cases(cases=cases, fig=fig)

    return fig