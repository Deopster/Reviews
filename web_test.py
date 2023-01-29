import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
from dash import Dash, dcc, html, dash_table, Input, Output, callback, State
import plotly.express as px
import dash_bootstrap_components as dbc
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = Dash(__name__, external_stylesheets=[dbc.themes.LUX,dbc.icons.FONT_AWESOME, dbc.icons.BOOTSTRAP])
app.layout = html.Div([
    html.Div(
        className='col-12',
        children=[
            dcc.FlexBox(
                id='flex-container',
                children=[
                    dcc.Graph(id='graph1'),
                    dcc.Graph(id='graph2'),
                    dcc.Graph(id='graph3'),
                ],
                flex='row',
                align='start',
                justify='start'
            )
        ]
    )
])
if __name__ == "__main__":
    app.run_server(debug=True)