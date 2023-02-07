import os
import time

from dash import html, dcc
from dash.dependencies import Input, Output, State
import base64
# Connect to main app.py file
import plotly.graph_objs as go
from generate import programm
from flask import Flask, send_from_directory
# Connect to your app pages
from pages import home,main
from urllib.parse import quote as urlquote
from components import grafpath
# Connect the navbar to the index
from components import navbar
import dash
import pandas as pd
import dash_bootstrap_components as dbc
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP,dbc.icons.FONT_AWESOME, dbc.icons.BOOTSTRAP,'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'], meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}],suppress_callback_exceptions=True)
nav = navbar.Navbar()
# Define the index page layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    nav,
    dcc.Store(id='store'),
    html.Div(id='page-content', children=[]),
])

cont404= html.Div([
        html.H1("4",style={'fontSize': '12em'}),html.H1("0:",style={'fontSize': '11em','transform':'rotate(-90deg)'}),html.H1("4",style={'fontSize': '12em'})
    ],
    style={
        "display": "flex",
        "justifyContent": "center",
        "alignItems": "center",
        "height": "90vh",
    }
)

# Create the callback to handle mutlipage inputs
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page1':
        return home.layout
    if pathname == '/page2':
        return main.layout
    else: # if redirected to unknown link
        return cont404

# Run the app on localhost:8050
@app.callback( Output("loading-demo", "children"),Output("my-output", "children"), Input('button', 'n_clicks'),[State('my-output', 'children')])
def run_script(n_clicks,text):
    if n_clicks > 0:
        init = programm()
        result = init.get_parse_data()
        init.create()
        tag_data = init.open()
        generated_data,num ,df = init.parse(result, tag_data)
        init.generate_exel(generated_data,df)
        grafpath.getdata()
    return ('',f"Данные от  {time.ctime(os.path.getmtime('./static/results.xlsx'))}")
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open
@app.callback(
    Output("loading-output", "children"),
    Output('hello', 'children'),
    Input('hello', 'children'),
)
def update_output(n):
    return "",grafpath.getRev()
@app.callback(
Output('AllDataGraf', 'children'),
Output('cat_list', 'children'),
Input('AllDataGraf', 'children'),
Input('cat_list', 'children'),
)
def upd(nd,nf):
    return grafpath.graf_main_2() ,grafpath.graf_main_1()
@app.callback(
Output('rev_ammount', 'children'),
Output('tag_stats', 'children'),
Input('rev_ammount', 'children'),
Input('tag_stats', 'children'),
)
def upd(nd,nf):
    return grafpath.graf_home_1(),grafpath.graf_home_2()
@app.callback(
    Output("modal-body-scroll", "is_open"),
    [
        Input("open-body-scroll", "n_clicks"),
        Input("close-body-scroll", "n_clicks"),
    ],
    [State("modal-body-scroll", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open




UPLOAD_DIRECTORY = "/tretafdtvd"


def save_file(name, content):
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
        fp.write(base64.decodebytes(data))


def uploaded_files():
    """List the files in the upload directory."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files


def file_download_link(filename):
    """Create a Plotly Dash 'A' element that downloads a file from the app."""
    location = "/download/{}".format(urlquote(filename))
    return html.A(filename, href=location)


@app.callback(
    Output("file-list", "children"),
    [Input("upload-data", "filename"), Input("upload-data", "contents")],
)
def update_output_upl(uploaded_filenames, uploaded_file_contents):
    """Save uploaded files and regenerate the file list."""

    if uploaded_filenames is not None and uploaded_file_contents is not None:
        for name, data in zip(uploaded_filenames, uploaded_file_contents):
            save_file(name, data)

    files = uploaded_files()
    if len(files) == 0:
        return [html.Li("No files yet!")]
    else:
        return [html.Li(file_download_link(filename)) for filename in files]




if __name__ == '__main__':
    app.run_server(debug=True)