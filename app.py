import os
import time

from dash import html, dcc, callback_context
from dash.dependencies import Input, Output, State
import base64
# Connect to main app.py file
import plotly.graph_objs as go
from dash.exceptions import PreventUpdate

import components.params
import scan
import web_test
from generate import programm
from flask import Flask, send_from_directory
# Connect to your app pages
from pages import home,main,auth,custom
from urllib.parse import quote as urlquote
from components import grafpath
# Connect the navbar to the index
from components import navbar,filelist
import dash

import dash_bootstrap_components as dbc
server = Flask(__name__)
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP,dbc.icons.FONT_AWESOME, dbc.icons.BOOTSTRAP,'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'], meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}],suppress_callback_exceptions=True, server=server)
nav = navbar.Navbar()
# Define the index page layout
app.config.suppress_callback_exceptions = True
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

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page2':
        return main.layout
    elif pathname == '/page1':
        return home.layout
    elif pathname == '/page3':
        return custom.layout
    elif pathname =='/':
        return auth.layout
    else: # if redirected to unknown link
        return cont404





@app.callback(
    Output("toggle-modal-1", "is_open"),
    [
        Input("open-lg-new", "n_clicks"),
        Input("open-toggle-modal-1", "n_clicks"),
        Input("open-toggle-modal-2", "n_clicks"),
    ],
    [State("toggle-modal-1", "is_open")],
)
def toggle_modal_1(n0, n1, n2, is_open):
    if n0 or n1 or n2:
        return not is_open
    return is_open


@app.callback(
    Output("toggle-modal-2", "is_open"),
    [
        Input("open-toggle-modal-2", "n_clicks"),
        Input("open-toggle-modal-1", "n_clicks"),
    ],
    [State("toggle-modal-2", "is_open")],
)
def toggle_modal_2(n2, n1, is_open):
    if n1 or n2:
        return not is_open
    return is_open




@app.callback( Output("loading-demo", "children"),Output("my-output", "children"), Input('button', 'n_clicks'),[State('my-output', 'children'),State("old-new", 'value')])
def run_script(n_clicks,text,state):
    if n_clicks > 0:
        print("Приложение",state)
        if len(state)==1:
            application = 'com.bank.domrf.v2'
        else:
            application = 'com.bssys.roscapretail'

        init = programm(appl=application)
        result = init.get_parse_data()
        init.create()
        tag_data = init.open()
        generated_data ,df = init.parse(result, tag_data)
        init.generate_exel(generated_data,df)
        web_test.test("df",'Отзыв',0.8,'./static/results.xlsx',"rety.xlsx")
        grafpath.getdata()
    return ('',f"Данные от  {time.ctime(os.path.getmtime('./static/results.xlsx'))}")
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    Output('hello', 'children'),
    Input('hello', 'children'),
    Input('ser', 'n_clicks'),
)
def update_output_1(n,dat):
    return grafpath.getRev()
@app.callback(
Output('AllDataGraf', 'children'),
Output('cat_list', 'children'),
Input('AllDataGraf', 'children'),
Input('cat_list', 'children'),
)
def updj(nd,nf):
    return grafpath.graf_main_2() ,grafpath.graf_main_1()
@app.callback(
Output('rev_ammount', 'children'),
Output('tag_stats', 'children'),
Output('cat_stats', 'children'),
Input('rev_ammount', 'children'),
Input('tag_stats', 'children'),
)
def upd(nd,nf):
    return grafpath.graf_home_1(),grafpath.graf_home_2(),grafpath.graf_home_3()
@app.callback(
Output('rev_stats', 'children'),
Input('cat_chose_holder', 'value'),
)
def upd(nd):
    return grafpath.graf_home_4(nd)
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
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
        fp.write(base64.decodebytes(data))


def uploaded_files():
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files


def file_download_link(filename):
    location = "/download/{}".format(urlquote(filename))
    return html.A(filename, href=location)


@app.callback(
    Output("file-list", "children"),
    [Input("upload-data", "filename"), Input("upload-data", "contents")],
)
def update_output_upl(uploaded_filenames, uploaded_file_contents):
    if uploaded_filenames is not None and uploaded_file_contents is not None:
        for name, data in zip(uploaded_filenames, uploaded_file_contents):
            save_file(name, data)

    files = uploaded_files()
    if len(files) == 0:
        return [html.Li("No files yet!")]
    else:
        return [html.Li(file_download_link(filename)) for filename in files]
dell= html.I(className="fas fa-trash",style=dict(display='inline',color='white'))
@app.callback(
    Output('form-container', 'children'),
    [Input('del', 'n_clicks'),Input('add-field', 'n_clicks')],
    [State('form-container', 'children')]
)
def add_field(n_clicks,tar, children):
    #print(dash.callback_context.triggered)
    if n_clicks is None:
        raise PreventUpdate
    else:
        #print(dash.callback_context.triggered[0])
        if dash.callback_context.triggered[0]['prop_id']=='add-field.n_clicks':
            new_field = dbc.ListGroupItem(dbc.Col([
                        dbc.Row([
                            dbc.Col(dbc.Select(
        ["Простое тегирование - поиск совпадений", "Тегирование - разделение по категориям", "Сканирование - сравнение построчно","перебор","график"],
        "Простое тегирование - поиск совпадений",
        id=f"chose_v{str(len(children)-2)}"
    ),className="mb-2",md=10,style={'paddingRight':'0','paddingLeft':'0'}),dbc.Col(dbc.Button(children=dell, id='del', n_clicks=0,size='md',color="info",className="mb-2"),md=2)
                        ]),
                        dbc.Row(children="",id=f'cont{str(len(children)-2)}')
                ],id=f'panal{str(len(children)-1)}')
            )
            children.insert(len(children)-1,new_field)
        elif dash.callback_context.triggered[0]['prop_id']=='del.n_clicks':
            children.pop(len(children)-2)
        return children
for i in range(10):
    @app.callback(
        Output(f'cont{str(i)}', 'children'),
        Input(f'chose_v{str(i)}', 'value'),
    )
    def change(name):
        #print(name)
        if name=='Простое тегирование - поиск совпадений':
            return components.params.simple
        elif name=='Тегирование - разделение по категориям':
            return components.params.tag_key
        elif name=="Сканирование - сравнение построчно":
            return components.params.scan


def save_file(name, content):
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
        fp.write(base64.decodebytes(data))


def uploaded_files():
    """List the files in the upload directory."""
    files = []
    #print(os.getcwd())
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
    Output("file-list1", "children"),
    [Input("upl_file", "filename"), Input("upl_file", "contents")],
)
def update_output(uploaded_filenames, uploaded_file_contents):
    """Save uploaded files and regenerate the file list."""
    #print("ДА")
    if uploaded_filenames is not None and uploaded_file_contents is not None:
        for name, data in zip(uploaded_filenames, uploaded_file_contents):
            save_file(name, data)

    files = uploaded_files()
    if len(files) == 0:
        return [html.Li("Пока нет файлов")]
    else:
        return [dbc.ListGroupItem( obj, id="button-item", n_clicks=0, action=True, active=True) for obj in files]

for i in range(5):
    @app.callback(
        Output(f"item_chose{str(i)}","active"),
        [Input(f"item_chose{str(i)}", "n_clicks"),Input(f"item_chose{str(i)}", "children"),Input(f"item_chose{str(i)}", "active")]
    )
    def say(m,a,s):
        #print(m,a,s)
        if m == 0:
            return dash.no_update
        else:
            if s is True:
                return False
            else:
                return True

# @app.callback(
#     Output("scan_col","children"),
#     [Input("add_scan","n_clicks")],
#     [State('scan_col', 'children')]
# )
#
# def some(n_clicks,s):
#     #print(n_clicks,s)
#     if n_clicks is None:
#         raise PreventUpdate
#     else:
#         s.append(
#             dbc.Row([
#                 dbc.Col(mvt, md=5),
#                 dbc.Col(sel, md=3),
#                 dbc.Col(dbc.Input(placeholder="Значение", type="text"), md=4),
#             ]),
#         )
#         print(s)
#         return s

@app.callback(
    Output("open-toggle-modal-2", "disabled"),
    [Input(f"item_chose{str(i)}", "n_clicks")for i in range(len(filelist.files_()))]
)
def say(*args):
    if sum(args) == 0:
        return dash.no_update
    else:
        return False

@app.callback(Output('file_name_card', 'children'),
              #Output("file_names_drop","options"),
              [Input('open-toggle-modal-2', 'n_clicks')])
def update_random_number(n):
    print("fdfdf")
    filelist.read_file()
    return f"в файле {filelist.getfile_name()} найдено {len(filelist.getfile().keys())} столбцов и {len(filelist.getfile())} строк" #,filelist.getfile().keys()
chose1 = dbc.Card(
    dbc.CardBody(html.Div([
        dcc.Dropdown(options= grafpath.Get_keys(),
        value=grafpath.Get_keys()[0],
        id="cat_chose_1",
        className="dash-bootstrap",
        clearable=False
                )
    ]))
                )
download = html.I(className="fas fa-cloud-download",style={'textAlign': 'center','verticalAlign': 'bottom','display':'inline'})
body1=dbc.Row(dbc.Button(children=download,href="/static/fin.xlsx",download="my_data.xlsx",external_link=True, color="success",size="lg", className="but"))
# body1 = dbc.Row([
#     dbc.Col([dbc.Row(chose1),dbc.Row(children=grafpath.graf_cust("Банк"),id="new_field")]),
#     dbc.Col()
# ])

@app.callback(
    Output("alert-warn", "is_open"),
    Output("my-store", "data"),
    Output("the_view","children"),
    [Input("start", 'n_clicks')],[State('form-container', 'children')]
)
def save_field_values(a,m):
    if a ==0:
        return dash.no_update
        print("Сохранён")
    #print(m)
    obr = {}
    for i in range(len(m)-1):
        tempval=[]
        #print('новое')
        zna= m[i]['props']['children']['props']['children'][0]['props']['children'][0]['props']['children']['props']['value']
        if zna == 'Тегирование - разделение по категориям':
            for n in m[i]['props']['children']['props']['children'][1]['props']['children']['props']['children']['props']['children']:
                #print(i)
                if n['type'] == 'Label':
                    pass
                else:
                    try:
                        #print(n['props']['value'])
                        tempval.append(n['props']['value'])
                    except KeyError:
                        #tempval.append("пусто")
                        return True, [],[]
        if zna == "Сканирование - сравнение построчно":
            for n in  m[i]['props']['children']['props']['children'][1]['props']['children']['props']['children']['props']['children']:
                #print("\n",n,"\n")
                if type(n['props']['children']) is list:
                    temp=[]
                    for inlist in n['props']['children']:
                        try:
                            # print(n['props']['value'])
                            temp.append(inlist['props']['children']['props']['value'])
                        except KeyError:
                            # tempval.append("пусто")
                            return True, [],[]
                        #print(inlist['props']['children']['props'])
                    tempval.append(temp)
        obr[zna]=tempval
    if 'Сканирование - сравнение построчно' in obr.keys():
        print("Вхождение сканирование")
        scan.scan(obr['Сканирование - сравнение построчно'])
    if 'Тегирование - разделение по категориям' in obr.keys():
        print("Вхождение тегирование")
        print(obr['Тегирование - разделение по категориям'])
        if len(obr.keys())>1:
            filename_send="./temp.xlsx"
        else:
            filename_send=f"./static/{filelist.getfile_name()}"
        web_test.test(obr['Тегирование - разделение по категориям'][4],obr['Тегирование - разделение по категориям'][1],obr['Тегирование - разделение по категориям'][3],filename_send,"./static/fin.xlsx")
        #print("\n",ell)
        #print("\n/\n")

    return False,list(m),body1

@app.callback(
Output("new_field","children"),
Input('cat_chose_1', 'value'),
)
def upd(nd):
    return grafpath.graf_cust(nd)
if __name__ == '__main__':
    app.run_server(debug=True)