from dash import Dash, dash_table, html, dcc
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

fall = FallTableau(fall_tableau_df=fall_tableau_df)
fall_semesters, fall_enrollments = fall.fall_semesters_and_enrollment_lists()
fall2 = FallDivisionEnrollments(fall_enrollment=Fall_Enrollment_df, fall_semesters=fall_semesters, fall_max_enrollments=fall_enrollments)
fall_max_enrollments, fall_semesters, fall_size = fall2.calculate_fall_enrollment()
fall2.calculate_sessions()
a = SpringTableau(tableau_df=tableau_df)
semester, enrollments = a.semester_and_enrollment_lists()

b = SpringDivisionEnrollments(spring_enrollment=Spring_Enrollment_df, spring_semesters=semester, spring_max_enrollments=enrollments)
enrollments, semesters, size = b.calculate_spring_enrollment()
c = BuildDashboard(enrollments=enrollments, semesters=semesters, size=size, fall_max_enrollments=fall_max_enrollments,
                 fall_semesters=fall_semesters, fall_size=fall_size)
fall_bar_fig = c.construct_fall_graphs()
bar_fig = c.construct_spring_graphs()



# print(subset_tableau_df)

subset_df = Spring_Enrollment_df[['Dept', 'Course', 'Class', 'Size', 'Max', 'FTES']]
# subset_modality_df = df[['Room', 'Course', 'Class', 'Size', 'Max', 'FTES']]

# df2 = subset_df.groupby('Course').agg({'Class': 'count','Size': 'sum','Max': 'sum'}).mean().reset_index()
df3 = subset_df.groupby('Dept').agg({'Class': 'count'}).reset_index()
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
app = Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)
app.layout = html.Div(
    [
        dbc.Row(dbc.Col(html.Div('A Single Column'))),
        dbc.Row([
            dbc.Col(html.Div(dcc.Graph(id='graph1', figure=fall_bar_fig)), width=6),
            dbc.Col(html.Div(dcc.Graph(id='graph2', figure=bar_fig)), width=6),
            # dbc.Col(html.Div(dash_table.DataTable(df4.to_dict('records'), [{'name': i, 'id': i} for i in df4.columns]),), width=3),
            # dbc.Col(html.Div(dash_table.DataTable(df5.to_dict('records'), [{'name': i, 'id': i} for i in df5.columns])), width=3),
            dbc.Col(html.Div('One of three columns'))
        ]),
        dbc.Row([
            dbc.Col(html.Div(dash_table.DataTable(df3.to_dict('records'), [{'name': i, 'id': i} for i in df3.columns]),
                             )),
            dbc.Col(html.Div('One of three columns'))
        ])
    ]
)

app.run(debug=True)