import os
import time

import dash
from dash import Dash, dcc, html, dash_table, Input, Output, callback, State
import dash_bootstrap_components as dbc
import plotly.express as px
from dash_bootstrap_templates import load_figure_template
load_figure_template('SLATE')
from generate import programm
df = px.data.gapminder()
years = df.year.unique()
continents = df.continent.unique()

# stylesheet with the .dbc class
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = Dash(__name__, use_pages='' ,external_stylesheets=[dbc.themes.MATERIA,dbc.icons.FONT_AWESOME, dbc.icons.BOOTSTRAP,'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'], meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}])
dash.register_page(__name__,path='/home')

header = html.H4(
    "<Made by Deopster>", className="bg-primary text-white p-2 mb-2 text-center"
)
ells = html.Div([
    dcc.Dropdown(['заморозить столбцы', 'Заморозить первую строку', 'Добавить автофильтр'], 'Заморозить первую строку', multi=True,className="dash-bootstrap mb-2")
])


table = html.Div(
    dash_table.DataTable(
        id="table",
        columns=[{"name": i, "id": i, "deletable": True} for i in df.columns],
        data=df.to_dict("records"),
        page_size=10,
        editable=True,
        cell_selectable=True,
        filter_action="native",
        sort_action="native",
        style_table={"overflowX": "auto"},
        row_selectable="multi",
    ),
    className="dbc-row-selectable",
)

number_input = html.Div([
    dcc.Input(
            id="dtrue", type="number",
            debounce=False, placeholder="0 - все отзывы",className="dash-bootstrap p-1 rt"
        )
])
dropdown = html.Div([
    dcc.Dropdown( ["Новые", "Старые", "Популярные"],
            "Новые",
            id="indicator",className="dash-bootstrap")
])


radio = html.Div(

)

list_data = dbc.Row(
    [
        dbc.Col(html.Div(dropdown)),
        dbc.Col(html.Div(number_input)),
    ],className="mb-2"
)
slider = html.Div(
    [
        dbc.Label("Применить фильтр оценок отзывов"),
        dcc.RangeSlider(1, 5, 1, value=[1, 5],className="p-0")
    ],
    className="mb-4",
)
terminal= html.I(className="fas fa-terminal",style=dict(display='inline',color='white'))
reload= html.I(className="fas fa-redo",style=dict(display='inline',color='white'))
download = html.I(className="fas fa-arrow-down-to-line",style=dict(display='inline', color='white'))

row_content = [
    html.Div([
        dbc.Button(children=reload, id='button',type="reset", n_clicks=0, className="but",size='lg',color="info"),
        dbc.Button(children=download,href="/static/results.xlsx",download="my_data.xlsx",external_link=True, color="success",size="lg", className="but"),
 html.Div(
    [
        dbc.Button(children=terminal, color="dark", className="but",size="lg",id="open-body-scroll", n_clicks=0),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Web Terminal")),
                dbc.ModalBody("Test output\nnext line",style={'color':'white','background-color':'black'}),
                dbc.ModalFooter(
                    dbc.Button(
                        "Send",
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
),
],className="pb-3",style={'float': 'right', 'display':'flex'})
]


buttonrow= html.Div(
        row_content,
)
#buttonrow= dbc.Card([],className=["mb-3"])
stateline = dbc.Card(
                    [
                        dbc.Row([
                                dbc.Card([
                                    dbc.CardBody(id='my-output',children='Первичная загрузка',className='p-1'),
                            ],style={'diplay':'block'},id='block_1'),
                        ], className="p-2"),
                    ],className=["mb-3"]
                )
controls = dbc.Card(
    [list_data, ells, slider],
    body=True,
)
template = "SLATE"
import plotly.graph_objects as go
fig = go.Figure()
fig.update_layout(template=template, title="Mt Bruno Elevation")
#fig.show()
tab1 = dbc.Tab([dcc.Graph(id="line-chart")], label="Line Chart")
tab2 = dbc.Tab([dcc.Graph(id="scatter-chart")], label="Scatter Chart")
tab3 = dbc.Tab([table], label="Table", className="p-0")
tabs = dbc.Card(dbc.Tabs([tab1, tab2, tab3]))

app.layout = dbc.Container(
    [
        header,
        dbc.Row(
            [

                dbc.Col(
                    [
                dbc.Row(
                    [
                        buttonrow,
                    ],
                ),
                        dbc.Row(
                            [
                                stateline,
                            ]
                        ),

                dbc.Row(
                    [
                        controls,
                    ],
                ),
                        ],md=4,className="left_column"),
                dbc.Col(tabs, md=8,className="right_column"),
            ],style={'marginLeft':'0'}
        ),
        dcc.Loading([html.Div(id="loading-demo")],fullscreen=True,type='cube',style={'backgroundColor': 'black'}),
    ],
    fluid=True,
    className="dbc",
)

@app.callback(Output("loading-demo", "children"),Output("my-output", "children"), Input('button', 'n_clicks'),[State('my-output', 'children')])
def run_cript(n_clicks,text):
    num = 'Temp for future replace'
    if n_clicks > 0:
        print(n_clicks)
        init = programm()
        result = init.get_parse_data()
        init.create()
        tag_data = init.open()
        generated_data,num = init.parse(result, tag_data)
        init.generate_exel(generated_data)
    return ('',f"{str(num)} matches were found, data from  {time.ctime(os.path.getmtime('./static/results.xlsx'))}")
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