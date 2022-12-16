from dash import Dash, dash_table, html, dcc, Input, Output
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import numpy
from Dashboard_Design import BuildDashboard
from Fall_Data import FallTableau, FallDivisionEnrollments
from Spring_Data import SpringTableau, SpringDivisionEnrollments


Fall_Enrollment_df = pd.read_csv('C:/Users/fmixson/PycharmProjects/DivisionEnrollment/Fall_Division_Enrollment.csv', encoding='Latin')
Spring_Enrollment_df = pd.read_csv('C:/Users/fmixson/PycharmProjects/DivisionEnrollment/Spring_Division_Enrollment.csv', encoding='Latin')
tableau_df = pd.read_csv('C:/Users/fmixson/Desktop/Dashboard_files/Enrollment Counts - table.csv', encoding='Latin')
fall_tableau_df = pd.read_csv('C:/Users/fmixson/Desktop/Dashboard_files/Fall_Enrollment Counts - table.csv', encoding='Latin')
pd.set_option('display.max_columns', None)
dropdown_list = Spring_Enrollment_df['Dept'].unique()

fall = FallTableau(fall_tableau_df=fall_tableau_df)
fall_semesters, fall_enrollments = fall.fall_semesters_and_enrollment_lists()
fall2 = FallDivisionEnrollments(fall_enrollment=Fall_Enrollment_df, fall_semesters=fall_semesters, fall_max_enrollments=fall_enrollments)
fall2.fall_table_cleanup()
fall_max_enrollments, fall_semesters, fall_size = fall2.calculate_fall_enrollment()
fall2.calculate_sessions()
a = SpringTableau(tableau_df=tableau_df)
semester, enrollments = a.semester_and_enrollment_lists()

b = SpringDivisionEnrollments(spring_enrollment=Spring_Enrollment_df, spring_semesters=semester, spring_max_enrollments=enrollments)
enrollments, semesters, size = b.calculate_spring_enrollment()
sessions_df = b.calculate_sessions()
modalities_df = b.modality_calculation()

c = BuildDashboard(enrollments=enrollments, semesters=semesters, size=size, fall_max_enrollments=fall_max_enrollments,
                 fall_semesters=fall_semesters, fall_size=fall_size)
fall_bar_fig = c.construct_fall_graphs()
bar_fig = c.construct_spring_graphs()

subset_df = Spring_Enrollment_df[['Dept', 'Course', 'Class', 'Size', 'Max', 'FTES']]

df3 = subset_df.groupby('Dept').agg({'Class': 'count'}).reset_index()

app = Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)
app.layout = html.Div(
        children=[
dbc.Row([
            # dbc.Col(html.Div(dcc.Graph(id='graph1', figure=fall_bar_fig)), width=3),
            dbc.Col(html.Div(dcc.Graph(id='graph2', figure=bar_fig)), width=4),
            dbc.Col(html.Div(dash_table.DataTable(sessions_df.to_dict('records'), [{'name': i, 'id': i} for i in sessions_df.columns]),), width=4),
            dbc.Col(html.Div(dash_table.DataTable(modalities_df.to_dict('records'), [{'name': i, 'id': i} for i in modalities_df.columns])), width=4),
            # dbc.Col(html.Div('One of three columns'))
        ]),
            dcc.Dropdown(
                id='dept_dropdown',
                options=[{'label': i , 'value': i} for i in dropdown_list],
                placeholder='--Select a Department--',
                multi=False,
                value='ASL'
            ),
            html.Div(id='datatable_container'),
            ])

        # dbc.Row([
        #     # dbc.Col(html.Div(dcc.Graph(id='graph1', figure=fall_bar_fig)), width=3),
        #     dbc.Col(html.Div(dcc.Graph(id='graph2', figure=bar_fig)), width=4),
        #     dbc.Col(html.Div(dash_table.DataTable(sessions_df.to_dict('records'), [{'name': i, 'id': i} for i in sessions_df.columns]),), width=4),
        #     dbc.Col(html.Div(dash_table.DataTable(modalities_df.to_dict('records'), [{'name': i, 'id': i} for i in modalities_df.columns])), width=4),
        #     # dbc.Col(html.Div('One of three columns'))
        # ]),

        # html.Div(id='datatable_ouput')])
            # dbc.Col(html.Div(dash_table.DataTable(subset_df.to_dict('records'), [{'name': i, 'id': i} for i in subset_df.columns]),
            #                   )),
            # dbc.Col(html.Div(dash_table.DataTable(modalities_df.to_dict('records'), [{'name': i, 'id':i} for i in modalities_df]))))




@app.callback(
    Output(component_id='datatable_container', component_property='children'),
    Input(component_id='dept_dropdown', component_property='value')
        )
def update_datatable(value):
    print('value', value)
    if value == None:
        return dash_table.DataTable(subset_df.to_dict('records'), [{'name': i, 'id': i} for i in subset_df.columns]),

    else:
        filtered_dff = subset_df[subset_df['Dept'] == value]
        

    return dash_table.DataTable(filtered_dff.to_dict('records'), [{'name': i, 'id': i} for i in filtered_dff.columns])

app.run(debug=True)

# df4 = subset_df.groupby('Dept').agg({'Class': 'count','Size': 'sum','Max': 'sum'}).reset_index()
# df5 = subset_modality_df.groupby('Room').agg({'Class': 'count'}).reset_index()
# total_modality = df5['Class'].sum()
# df5['Perc'] = df5['Class'] / total_modality
# df4['Fill'] = df4['Size'] / df4['Max']
# df4_style = df4.style.format({'Fill': "{:.2%}"})
# print(df4_style)
# random_x = df5['Perc']
# names = df5['Room']
# div_enroll = dept_df.iloc[0,2:3]
# print('div enroll', div_enroll)
# fig = px.pie(data_frame=df5, values='Perc', names='Room')
# bar_fig = go.Figure(data=[
#                     go.Bar(name='Size', x=df4['Dept'], y=df4['Size']),
#                     go.Bar(name='Max', x=df4['Dept'], y=df4['Max'])])
#