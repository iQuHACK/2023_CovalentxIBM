from dash import Dash, dcc, html, Input, Output, State
from func import transform, predict
from process_input import read_input
import base64
import uuid
import os
import flask

app = Dash(__name__, external_scripts=['https://cdn.tailwindcss.com'])

app.scripts.config.serve_locally = False
test_png = 'figs/schrodingersduck.png'
test_base64 = base64.b64encode(open(test_png, 'rb').read()).decode('ascii')
app.head = [html.Link(rel='stylesheet', href='./assets/base.css'),  ('''
    <style type="text/css">
    @tailwind base;
    </style>
    ''')]

app.layout = html.Div([
    html.Img(src='data:image/png;base64,{}'.format(test_base64),
             style={'height': '25%', 'width': '25%'}),
    html.Br(),
    html.H1("Spam detection with QSVC", className="m-5"),
    html.H6("Team Ytterbium @ iQuHack 2023", className="m-5 text-md"),
    html.Br(),
    # html.Div(id='container-button-basic',
    #          children='Enter a value and press submit')
    html.Div(dcc.Textarea(id='input-on-submit', placeholder="Email body",
             className="block w-96 m-5 h-40 p-4 text-gray-900 border border-gray-300 rounded-lg bg-gray-50 sm:text-md focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500")),
    html.Button('Submit', id='submit-val',
                className="rounded-full font-bold m-5 bg-cyan-200 text-black px-5 py-3", n_clicks=0),
    html.Br(),
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
    app.run_server(debug=False)
