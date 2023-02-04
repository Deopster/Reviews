import os
import time

from dash import html, dcc
from dash.dependencies import Input, Output, State

# Connect to main app.py file
from app import app
from generate import programm

# Connect to your app pages
from pages import page1, page2,home,main

# Connect the navbar to the index
from components import navbar
import dash
import dash_bootstrap_components as dbc
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP,dbc.icons.FONT_AWESOME, dbc.icons.BOOTSTRAP,'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'], meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}],suppress_callback_exceptions=True)

# Define the navbar
nav = navbar.Navbar()

# Define the index page layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    nav,
    html.Div(id='page-content', children=[]),
])

# Create the callback to handle mutlipage inputs
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page1':
        return home.layout
    if pathname == '/page2':
        return main.layout
    else: # if redirected to unknown link
        return "404 Page Error! Please choose a link"

# Run the app on localhost:8050
@app.callback(Output("loading-demo", "children"),Output("my-output", "children"), Input('button', 'n_clicks'),[State('my-output', 'children')])
def run_script(n_clicks,text):
    num = 'Temp for future replace'
    if n_clicks > 0:
        print(n_clicks)
        print(n_clicks)
        init = programm()
        result = init.get_parse_data()
        init.create()
        tag_data = init.open()
        generated_data,num ,df = init.parse(result, tag_data)
        init.generate_exel(generated_data,df)

    return ('',f"Данные от  {time.ctime(os.path.getmtime('./static/results.xlsx'))}")
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open
@app.callback(
    Output("loading-output", "children"),
    Output('hello', 'children'),
    [Input('input-id', 'value')],
    [State('input-id', 'id')]
)
def update_output(input_value, input_id):
    global items
    if input_id:
        while True:
            try:
                print("Вхождение")
                NANI = programm()
                dat = NANI.get_parse_data()
                items = [i['content'] for i in dat]
            except ConnectionResetError:
                print("Наебнулось")
                continue
            except Exception:
                print("Наебнулось иначе")
                continue
            break

    return "",[dbc.ListGroupItem(item) for item in items]
if __name__ == '__main__':
    app.run_server(debug=True)