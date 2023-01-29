from dash import Dash, dcc, html, Input, Output, State
from func import transform, predict
from process_input import read_input
import base64
import uuid
import os
import flask

app = Dash(__name__)

test_png = 'figs/schrodingersduck.png'
test_base64 = base64.b64encode(open(test_png, 'rb').read()).decode('ascii')

app.layout = html.Div([
    html.Img(src='data:image/png;base64,{}'.format(test_base64), style={'height':'25%', 'width':'25%'}),
    html.Br(),
    html.H6("qSpam, TEAM Ytterbium @ iQuHack 2023."),
    html.Br(),
    html.Div(dcc.Input(id='input-on-submit', type='text')),
    html.Button('Submit', id='submit-val', n_clicks=0),
    html.Br(),
    html.Div(id='container-button-basic',
             children='Enter a value and press submit')
])


@app.callback(
    Output('container-button-basic', 'children'),
    Input('submit-val', 'n_clicks'),
    State('input-on-submit', 'value')
)
def update_output(n_clicks, value):
    tmp = read_input(value)
    output = predict(tmp)
    return 'Spam!' if output == 1 else "Not spam"

if __name__ == '__main__':
    app.run_server(debug=True)
