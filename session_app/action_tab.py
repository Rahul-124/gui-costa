import datajoint as dj
import dash
import dash_table
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import copy

from dj_tables import lab, subject, action
import utils

## ========================= Construct components =========================
# table style settings
table_style_template = dict(
    fixed_columns={'headers': True, 'data': 1},
    style_cell={
        'textAlign': 'left',
        'fontSize':12,
        'font-family':'helvetica',
        'minWidth': '150px', 'width': '150px', 'maxWidth': '150px',
        'overflow': 'hidden',
        'height': '30px'},
    page_action='none',
    style_table={
        'minWidth': '950px',
        'width': '950px',
        'maxWidth': '950px',
        'overflowY': 'scroll',
        'overflowX': 'scroll'},
    style_header={
        'backgroundColor': 'rgb(220, 220, 220)',
        'fontWeight': 'bold'})

## ------------------------- action table --------------------------------
# action table style
action_table_style = copy.deepcopy(table_style_template)
action_table_style.update(
    style_data_conditional=[
        {'if': {'row_index': 'odd'},
        'backgroundColor': 'rgb(245, 245, 245)'}
    ],
    # allow sorting
    sort_action='native',
    # allow filtering
    filter_action='native',
    # allow selecting a single entry
    row_selectable='single')

action_table_style['style_table'].update({
    'minHeight': '300px',
    'height': '300px',
    'maxHeight': '300px',
})

# from datajoint tables, get the data and table definition
contents = action.Weighing.fetch(as_dict=True)
columns = [{"name": i, "id": i} for i in action.Weighing.heading.names]

action_table = dash_table.DataTable(
    id='action-table',
    columns=columns,
    data=contents,
    # below are all styles
    **action_table_style
)

## ------------------------- add action table ------------------------------
# some fields are presented as dropdown list

# for c in columns:
#     if c['name'] in ['sex', 'strain']:
#         c.update(presentation="dropdown")

# add subject table style
add_action_style = copy.deepcopy(table_style_template)
add_action_style['style_table'].update({
    'minHeight': '80px',
    'height': '80px',
    'maxHeight': '80px',
})

add_action_table = dash_table.DataTable(
    id='add-action-table',
    columns=columns,
    data=[{c['id']: utils.get_default(action.Weighing, c['id']) for c in columns}],
    **add_action_style,
    editable=True
    )

## ----------------------------- add action button ---------------------------------
add_action_button = html.Button(
    children='Add an action record',
    id='add-action-button', n_clicks=0,
    style={'marginBottom': '0.5em'})

## ------------------------- deletion confirm dialogue ------------------------------
delete_action_confirm = dcc.ConfirmDialog(
    id='delete-action-confirm',
    message='Are you sure you want to delete the record?',
),
## ------------------------- deletion action button --------------------------------
delete_action_button = html.Button(
    children='Delete the current record',
    id='delete-action-button', n_clicks=0,
    style={'marginRight': '1em'})

## ------------------------- update action button --------------------------------
update_action_button = html.Button(
    children='Update the current record',
    id='update-action-button', n_clicks=0,
    # style={'display': 'inline-block'}
    )
## ------------------------- action tab -------------------------------------
action_tab_contents = html.Div(
    children=[
        html.Div(
            className="row app-body",
            children=[

            html.Div(
                #Table Selection
                className="three columns card",
                children=[
                ## ----------------------------- Table Options ---------------------------------
                    html.Div(
                        className="bg-white",
                        children=[
                            html.Div(
                                children=[
                                    ## ----------------------------- Monitoring ---------------------------------
                                    html.Div(
                                        className="padding-bot",
                                        children= [
                                            html.H6("Monitoring"),
                                            dcc.Dropdown(
                                            id='monitoring-action-dropdown',
                                            options=[
                                                # label is what is shown up on the dropdown list
                                                {'label': 'Weight', 'value': 'Weighing'},
                                                {'label': 'Health Status', 'value': 'HealthStatus'}
                                            ],
                                            value='Weighing',
                                            style={'width': '200px'},
                                            # clearable=False,
                                            # searchable=False,
                                            multi=False,
                                            placeholder='Select table ...')
                                        ]
                                    ),
                                    ## ----------------------------- Restriction ---------------------------------
                                    html.Div(
                                        className="padding-top-bot",
                                        children=[
                                            html.H6("Restriction"),
                                            dcc.Dropdown(
                                            id='restriction-action-dropdown',
                                            options=[
                                                # label is what is shown up on the dropdown list
                                                {'label': 'Water', 'value': 'WaterRestriction'},
                                                {'label': 'Food', 'value': 'FoodRestriction'},
                                            ],
                                            # value='U',
                                            style={'width': '200px'},
                                            # clearable=False,
                                            # searchable=False,
                                            multi=False,
                                            placeholder='Select table ...')
                                        ]
                                    ),


                                    ## ----------------------------- Administration ---------------------------------
                                    html.Div(
                                        className="padding-top-bot",
                                        children=[
                                            html.H6("Administration"),
                                            dcc.Dropdown(
                                            id='administration-action-dropdown',
                                            options=[
                                                # label is what is shown up on the dropdown list
                                                {'label': 'Water', 'value': 'WaterAdministration'},
                                                {'label': 'Food', 'value': 'FoodAdministration'},
                                            ],
                                            # value='U',
                                            style={'width': '200px'},
                                            # clearable=False,
                                            # searchable=False,
                                            multi=False,
                                            placeholder='Select table ...')
                                        ]
                                    )
                                ],
                            ),
                        ],
                    )
                ],
                style={'margin-left': '-40px'},
            ),
            ## ----------------------------- Tables ---------------------------------
            html.Div(
                className="eight columns card-left",
                children=[
                    html.Div(
                        children =
                        [
                            add_action_button,
                            add_action_table
                        ],
                        style={'marginBottom': '20px'}
                    ),

                    html.Div(
                        children =
                        [
                            delete_action_button,
                            update_action_button
                        ],
                        style={'marginBottom': '0.5em'}
                    ),
                    action_table
                ],
                style={'width': '50%', 'marginTop': '-22px'}
            )

## -----------------------------------------------------------------------------
          ]
        )
    ]
)
