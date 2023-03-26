import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
accordion = html.Div(
    dbc.Accordion(
        [
            dbc.AccordionItem(
                "This is the content of the first section", title=dbc.Button(children="ffdf", id='del', n_clicks=0,size='md',color="info",className="mt-2")
            ),
            dbc.AccordionItem(
                "This is the content of the second section", title="Item 2"
            ),
            dbc.AccordionItem(
                "This is the content of the third section", title="Item 3"
            ),
        ],
        flush=True,
    ),
)
app.layout = html.Div(accordion)
if __name__ == '__main__':
    app.run_server(debug=True)