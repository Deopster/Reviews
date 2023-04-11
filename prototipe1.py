import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
icon = html.I(className='fas fa-arrow-alt-circle-right')
but=dbc.Button(
    [
        html.I(className='bi bi-plus'),  # иконка плюса
        '+',  # текст кнопки
    ],
    color='primary',  # цвет кнопки
    className='m-3',  # дополнительный CSS класс для настройки отступов
    size='sm',  # размер кнопки
    id='add-field',
    n_clicks=0,
    style={'flex': 1,'max-width':'40px'}
)
app.layout = html.Div([
html.Div(children=[html.Div(children=html.H4("fdfdfdf"), style={'flex': 1,'max-width':'100px'}),but,icon,dbc.Input(type='text',placeholder='Название поля для записи', style={'flex': 1,'max-width':'250px','min-width':'250px'})
        ],id='form-container',style={
        'display': 'flex',
        'flex-wrap': 'wrap',
        'justify-content': 'flex-start',
        'align-items': 'center',
    }),mva
])

@app.callback(
    Output('form-container', 'children'),
    [Input('add-field', 'n_clicks')],
    [State('form-container', 'children')]
)
def add_field(n_clicks, children):
    if n_clicks!=0:
        new_field = dbc.Input(type='text', style={'flex': 1,'max-width':'250px'})
        children.insert(len(children)-3,new_field)
    return children

if __name__ == '__main__':
    app.run_server(debug=True)