import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
from dash import Dash, dcc, html, dash_table, Input, Output, callback, State
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Dash, html, dcc
import dash
import dash_bootstrap_components as dbc
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

import dash_html_components as html
import dash_bootstrap_components as dbc

divs = [html.Div(f"Div {i}") for i in range(1, 11)]

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(id="scrolling-divs", children=divs[:10], style={"overflow-y": "scroll"})
                    ],
                    width={"size": 12, "offset": 0},
                )
            ]
        )
    ]
)

@app.callback(
    Output("scrolling-divs", "children"),
    [Input("url", "pathname")],
    [State("scrolling-divs", "children")],
)
def update_divs(pathname, current_divs):
    current_page = int(pathname.split("/")[-1])
    start_index = (current_page - 1) * 5
    end_index = current_page * 5
    return divs[start_index:end_index]

if __name__ == "__main__":
    import plotly.express as px

    df = px.data.medals_long()
    print(df['medal'])
    print(df['count'])
    print(df['nation'])
    fig = px.bar(df, x="medal", y="count", color="nation",
                 pattern_shape="nation", pattern_shape_sequence=[".", "x", "+"])
    fig.show()
    #app.run_server(debug=True)
