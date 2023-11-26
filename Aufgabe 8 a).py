#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import math
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import numpy as np
import pandas as pd
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# generate random normal distributed data for x and y
# and store it in a pandas DataFrame

df = pd.DataFrame({'y': np.random.normal(loc=0, scale=10, size=1000),
                   'x': np.random.normal(loc=10, scale=2, size=1000)})

min_range = math.floor(df['y'].min())
max_range = math.ceil(df['y'].max())
mark1 = 10

marks = {i: str(i) for i in range(min_range, max_range + 1, mark1)}

app.layout = html.Div([html.H1("Dashboard 2"),
    dbc.Row([dbc.Col([dcc.Dropdown(options=['red', 'green', 'blue'], value='red', id='color', multi=False)], width=6),
             dbc.Col(
                 [dcc.RangeSlider
                      (min=min_range, 
                       max=max_range, 
                       id="range_slider",
                       marks=marks,
                        value=[df['y'].min(), df['y'].max()]
                      )
                ], width=6)
    ]),
    dbc.Row([dbc.Col([dcc.Graph(id="graph_1")], width=6),
             dbc.Col([dcc.Graph(id="graph_2")], width=6)
    ])], className="m-4")

@app.callback(Output("graph_1", "figure"), Input("color", "value"))

def update_graph_1(dropdown_value_color):
    fig = px.histogram(df, x="y", color_discrete_sequence=[dropdown_value_color])
    fig.update_layout()
    return fig

@app.callback(Output("graph_2", "figure"), Input("range_slider", "value"))

def update_graph_2(range_slider):
    dff = df[(df['y'] >= range_slider[0]) & (df['y'] <= range_slider[1])
            ] 
    fig = px.scatter(dff, x='x', y='y')
    fig.update_layout()
    return fig

if __name__ == '__main__':
    app.run_server(debug=False, port=8000)


# In[ ]:




