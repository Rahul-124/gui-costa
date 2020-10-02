import datajoint as dj
import dash
import dash_table
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import copy

from dj_tables import lab, subject, action, acquisition
import utils

import performance_tab

## ========================= Create a flask app ===========================
# dash does the job for you
app = dash.Dash(__name__)

## ========================= Construct webpage layout ========================
app.layout = html.Div([
    dcc.Tabs(id="tabs", value='Performance', children=[
        dcc.Tab(label='Performance', value='Performance'),
        dcc.Tab(label='Post-Imaging', value='Post-Imaging')
    ],
    style={'width': '50%', 'marginBottom': '2em'}),
    html.Div(id='tabs-content')
])

## ========================= Callback functions =========================
@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'Performance':
        return performance_tab.performance_tab_contents

    elif tab == 'Post-Imaging':
        return html.Div([
            html.H3('Post-Imaging content')
        ])

## ------------------------- performance tab callback --------------------------------
# @app.callback(
#     # first argument is the id of a component, second is the field of that component
#     [Output('cohort-performance-dropdown', 'options')], # function returns overwrite the 'column' here
#     [Input('select-performance-dropdown', 'value'),
#      Input('user-performance-dropdown', 'value')])
# def populate_cohort_dropdown(task_selection, user_selection):
#
# return options


## ========================= Run server =========================

if __name__ == '__main__':
    dj.config['safemode'] = False
    # run the server, debug = True allows auto-updating without restarting the server.
    app.run_server(debug=True)
