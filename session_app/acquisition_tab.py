import datajoint as dj
import dash
import dash_table
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import copy

from dj_tables import lab, subject, acquisition
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

## ------------------------- acquisition table --------------------------------
# acquisition table style
acquisition_table_style = copy.deepcopy(table_style_template)
acquisition_table_style.update(
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

acquisition_table_style['style_table'].update({
    'minHeight': '300px',
    'height': '300px',
    'maxHeight': '300px',
})

# from datajoint tables, get the data and table definition
contents = acquisition.Session.fetch(as_dict=True)
columns = [{"name": i, "id": i} for i in acquisition.Session.heading.names]

acquisition_table = dash_table.DataTable(
    id='acquisition-table',
    columns=columns,
    data=contents,
    # below are all styles
    **acquisition_table_style
)

## ------------------------- add acquisition table ------------------------------
# some fields are presented as dropdown list

# for c in columns:
#     if c['name'] in ['sex', 'strain']:
#         c.update(presentation="dropdown")

# add subject table style
add_acquisition_style = copy.deepcopy(table_style_template)
add_acquisition_style['style_table'].update({
    'minHeight': '80px',
    'height': '80px',
    'maxHeight': '80px',
})

add_acquisition_table = dash_table.DataTable(
    id='add-acquisition-table',
    columns=columns,
    data=[{c['id']: utils.get_default(acquisition.Session, c['id']) for c in columns}],
    **add_acquisition_style,
    editable=True
    )

## ----------------------------- add acquisition button ---------------------------------
add_acquisition_button = html.Button(
    children='Add an acquisition record',
    id='add-acquisition-button', n_clicks=0,
    style={'marginBottom': '0.5em'})

## ------------------------- deletion confirm dialogue ------------------------------
delete_acquisition_confirm = dcc.ConfirmDialog(
    id='delete-acquisition-confirm',
    message='Are you sure you want to delete the record?',
),
## ------------------------- deletion acquisition button --------------------------------
delete_acquisition_button = html.Button(
    children='Delete the current record',
    id='delete-acquisition-button', n_clicks=0,
    style={'marginRight': '1em'})

## ------------------------- update acquisition button --------------------------------
update_acquisition_button = html.Button(
    children='Update the current record',
    id='update-acquisition-button', n_clicks=0,
    # style={'display': 'inline-block'}
    )
## ------------------------- acquisition tab -------------------------------------
acquisition_tab_contents = html.Div(
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
                                            html.H6("General Parameters"),
                                            dcc.Dropdown(
                                            id='general-acquisition-dropdown',
                                            options=[
                                                # label is what is shown up on the dropdown list
                                                {'label': 'Session', 'value': 'Session'},
                                                {'label': 'User', 'value': 'User'},
                                                {'label': 'Reward', 'value': 'Reward'}
                                            ],
                                            value='Session',
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
                                            html.H6("Task Parameters"),
                                            dcc.Dropdown(
                                            id='task-acquisition-dropdown',
                                            options=[
                                                # label is what is shown up on the dropdown list
                                                {'label': 'Scara', 'value': 'Scara'},
                                                {'label': 'Lever Press', 'value': 'LeverPress'}
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
                                            html.H6("Instrument(s) Used & Calibration"),
                                            dcc.Dropdown(
                                            id='instruments-acquisition-dropdown',
                                            options=[
                                                # label is what is shown up on the dropdown list
                                                {'label': 'Camera', 'value': 'Camera'},
                                                {'label': 'Two Photon', 'value': 'TwoPhoton'},
                                                {'label': 'Inscopix', 'value': 'Inscopix'},
                                                {'label': 'Nvoke', 'value': 'Nvoke'},
                                                {'label': 'Optogenetics', 'value': 'Optogenetics'},
                                                {'label': 'Ephysiology', 'value': 'Ephys'},
                                                {'label': 'Calibration Notes', 'value': 'Calibration'}
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
                            add_acquisition_button,
                            add_acquisition_table
                        ],
                        style={'marginBottom': '20px'}
                    ),

                    html.Div(
                        children =
                        [
                            delete_acquisition_button,
                            update_acquisition_button
                        ],
                        style={'marginBottom': '0.5em'}
                    ),
                    acquisition_table
                ],
                style={'width': '50%', 'marginTop': '-22px'}
            )

## -----------------------------------------------------------------------------
          ]
        )
    ]
)
