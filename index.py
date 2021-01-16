# analysis tools
import pandas as pd
import numpy as np

# plotting
import plotly.express as px
import plotly.graph_objects as go

# dash components
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# pages from apps folder
from apps import revenue
from apps import test ###############
from apps import yearly
from apps import market_product

# read in the app and server from the app file
from app import app
from app import server

# create a header with drop down of the pages
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/apps/test")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("yearly", href="/apps/yearly"),
                dbc.DropdownMenuItem("revenue", href="/apps/revenue"),
                dbc.DropdownMenuItem("test", href="/apps/test"),
                dbc.DropdownMenuItem("market products", href="/apps/market_product")
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="Sales Data Analysis",
    brand_href="#",
    color="primary",
    dark=True,
)

# creating the content from the page selected
content = html.Div(id="page-content", className="content")

# gaining access to the layout of each page via selection
app.layout = html.Div([dcc.Location(id="url"), navbar, content])

# call back for specific page selected
@app.callback(Output(component_id='page-content', component_property='children'),
              [Input(component_id='url', component_property='pathname')])
def display_page(pathname):
    if pathname == '/apps/yearly':
        return yearly.layout
    if pathname == '/apps/revenue':
        return revenue.layout
    if pathname == '/apps/market_product':
        return market_product.layout
    if pathname == '/apps/test': #############
        return test.layout        #############
    else:
        return test.layout

# run application: host file
if __name__ == '__main__':
    app.run_server(debug=True)


# TODO:
# figure out why year is differnet than revenue
# get 2 plots on one row
# why did the import work after i tried it?
# make a home page dash board then other pages are more in depth
# More analysis