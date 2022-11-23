from dash import Dash, dash_table, html, dcc
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
import numpy

df = pd.read_csv('C:/Users/fmixson/PycharmProjects/DivisionEnrollment/Division_Enrollment_Dash.csv', encoding='Latin')
pd.set_option('display.max_columns', None)

subset_modality_df = df[['Room', 'Course', 'Class', 'Size', 'Max', 'FTES']]

df5 = subset_modality_df.groupby('Room').agg({'Class': 'count'}).reset_index()
total_modality = df5['Class'].sum()
df5['Perc'] = df5['Class'] / total_modality
random_x = df5['Perc']
names = df5['Room']

fig = px.pie(values=random_x, names=names)
fig.show()



