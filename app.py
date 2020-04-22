import dash
from datetime import datetime
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from utils import load_cases, INCLUDE_COUNTIES
from views import all_counties_view, county_detail_view

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = 'Texas Rt Calculations'
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Calculate initial view for counties
df, final_results = load_cases()
all_counties_fig = all_counties_view(final_results=final_results, 
                        counties=INCLUDE_COUNTIES)
county_detail_fig = county_detail_view(df=df, 
                        final_results=final_results, 
                        county=INCLUDE_COUNTIES[0])


main_layout = html.Div(children=[
    html.H1(children='Texas Covid-19 Rt'),

    dcc.Markdown(
        children='''
            Calculated below are up-to-date values for the covid-19 effective reproduction 
            number __Rt__ in Texas counties using Kevin Systrom's methodology as described in [this notebook]
            (https://github.com/k-sys/covid-19/blob/master/Realtime%20R0.ipynb) and deployed at 
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
        options=[{'label': c, 'value': c} for c in INCLUDE_COUNTIES],
        value=INCLUDE_COUNTIES[0],
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


# Main routing
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return main_layout
    elif pathname == '/detail':
        return detail_layout
    else:
        return main_layout

# Detail page callbacks
@app.callback(Output('county-detail-view', 'figure'),
              [Input('county-dropdown', 'value')])
def callback_detail_view(value):
    return county_detail_view(df=df, 
                        final_results=final_results, 
                        county=value)

if __name__ == '__main__':
    app.run_server(use_reloader=False)