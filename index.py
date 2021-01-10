import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from apps import revenue
from apps import test ###############
from apps import yearly
# read in the app and server from the app file
from app import app
from app import server

# read in the pages from the apps folder


app.layout = html.Div([
    html.Div([
        dcc.Link('yearly|', href='/apps/yearly'),
        dcc.Link('revenue|', href='/apps/revenue'),
        dcc.Link('test|', href='/apps/test') #################
    ], className="row"),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', children=[])
])

@app.callback(Output(component_id='page-content', component_property='children'),
              [Input(component_id='url', component_property='pathname')])
def display_page(pathname):
    if pathname == '/apps/yearly':
        return yearly.layout
    if pathname == '/apps/revenue':
        return revenue.layout
    if pathname == '/apps/test': #############
        return test.layout        #############
    else:
        return revenue.layout

if __name__ == '__main__':
    app.run_server(debug=True)


# TODO:
# figure out why year is differnet than revenue
# get 2 plots on one row
# why did the import work after i tried it?
# make a home page dash board then other pages are more in depth