import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# read in the app and server from the app file
from app import app
from app import server

# read in the pages from the apps folder
from apps import yearly

app.layout = dbc.Container([
    dcc.Location(id='url', refresh=False), # by defalt pathname is empty

    # row that will be the links to other pages at the top of the page.
    dbc.Row([
        dcc.Link('yearly|', href='/apps/yearly'),
        dcc.Link('products|', href='/apps/products')
            ],className='row'),
    html.Div(id='page-content', children=[])
])


@app.callback(
    Output('page-condent', 'children'),
    [Input('url', 'pathname')])

def display_page(pathname):
    if pathname == 'app/yearly':
        return yearly.layout


if __name__ == '__main__':

    app.run_server(debug=True)