from dash import Dash, dash_table, html, dcc
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import numpy

class DivisionEnrollmentsbySemester:

    def __init__(self, tableau_df):
        self.tableau_df = tableau_df

    def semester_and_enrollment_lists(self):

        self.tableau_df.fillna(0, inplace=True)
        self.tableau_df.replace(',', '', regex=True, inplace=True)

        self.tableau_df[['Spring 2017', 'Spring 2018', 'Spring 2019', 'Spring 2020', 'Spring 2021', 'Spring 2022']] = \
            self.tableau_df[
                ['Spring 2017', 'Spring 2018', 'Spring 2019', 'Spring 2020', 'Spring 2021', 'Spring 2022']].astype(
                str).astype(int)

        subset_tableau_df = self.tableau_df[
            ['Division', 'Department', 'Subject', 'Course', 'Spring 2017', 'Spring 2018', 'Spring 2019',
             'Spring 2020', 'Spring 2021', 'Spring 2022']]

        div_totals = subset_tableau_df.groupby('Division').agg(
            {'Spring 2017': 'sum', 'Spring 2018': 'sum', 'Spring 2019': 'sum',
             'Spring 2020': 'sum', 'Spring 2021': 'sum', 'Spring 2022': 'sum'}).reset_index()
        div_totals_series = div_totals.iloc[0]

        div_totals_list = div_totals_series.values.tolist()
        div_index_list = div_totals_series.index.values.tolist()

        semesters = div_index_list[1:]
        enrollments = div_totals_list[1:]

        return semesters, enrollments

class FallDivisionEnrollments:

    def __init__(self, fall_enrollment, fall_semesters, fall_max_enrollments):
        self.fall_enrollment = fall_enrollment
        self.fall_semesters = fall_semesters
        self.fall_max_enrollments = fall_max_enrollments

    def calculate_spring_enrollment(self):
        fall_size = [0, 0, 0, 0, 0, 0]
        fall_size_enrollment = self.fall_enrollment['Size'].sum()
        fall_max_enrollment = self.fall_enrollment['Max'].sum()
        self.fall_max_enrollments.append(fall_max_enrollment)
        fall_size.append(fall_size_enrollment)
        self.fall_semesters.append('Fall 2023')
        return self.fall_max_enrollments, self.fall_semesters, fall_size

class SpringDivisionEnrollments:

    def __init__(self, spring_enrollment, spring_semesters, spring_max_enrollments):
        self.spring_enrollment = spring_enrollment
        self.spring_semesters = spring_semesters
        self.spring_max_enrollments = spring_max_enrollments

    def calculate_spring_enrollment(self):
        spring_size = [0, 0, 0, 0, 0, 0]
        spring_size_enrollment = self.spring_enrollment['Size'].sum()
        spring_max_enrollment_df = self.spring_enrollment['Max'].sum()
        self.spring_max_enrollments.append(spring_max_enrollment_df)
        spring_size.append(spring_size_enrollment)
        self.spring_semesters.append('Spring 2023')
        return self.spring_max_enrollments, self.spring_semesters, spring_size

class BuildWebsite:

    def __init__(self, enrollments, semesters, size):
        self.enrollments = enrollments
        self.semesters = semesters
        self.size = size

    def construct_graphs(self):

        actual = [0, 0, 0, 0, ]
        bar_fig = go.Figure(data=[
                                go.Bar(name='actual', x=self.semesters, y=self.size),
                                go.Bar(name='enrollments', x=self.semesters, y=self.enrollments)])

        return bar_fig


Fall_Enrollment_df = pd.read_csv('C:/Users/fmixson/PycharmProjects/DivisionEnrollment/Fall_Division_Enrollment.csv', encoding='Latin')
Spring_Enrollment_df = pd.read_csv('C:/Users/fmixson/PycharmProjects/DivisionEnrollment/Spring_Division_Enrollment.csv', encoding='Latin')
tableau_df = pd.read_csv('C:/Users/fmixson/Desktop/Dashboard_files/Enrollment Counts - table.csv', encoding='Latin')
pd.set_option('display.max_columns', None)

a = DivisionEnrollmentsbySemester(tableau_df=tableau_df)
semester, enrollments = a.semester_and_enrollment_lists()

b = SpringDivisionEnrollments(spring_enrollment=Spring_Enrollment_df, spring_semesters=semester, spring_max_enrollments=enrollments)
enrollments, semesters, size = b.calculate_spring_enrollment()
c = BuildWebsite(enrollments=enrollments, semesters=semesters, size=size)
bar_fig = c.construct_graphs()



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
            dbc.Col(html.Div(dcc.Graph(id='graph1', figure=bar_fig)), width=6),
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