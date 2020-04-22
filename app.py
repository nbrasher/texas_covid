import dash
from datetime import datetime
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from utils import load_cases, INCLUDE_COUNTIES
from views import all_counties_view

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Calculate initial view for counties
df, final_results = load_cases()
fig = all_counties_view(final_results=final_results, 
                        counties=INCLUDE_COUNTIES)


app.layout = html.Div(children=[
    html.H1(children='Texas Covid-19'),

    html.H6(
        children='Data Updated: ' + datetime.strftime(
            final_results['timestamp'], '%m/%d %I:%M %p')
    ),

    html.Div(
        children='''
            These are up-to-date values for Rt, a key measure of how fast the virus 
            is growing. It’s the average number of people who become infected by an
            infectious person. If Rt is above 1.0, the virus will spread quickly. 
            When Rt is below 1.0, the virus will stop spreading.
        ''',
        style={'width': 750}
    ),

    dcc.Graph(id='all-counties-view', figure=fig),
])


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)