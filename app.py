import dash
from datetime import datetime
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from utils import load_cases
from views import all_counties_view, county_detail_view


# Main app settings
app = dash.Dash(
    __name__, 
    external_stylesheets=['assets/bWLwgP.css']
)
server = app.server
app.title = 'Texas Rt Calculations'
app.config.suppress_callback_exceptions = True
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Load raw data and get county list
df, final_results = load_cases()
counties = [k for k, v in final_results.items() 
            if k != 'timestamp']

all_counties_fig = all_counties_view(
        final_results=final_results, 
        counties=counties
)
county_detail_fig = county_detail_view(
        result=final_results[counties[0]], 
        cases=df.loc[counties[0]], 
        county=counties[0]
)


# Main page layout
main_layout = html.Div(children=[
    html.H1(children='Texas Covid-19 Rt'),

    dcc.Markdown(
        children='''
            Calculated below are up-to-date values for the covid-19 effective reproduction 
            number __Rt__ in Texas counties using Kevin Systrom's methodology as described in [this notebook]
            (https://github.com/k-sys/covid-19/blob/master/Realtime%20Rt%20mcmc.ipynb) and deployed at 
            [Rt.live](https://rt.live/). __Rt__ is a measure of how fast the outbreak is spreading, 
            when it is greater than 1.0 the disease will spread rapidly, when it is below 1.0 the 
            daily number of new cases will decrease. The data is displayed for the 12 Texas counties with 
            the highest case counts.  

            For a detailed view of individual counties go [here](/detail).
        ''',
        style = {'max-width': 1000}
    ),

    html.Div(
        children=[
            html.Br(),
            html.P(
                'Data Updated: ' + datetime.strftime(
                final_results['timestamp'], '%m/%d %I:%M %p'),
                style = {
                    'background-color': 'GhostWhite', 
                    'align-items': 'center',
                    'width': 225,
                    }
            ),
        ]
    ),

    dcc.Graph(id='all-counties-view', figure=all_counties_fig),

    dcc.Markdown(
        children='''
            Data from [Texas Dept of Health and Human Services]
            (https://dshs.texas.gov/coronavirus/additionaldata/)
        '''
    ),
])


# County detail page layout
detail_layout = html.Div(children=[
    html.H1(children='Texas Covid-19 Rt'),

    dcc.Markdown(
        children='''
            Below is a county-specific view of Rt as well as the confirmed cases 
            reported by day. The 7-day rolling average of new cases is displayed in blue. 

            For a view of all counties go back to the [top level](/).
        ''',
        style = {'max-width': 1000}
    ),

    html.Div(
        children=[
            html.Br(),
            html.P(
                'Data Updated: ' + datetime.strftime(
                final_results['timestamp'], '%m/%d %I:%M %p'),
                style = {
                    'background-color': 'GhostWhite', 
                    'align-items': 'center',
                    'width': 225,
                    }
            ),
            html.Br(),
        ]
    ),

    dcc.Dropdown(
        id='county-dropdown',
        options=[{'label': c, 'value': c} for c in counties],
        value=counties[0],
        style={'width': 225}
    ),

    dcc.Graph(id='county-detail-view', figure=county_detail_fig),

    dcc.Markdown(
        children='''
            Data from [Texas Dept of Health and Human Services]
            (https://dshs.texas.gov/coronavirus/additionaldata/)
        '''
    ),
])


# Broken route layout
error_layout = html.Div(children=[
    dcc.Markdown(
        children='''
            Whoops! Something went wrong, go back to the [top level](/).
        '''
    ),
])


# Main routing callback
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return main_layout
    elif pathname == '/detail':
        return detail_layout
    else:
        return error_layout


# Detail page callback
@app.callback(Output('county-detail-view', 'figure'),
              [Input('county-dropdown', 'value')])
def callback_detail_view(value):
    return county_detail_view(result=final_results[value], 
                              cases=df.loc[value], 
                              county=value)


if __name__ == '__main__':
    app.run_server(port=8050, host='127.0.0.1', use_reloader=False)