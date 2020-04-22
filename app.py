import dash
from datetime import datetime
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from utils import load_cases, INCLUDE_COUNTIES
from views import all_counties_view

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Texas Rt Calculations'
server = app.server

# Calculate initial view for counties
df, final_results = load_cases()
fig = all_counties_view(final_results=final_results, 
                        counties=INCLUDE_COUNTIES)


app.layout = html.Div(children=[
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

    dcc.Graph(id='all-counties-view', figure=fig),

    dcc.Markdown(
        children='''
            Data from [Texas Dept of Health and Human Services]
            (https://dshs.texas.gov/coronavirus/additionaldata/)
        '''
    ),
])


if __name__ == '__main__':
    app.run_server(use_reloader=False)