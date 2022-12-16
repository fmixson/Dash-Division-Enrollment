from dash import Dash, dash_table, html, dcc, Input, Output
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import numpy

Spring_Enrollment_df = pd.read_csv('C:/Users/fmixson/PycharmProjects/DivisionEnrollment/Spring_Division_Enrollment.csv', encoding='Latin')
subset_df = Spring_Enrollment_df[['Dept', 'Course', 'Class', 'Size', 'Max', 'FTES']]

app = Dash()
app.layout = html.Div([
    dcc.Dropdown(
        id='dept_dropdown',
        options=[{'label': i, 'value': i} for i in subset_df['Dept'].unique()]
    ),
    html.Div(id='datatable_interactivity')
])


@app.callback(
    Output(component_id='datatable_interactivity', component_property='children'),
    Input(component_id='dept_dropdown', component_property='value')
        )
def update_datatable(value):
    print('value', value)
    if value == None:
        return dash_table.DataTable(subset_df.to_dict('records'), [{'name': i, 'id': i} for i in subset_df.columns],
                                    filter_action='native'),

app.run(debug=True)