import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
from dash import Dash, dcc, html, dash_table, Input, Output, callback, State
import plotly.express as px
import dash_bootstrap_components as dbc
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = Dash(__name__, external_stylesheets=[dbc.themes.LUX,dbc.icons.FONT_AWESOME, dbc.icons.BOOTSTRAP])

modal = html.Div(
    [
        dbc.Button(children="dfdf",download='results.xlsx',external_link=True,href="results.xlsx",),
        dbc.Button(
            "Modal with scrollable body", id="open-body-scroll", n_clicks=0
        ),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Modal with scrollable body")),
                dbc.ModalBody("fdfdsfsdf",style={'color':'red','background-color':'black'}),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close",
                        id="close-body-scroll",
                        className="ms-auto",
                        n_clicks=0,
                    )
                ),
            ],
            id="modal-body-scroll",
            scrollable=True,
            is_open=False,
            fullscreen=True
        ),
    ]
)
app.layout = dbc.Container(
    [
        modal
]
)


def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


app.callback(
    Output("modal-body-scroll", "is_open"),
    [
        Input("open-body-scroll", "n_clicks"),
        Input("close-body-scroll", "n_clicks"),
    ],
    [State("modal-body-scroll", "is_open")],
)(toggle_modal)
if __name__ == "__main__":
    app.run_server(debug=True)