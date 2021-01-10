import sys
sys.path.append("..")

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pathlib
from multi_page_sales.app import app

# read in csv from datasets folder.
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()
df = pd.read_csv(DATA_PATH.joinpath("db_csv.csv"))

# if __name__ == '__main__':
#     a = app
#     print(a)