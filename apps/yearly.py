import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import plotly.express as px
import pandas as pd
import pathlib

from app import app

months = ['January','February','March','April','May','June'
        ,'July','August','September','October','November','December']

## do this before loading in data ##
# read in csv from datasets folder.
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

#specific data
df = pd.read_csv(DATA_PATH.joinpath("db_csv.csv"))
df = df[df['year']!=2017]

month_year_group = df.groupby(['year','month_name'])['sales_amount'].sum()
month_year_group = month_year_group.reindex(months, level='month_name').reset_index()

layout = dbc.Container([
    # header
    dbc.Row([
            dbc.Col(html.H1("web application, sales by year",
            style={'text-align':'center'},
            className='mb-5'),width=12)
    ]),

    # year revenue over time
    dbc.Row([

            dbc.Col([

            dcc.Checklist(id='year2', value=[2018,2019,2020],
                          options=[{'label':x, 'value':x}
                                   for x in sorted(month_year_group['year'].unique())],
                          labelClassName="mr-3"),

            dcc.Graph(id='month_year', figure={})],
            xs=12, sm=12, md=12, lg=6, xl=6
                ),

            # dbc.Col([
            # dcc.Graph(id='customer_type', figure={})],
            # xs=12, sm=12, md=12, lg=6, xl=6
            #     )
    ]),
])
@app.callback(
    Output('month_year', 'figure'),
    Input('year2', 'value')
)

def update_graph(values):
    temp = month_year_group[month_year_group['year'].isin(values)]
    fig2 = px.line(temp, x="month_name", y='sales_amount', color='year')
    fig2.update_xaxes(type='category', tick0='January')
    fig2.update_layout(hovermode="x")
    return fig2