import datajoint as dj
import dash
import dash_table
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import copy

from dj_tables import lab, subject, action, acquisition
import utils

import action_tab, acquisition_tab

## ========================= Create a flask app ===========================
# dash does the job for you
app = dash.Dash(__name__)

## ========================= Construct webpage layout ========================
app.layout = html.Div([
    dcc.Tabs(id="tabs", value='Subject', children=[
        dcc.Tab(label='Subject', value='Subject'),
        dcc.Tab(label='Action', value='Action'),
        dcc.Tab(label='Acquisition', value='Acquisition'),
        dcc.Tab(label='Instrument', value='Instrument')
    ],
    style={'width': '50%', 'marginBottom': '2em'}),
    html.Div(id='tabs-content')
])

## ========================= Callback functions =========================
@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'Subject':
        return html.Div([
            html.H3('Subject content')
        ])
    elif tab == 'Action':
        return action_tab.action_tab_contents

    elif tab == 'Acquisition':
        return acquisition_tab.acquisition_tab_contents

    elif tab == 'Instrument':
        return html.Div([
            html.H3('Instrument content')
        ])

## ------------------------- action tab callback --------------------------------
@app.callback(
    # first argument is the id of a component, second is the field of that component
    [Output('action-table', 'data'), # function returns overwrite the 'data' here
     Output('action-table', 'columns'),
     Output('add-action-table', 'data'),
     Output('add-action-table', 'columns')], # function returns overwrite the 'column' here
    [Input('add-action-button', 'n_clicks'),
     Input('delete-action-button', 'n_clicks'),
     Input('monitoring-action-dropdown', 'value'),
     Input('restriction-action-dropdown', 'value'),
     Input('administration-action-dropdown', 'value')],
    [State('add-action-table', 'data'),
     State('action-table', 'data'),
     State('action-table', 'selected_rows')])
# arguments of the call back function need to be the same order
# as the Input and State
def add_action(n_clicks_add, n_clicks_delete, monitoring_dropdown_value, restriction_dropdown_value, administration_dropdown_value, new_data, data, selected_rows):
    ctx = dash.callback_context
    triggered_component = ctx.triggered[0]['prop_id'].split('.')[0]

    if monitoring_dropdown_value == 'Weighing':
        data = action.Weighing.fetch(as_dict=True)
        columns = [{"name": i, "id": i} for i in action.Weighing.heading.names]
        data_add_action_table =[{c['id']: utils.get_default(action.Weighing, c['id']) for c in columns}]

    elif monitoring_dropdown_value == 'HealthStatus':
        data = action.Weighing.HealthStatus.fetch(as_dict=True)
        columns = [{"name": i, "id": i} for i in action.Weighing.HealthStatus.heading.names]
        data_add_action_table =[{c['id']: utils.get_default(action.Weighing.HealthStatus, c['id']) for c in columns}]

    elif restriction_dropdown_value == 'WaterRestriction':
        data = action.WaterRestriction.fetch(as_dict=True)
        columns = [{"name": i, "id": i} for i in action.WaterRestriction.heading.names]
        data_add_action_table =[{c['id']: utils.get_default(action.WaterRestriction, c['id']) for c in columns}]

    elif restriction_dropdown_value == 'FoodRestriction':
        data = action.FoodRestriction.fetch(as_dict=True)
        columns = [{"name": i, "id": i} for i in action.FoodRestriction.heading.names]
        data_add_action_table =[{c['id']: utils.get_default(action.FoodRestriction, c['id']) for c in columns}]

    elif administration_dropdown_value == 'WaterAdministration':
        data = action.WaterAdministration.fetch(as_dict=True)
        columns = [{"name": i, "id": i} for i in action.WaterAdministration.heading.names]
        data_add_action_table =[{c['id']: utils.get_default(action.WaterAdministration, c['id']) for c in columns}]

    elif administration_dropdown_value =='FoodAdministration':
        data = action.FoodAdministration.fetch(as_dict=True)
        columns = [{"name": i, "id": i} for i in action.FoodAdministration.heading.names]
        data_add_action_table =[{c['id']: utils.get_default(action.FoodAdministration, c['id']) for c in columns}]

    if triggered_component == 'add-action-button':
        entry = {k: v for k, v in new_data[0].items() if v!=''}

        if monitoring_dropdown_value == 'Weighing':
            action.Weighing.insert1(entry)
            data = action.Weighing.fetch(as_dict=True)

        elif monitoring_dropdown_value == 'HealthStatus':
            for c in columns:
                if c['name'] in ['fur', 'mobility', 'stress', 'suture_implant']:
                    c=c.update(presentation="dropdown")
            action.Weighing.HealthStatus.insert1(entry)
            data = action.Weighing.HealthStatus.fetch(as_dict=True)

        elif restriction_dropdown_value == 'WaterRestriction':
            action.WaterRestriction.insert1(entry)
            data = action.WaterRestriction.fetch(as_dict=True)

        elif restriction_dropdown_value == 'FoodRestriction':
            action.FoodRestriction.insert1(entry)
            data = action.FoodRestriction.fetch(as_dict=True)

        elif administration_dropdown_value =='WaterAdministration':
            action.WaterAdministration.insert1(entry)
            data = action.WaterAdministration.fetch(as_dict=True)

        elif administration_dropdown_value =='FoodAdministration':
            action.FoodAdministration.insert1(entry)
            data = action.FoodAdministration.fetch(as_dict=True)


    if triggered_component == 'delete-action-button' and selected_rows:
        print(selected_rows)

        if monitoring_dropdown_value == 'Weighing':
            entry = {'subject_id': data[selected_rows[0]]['subject_id'],
                     'weighing_time': data[selected_rows[0]]['weighing_time']}
            (action.Weighing & entry).delete()
            data = action.Weighing.fetch(as_dict=True)

        elif monitoring_dropdown_value == 'HealthStatus':
            entry = {'subject_id': data[selected_rows[0]]['subject_id'],
                     'computer_name': data[selected_rows[0]]['computer_name']}
            (action.Weighing.HealthStatus & entry).delete()
            data = action.Weighing.HealthStatus.fetch(as_dict=True)

        elif restriction_dropdown_value == 'WaterRestriction':
            entry = {'subject_id': data[selected_rows[0]]['subject_id'],
                     'water_restr_start_time': data[selected_rows[0]]['water_restr_start_time']}
            (action.WaterRestriction & entry).delete()
            data = action.WaterRestriction.fetch(as_dict=True)

        elif restriction_dropdown_value == 'FoodRestriction':
            entry = {'subject_id': data[selected_rows[0]]['subject_id'],
                     'food_restr_start_time': data[selected_rows[0]]['food_restr_start_time']}
            (action.FoodRestriction & entry).delete()
            data = action.FoodRestriction.fetch(as_dict=True)

        elif administration_dropdown_value == 'WaterAdministration':
            entry = {'subject_id': data[selected_rows[0]]['subject_id'],
                     'water_admin_time': data[selected_rows[0]]['water_admin_time']}
            (action.WaterAdministration & entry).delete()
            data = action.WaterAdministration.fetch(as_dict=True)

        elif administration_dropdown_value =='FoodAdministration':
            entry = {'subject_id': data[selected_rows[0]]['subject_id'],
                     'food_admin_time': data[selected_rows[0]]['food_admin_time']}
            (action.FoodAdministration & entry).delete()
            data = action.FoodAdministration.fetch(as_dict=True)


    return data, columns,data_add_action_table, columns

@app.callback(
    [Output('delete-action-button', 'disabled'),
     Output('update-action-button', 'disabled')],
    [Input('action-table', 'selected_rows')])
def set_button_enabled_state(selected_rows):
    if selected_rows:
        disabled = False
    else:
        disabled = True
    return disabled, disabled
## ------------------------- acquisition tab callback --------------------------------
@app.callback(
    # first argument is the id of a component, second is the field of that component
    [Output('acquisition-table', 'data'), # function returns overwrite the 'data' here
     Output('acquisition-table', 'columns'),
     Output('add-acquisition-table', 'data'),
     Output('add-acquisition-table', 'columns')], # function returns overwrite the 'column' here
    [Input('add-acquisition-button', 'n_clicks'),
     Input('delete-acquisition-button', 'n_clicks'),
     Input('general-acquisition-dropdown', 'value'),
     Input('task-acquisition-dropdown', 'value'),
     Input('instruments-acquisition-dropdown', 'value')],
    [State('add-acquisition-table', 'data'),
     State('acquisition-table', 'data'),
     State('acquisition-table', 'selected_rows')])
# arguments of the call back function need to be the same order
# as the Input and State
def add_acquisition(n_clicks_add, n_clicks_delete, general_dropdown_value, task_dropdown_value, instruments_dropdown_value, new_data, data, selected_rows):
    ctx = dash.callback_context
    triggered_component = ctx.triggered[0]['prop_id'].split('.')[0]

    if general_dropdown_value == 'Session':
        data = acquisition.Session.fetch(as_dict=True)
        columns = [{"name": i, "id": i} for i in acquisition.Session.heading.names]
        data_add_acquisition_table =[{c['id']: utils.get_default(acquisition.Session, c['id']) for c in columns}]

    elif general_dropdown_value == 'User':
        data = acquisition.Session.User.fetch(as_dict=True)
        columns = [{"name": i, "id": i} for i in acquisition.Session.User.heading.names]
        data_add_acquisition_table =[{c['id']: utils.get_default(acquisition.Session.User, c['id']) for c in columns}]

    elif general_dropdown_value == 'Reward':
        data = acquisition.Session.Reward.fetch(as_dict=True)
        columns = [{"name": i, "id": i} for i in acquisition.Session.Reward.heading.names]
        data_add_acquisition_table =[{c['id']: utils.get_default(acquisition.Session.Reward, c['id']) for c in columns}]

    elif task_dropdown_value == 'Scara':
        data = acquisition.Session.Scara.fetch(as_dict=True)
        columns = [{"name": i, "id": i} for i in acquisition.Session.Scara.heading.names]
        data_add_acquisition_table =[{c['id']: utils.get_default(acquisition.Session.Scara, c['id']) for c in columns}]

    elif instruments_dropdown_value == 'Camera':
        data = acquisition.Session.Camera.fetch(as_dict=True)
        columns = [{"name": i, "id": i} for i in acquisition.Session.Camera.heading.names]
        data_add_acquisition_table =[{c['id']: utils.get_default(acquisition.Session.Camera, c['id']) for c in columns}]

    elif instruments_dropdown_value =='TwoPhoton':
        data = acquisition.Session.TwoPhoton.fetch(as_dict=True)
        columns = [{"name": i, "id": i} for i in acquisition.Session.TwoPhoton.heading.names]
        data_add_acquisition_table =[{c['id']: utils.get_default(acquisition.Session.TwoPhoton, c['id']) for c in columns}]

    elif instruments_dropdown_value == 'Inscopix':
        data = acquisition.Session.Inscopix.fetch(as_dict=True)
        columns = [{"name": i, "id": i} for i in acquisition.Session.Inscopix.heading.names]
        data_add_acquisition_table =[{c['id']: utils.get_default(acquisition.Session.Inscopix, c['id']) for c in columns}]

    elif instruments_dropdown_value == 'Nvoke':
        data = acquisition.Session.Nvoke.fetch(as_dict=True)
        columns = [{"name": i, "id": i} for i in acquisition.Session.Nvoke.heading.names]
        data_add_acquisition_table =[{c['id']: utils.get_default(acquisition.Session.Nvoke, c['id']) for c in columns}]

    elif instruments_dropdown_value == 'Optogenetics':
        data = acquisition.Session.Optogenetics.fetch(as_dict=True)
        columns = [{"name": i, "id": i} for i in acquisition.Session.Optogenetics.heading.names]
        data_add_acquisition_table =[{c['id']: utils.get_default(acquisition.Session.Optogenetics, c['id']) for c in columns}]

    elif instruments_dropdown_value == 'Ephys':
        data = acquisition.Session.Ephys.fetch(as_dict=True)
        columns = [{"name": i, "id": i} for i in acquisition.Session.Ephys.heading.names]
        data_add_acquisition_table =[{c['id']: utils.get_default(acquisition.Session.Ephys, c['id']) for c in columns}]

    elif instruments_dropdown_value == 'Calibration':
        data = acquisition.Session.Calibration.fetch(as_dict=True)
        columns = [{"name": i, "id": i} for i in acquisition.Session.Calibration.heading.names]
        data_add_acquisition_table =[{c['id']: utils.get_default(acquisition.Session.Calibration, c['id']) for c in columns}]


    if triggered_component == 'add-acquisition-button':
        entry = {k: v for k, v in new_data[0].items() if v!=''}

        if general_dropdown_value == 'Session':
            acquisition.Session.insert1(entry)
            data = acquisition.Session.fetch(as_dict=True)

        elif general_dropdown_value == 'User':
            acquisition.Session.User.insert1(entry)
            data = acquisition.Session.User.fetch(as_dict=True)

        elif general_dropdown_value == 'Reward':
            acquisition.Session.Reward.insert1(entry)
            data = acquisition.Session.Reward.fetch(as_dict=True)

        elif task_dropdown_value == 'Scara':
            acquisition.Session.Scara.insert1(entry)
            data = acquisition.Session.Scara.fetch(as_dict=True)

        elif instruments_dropdown_value =='Camera':
            acquisition.Session.Camera.insert1(entry)
            data = acquisition.Session.Camera.fetch(as_dict=True)

        elif instruments_dropdown_value =='TwoPhoton':
            acquisition.Session.TwoPhoton.insert1(entry)
            data = acquisition.Session.TwoPhoton.fetch(as_dict=True)

        elif instruments_dropdown_value =='Inscopix':
            acquisition.Session.Inscopix.insert1(entry)
            data = acquisition.Session.Inscopix.fetch(as_dict=True)

        elif instruments_dropdown_value =='Nvoke':
            acquisition.Session.Nvoke.insert1(entry)
            data = acquisition.Session.Nvoke.fetch(as_dict=True)

        elif instruments_dropdown_value =='Optogenetics':
            acquisition.Session.Optogenetics.insert1(entry)
            data = acquisition.Session.Optogenetics.fetch(as_dict=True)

        elif instruments_dropdown_value =='Ephys':
            acquisition.Session.Ephys.insert1(entry)
            data = acquisition.Session.Ephys.fetch(as_dict=True)

        elif instruments_dropdown_value =='Calibration':
            acquisition.Session.Calibration.insert1(entry)
            data = acquisition.Session.Calibration.fetch(as_dict=True)


    if triggered_component == 'delete-acquisition-button' and selected_rows:
        print(selected_rows)

        if general_dropdown_value == 'Session':
            entry = {'subject_id': data[selected_rows[0]]['subject_id'],
                     'session_start_time': data[selected_rows[0]]['session_start_time']}
            (acquisition.Session & entry).delete()
            data = acquisition.Session.fetch(as_dict=True)

        elif general_dropdown_value == 'User':
            entry = {'subject_id': data[selected_rows[0]]['subject_id'],
                     'session_start_time': data[selected_rows[0]]['session_start_time'],
                     'user': data[selected_rows[0]]['user']}
            (acquisition.Session.User & entry).delete()
            data = acquisition.Session.User.fetch(as_dict=True)

        elif general_dropdown_value == 'Reward':
            entry = {'subject_id': data[selected_rows[0]]['subject_id'],
                     'session_start_time': data[selected_rows[0]]['session_start_time'],
                     'reward_name': data[selected_rows[0]]['reward_name']}
            (acquisition.Session.Reward & entry).delete()
            data = acquisition.Session.Reward.fetch(as_dict=True)

        elif task_dropdown_value == 'Scara':
            entry = {'subject_id': data[selected_rows[0]]['subject_id'],
                     'session_start_time': data[selected_rows[0]]['session_start_time']}
            (acquisition.Scara & entry).delete()
            data = acquisition.Scara.fetch(as_dict=True)

        elif instruments_dropdown_value == 'Camera':
            entry = {'subject_id': data[selected_rows[0]]['subject_id'],
                     'session_start_time': data[selected_rows[0]]['session_start_time'],
                     'camera_index': data[selected_rows[0]]['camera_index']}
            (acquisition.Session.Camera & entry).delete()
            data = acquisition.Session.Camera.fetch(as_dict=True)

        elif instruments_dropdown_value =='TwoPhoton':
            entry = {'subject_id': data[selected_rows[0]]['subject_id'],
                     'session_start_time': data[selected_rows[0]]['session_start_time'],
                     'two_photon_name': data[selected_rows[0]]['two_photon_name']}
            (acquisition.Session.TwoPhoton & entry).delete()
            data = acquisition.Session.TwoPhoton.fetch(as_dict=True)

        elif instruments_dropdown_value =='Inscopix':
            entry = {'subject_id': data[selected_rows[0]]['subject_id'],
                     'session_start_time': data[selected_rows[0]]['session_start_time']}
            (acquisition.Session.Inscopix & entry).delete()
            data = acquisition.Session.Inscopix.fetch(as_dict=True)

        elif instruments_dropdown_value =='Nvoke':
            entry = {'subject_id': data[selected_rows[0]]['subject_id'],
                     'session_start_time': data[selected_rows[0]]['session_start_time']}
            (acquisition.Session.Nvoke & entry).delete()
            data = acquisition.Session.Nvoke.fetch(as_dict=True)

        elif instruments_dropdown_value =='Optogenetics':
            entry = {'subject_id': data[selected_rows[0]]['subject_id'],
                     'session_start_time': data[selected_rows[0]]['session_start_time']}
            (acquisition.Session.Optogenetics & entry).delete()
            data = acquisition.Session.Optogenetics.fetch(as_dict=True)

        elif instruments_dropdown_value =='Ephys':
            entry = {'subject_id': data[selected_rows[0]]['subject_id'],
                     'session_start_time': data[selected_rows[0]]['session_start_time']}
            (acquisition.Session.Ephys & entry).delete()
            data = acquisition.Session.Ephys.fetch(as_dict=True)

        elif instruments_dropdown_value =='Calibration':
            entry = {'subject_id': data[selected_rows[0]]['subject_id'],
                     'session_start_time': data[selected_rows[0]]['session_start_time']}
            (acquisition.Session.Calibration & entry).delete()
            data = acquisition.Session.Calibration.fetch(as_dict=True)


    return data, columns,data_add_acquisition_table, columns

@app.callback(
    [Output('delete-acquisition-button', 'disabled'),
     Output('update-acquisition-button', 'disabled')],
    [Input('acquisition-table', 'selected_rows')])
def set_button_enabled_state(selected_rows):
    if selected_rows:
        disabled = False
    else:
        disabled = True
    return disabled, disabled
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
