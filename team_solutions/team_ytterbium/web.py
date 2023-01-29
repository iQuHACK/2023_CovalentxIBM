import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import base64
from func import *

import uuid
import os
import flask
stylesheets = [
    "https://cdnjs.cloudflare.com/ajax/libs/bulma/0.7.2/css/bulma.min.css",
]

# create app
app = dash.Dash(
    __name__,
    external_stylesheets=stylesheets
)


@app.callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='my-input1', component_property='value')
        )
def update_output_div(input_value):
    output = transform(input_value)
    return f'Result: {output}'

test_png = 'figs/schrodingersduck.png'
test_base64 = base64.b64encode(open(test_png, 'rb').read()).decode('ascii')

app.layout = html.Div([
    html.Img(src='data:image/png;base64,{}'.format(test_base64), style={'height':'50%', 'width':'50%'}),
    html.Br(),
    html.H6("PROJECT NAME, TEAM Ytterbium @ iQuHack 2023."),
    html.Br(),
    html.Div([
        "Enter email below:",
        dcc.Textarea(
            id="my-input1",
            className="textarea",
            placeholder='Enter a value...',
            style={'width': '150px'}
        ),
    ]),
    html.Br(),
    html.Div(id='my-output'),

])


if __name__ == '__main__':
    app.run_server(debug=True)
