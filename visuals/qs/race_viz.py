import constants as C
import dataframe_init as D
import matplotlib.pyplot as plt
import mpld3
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import textwrap
from django_plotly_dash import DjangoDash

import pandas as pd
from datetime import datetime

app = DjangoDash('race_viz', external_stylesheets=[dbc.themes.BOOTSTRAP])

race_dict = {'Asian':73, 'Black or African American':4, 'Hispanic or Latinx':4, 'White':35}
race_label = list(race_dict.keys())
race_num = list(race_dict.values())

fig = px.bar(x = race_label, y = race_num)

fig.update_traces(marker_color = 'rgb(71,159,118)')
for axis in fig.layout:
    if type(fig.layout[axis])==go.layout.YAxis:
        fig.layout[axis].title.text=''
    if type(fig.layout[axis])==go.layout.XAxis:
        fig.layout[axis].title.text=''
    
fig.update_layout(
        xaxis=dict(
            fixedrange=True,
        ),
        yaxis=dict(
            fixedrange = True, 
        ),
    )

fig.update_layout(
    margin=dict(l=0, r=0, t=35, b=0),
)

app.layout = html.Div([
    html.Div([
        dcc.Graph(figure=fig)
    ]),

])

if __name__ == '__main__':
    app.run_server(debug=True)