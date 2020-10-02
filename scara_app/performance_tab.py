import datajoint as dj
import dash
import dash_table
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import copy

from dj_tables import lab, subject, acquisition, scara
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

## ------------------------- performance table --------------------------------
# performance table style
performance_table_style = copy.deepcopy(table_style_template)
performance_table_style.update(
    style_data_conditional=[
        {'if': {'row_index': 'odd'},
        'backgroundColor': 'rgb(245, 245, 245)'}
    ],
    # allow sorting
    sort_action='native',
    # allow filtering
    filter_action='native')

performance_table_style['style_table'].update({
    'minHeight': '300px',
    'height': '300px',
    'maxHeight': '300px',
})

# from datajoint tables, get the data and table definition
contents = scara.ScaraPerformance.fetch(as_dict=True)
columns = [{"name": i, "id": i} for i in scara.ScaraPerformance.heading.names]

performance_table = dash_table.DataTable(
    id='performance-table',
    columns=columns,
    data=contents,
    # below are all styles
    **performance_table_style
)

## ----------------------------- auto-populate button ---------------------------------
populate_performance_button = html.Button(
    children='Click to Auto-Populate',
    id='add-performance-button', n_clicks=0,
    style={'marginBottom': '0.5em'})

## ----------------------------- user dropdown options ---------------------------------
users = list(dict.fromkeys(subject.Subject.User.fetch('user')))
user_dropdown_options = [{"label": i, "value": i} for i in users]

## ----------------------------- cohort dropdown options ---------------------------------

## ------------------------- performance tab -------------------------------------
performance_tab_contents = html.Div(
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
                                    ## ----------------------------- Selection ---------------------------------
                                    html.Div(
                                        className="padding-bot",
                                        children= [
                                            html.H6("Select Task Type"),
                                            dcc.Dropdown(
                                            id='select-performance-dropdown',
                                            options=[
                                                # label is what is shown up on the dropdown list
                                                {'label': 'Scara Joystick', 'value': 'scara'},
                                                {'label': 'Lever Press', 'value': 'leverpress'},
                                                {'label': 'Three-Poke', 'value': 'three_poke'}
                                            ],
                                            value='Session',
                                            style={'width': '200px'},
                                            # clearable=False,
                                            # searchable=False,
                                            multi=False,
                                            placeholder='Select table ...')
                                        ]
                                    ),
                                    ## ----------------------------- User ---------------------------------
                                    html.Div(
                                        className="padding-top-bot",
                                        children=[
                                            html.H6("Select User"),
                                            dcc.Dropdown(
                                            id='user-performance-dropdown',
                                            options = user_dropdown_options, #Get options & remove duplicates
                                            # value='U',
                                            style={'width': '200px'},
                                            # clearable=False,
                                            # searchable=False,
                                            multi=False,
                                            placeholder='Select user ...')
                                        ]
                                    ),


                                    ## ----------------------------- Cohort ---------------------------------
                                    html.Div(
                                        className="padding-top-bot-divider",
                                        children=[
                                            html.H6(" ", style = {'border-top':'1px solid blue'}),
                                            html.H6("Select Cohort", style = {'margin-top':'15px'}),
                                            dcc.Dropdown(
                                            id='cohort-performance-dropdown',
                                            options=[], #none initially
                                            # value='U',
                                            style={'width': '200px'},
                                            # clearable=False,
                                            # searchable=False,
                                            multi=False,
                                            placeholder='Select cohort ...')
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
                            populate_performance_button
                        ],
                        style={'marginBottom': '20px'}
                    ),
                    performance_table
                ],
                style={'width': '50%', 'marginTop': '-22px'}
            )

## -----------------------------------------------------------------------------
          ]
        )
    ]
)
