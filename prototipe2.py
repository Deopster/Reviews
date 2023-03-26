import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
select = html.Div(
    dbc.Select(
        ["простое тегирование", "Тегирование ключ-слово", "сканирование","перебор"],
        "простое тегирование",
        id="shorthand-select",
    ),
    className="py-2 mb-2",
)

app.layout = html.Div([
    dbc.ListGroup(children=[dbc.ListGroupItem("+ Добавить",id='add-field',action=True),dbc.ListGroupItem(dbc.Input(type='text',placeholder='Название поля для записи', ))
        ],id='form-container',flush=False),
])

@app.callback(
    Output('form-container', 'children'),
    [Input('add-field', 'n_clicks')],
    [State('form-container', 'children')]
)
def add_field(n_clicks, children):
    if n_clicks!=0:
        new_field = dbc.ListGroupItem(select)
        children.insert(len(children)-2,new_field)
    return children

if __name__ == '__main__':
    app.run_server(debug=True)