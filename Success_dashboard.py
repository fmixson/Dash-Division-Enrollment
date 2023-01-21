from dash import Dash, dash_table, html, dcc, Input, Output
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import numpy
import openpyxl


df = pd.read_csv('C:/Users/fmixson/PycharmProjects/DivisionEnrollment/BE_Success_by_Modality.csv')
print(df)
# group_modalities = df.groupby('Room').agg({'Class':'count', 'Success': 'sum', 'Completion': 'sum'}).reset_index()
# group_modalities['Rate'] = group_modalities['Success'] / group_modalities['Completion']
# modality = group_modalities
# print(modality)
# fig = px.bar(modality, y='Rate', x='Room')
# fig.show()

app = Dash(__name__,
           external_stylesheets=[dbc.themes.BOOTSTRAP]
           )
app.layout = html.Div(
    [
    html.Div(
    dcc.Dropdown(id='dept_dropdown',
                 options=[{'label': dept, 'value': dept}
                          for dept in df['Dept'].unique()]
                 )),
        dbc.Row([
        dbc.Col(html.H2('Success and Enrollment by Modalities'), width=6 ,style={'textAlign': 'center'}),
        dbc.Col(html.H2('Success and Enrollment by Sessions'), width=6 ,style={'textAlign': 'center'})]),
        dbc.Row([
        dbc.Col(dcc.Graph(id='modality_success_bar_chart'), width=6),
        dbc.Col(dcc.Graph(id='session_success_bar_chart'), width=6)
            ]),
        dbc.Row([
        dbc.Col(html.H2('Success Rates by Modalities'), width=6 ,style={'textAlign': 'center'}),
        dbc.Col(html.H2('Success Rates by Sessions'), width=6 ,style={'textAlign': 'center'})]),
        dbc.Row([
        dbc.Col(dcc.Graph(id='modality_success_single_bar_chart'), width=6),
        dbc.Col(dcc.Graph(id='session_success_single_bar_chart'), width=6)
    ]),
        ])

@app.callback(
    Output(component_id='modality_success_bar_chart', component_property='figure'),
    Input(component_id='dept_dropdown', component_property='value'))
def modality_bar_chart(dept):
    if dept is None:
        # subset_df = df[['Dept', 'Modality', 'Class', 'Size', 'Max']]
        group_modalities = df.groupby('Room').agg({'Class':'count', 'Success': 'sum', 'Completion': 'sum'}).reset_index()
        print(group_modalities)
        group_modalities['Rate'] = group_modalities['Success'] / group_modalities['Completion']
        print(group_modalities)
        fig = go.Figure(data=[
            go.Bar(name='Success', x=group_modalities['Room'], y=group_modalities['Success'],
                   text=group_modalities['Success']),
            go.Bar(name='Completion', x=group_modalities['Room'], y=group_modalities['Completion'],
                   text=group_modalities['Completion'])
        ])
        return fig
    else:
        # subset_df = df[['Dept', 'Modality', 'Class', 'Size', 'Max']]
        dept_df = df[df['Dept'] == dept]
        group_modalities = dept_df.groupby('Room').agg({'Class': 'count', 'Success': 'sum', 'Completion': 'sum'}).reset_index()
        group_modalities['Rate'] = group_modalities['Success'] / group_modalities['Completion']
        fig = go.Figure(data=[
            go.Bar(name='Success', x=group_modalities['Room'], y=group_modalities['Success'],
                   text=group_modalities['Success']),
            go.Bar(name='Completion', x=group_modalities['Room'], y=group_modalities['Completion'],
                   text=group_modalities['Completion'])
        ])
        return fig


@app.callback(
    Output(component_id='session_success_bar_chart', component_property='figure'),
    Input(component_id='dept_dropdown', component_property='value')
)
def session_bar_chart(dept):
    if dept is None:
        # subset_df = df[['Dept', 'Session', 'Class', 'Size', 'Max']]
        group_modalities = df.groupby('Session').agg({'Class':'count', 'Success': 'sum', 'Completion': 'sum'}).reset_index()
        # total_count = group_modalities['Size'].sum()
        group_modalities['Rate'] = group_modalities['Success'] / group_modalities['Completion']
        fig = go.Figure(data=[
            go.Bar(name='Success', x=group_modalities['Session'], y=group_modalities['Success'],
                   text=group_modalities['Success']),
            go.Bar(name='Completion', x=group_modalities['Session'], y=group_modalities['Completion'],
                   text=group_modalities['Completion'])
        ])
        return fig

    else:
        # subset_df = df[['Dept', 'Session', 'Class', 'Size', 'Max']]
        dept_df = df[df['Dept'] == dept]
        group_modalities = dept_df.groupby('Session').agg({'Class': 'count', 'Success': 'sum', 'Completion': 'sum'}).reset_index()
        group_modalities['Rate'] = group_modalities['Success'] / group_modalities['Completion']
        fig = go.Figure(data=[
            go.Bar(name='Success', x=group_modalities['Session'], y=group_modalities['Success'],
                   text=group_modalities['Success']),
            go.Bar(name='Completion', x=group_modalities['Session'], y=group_modalities['Completion'],
                   text=group_modalities['Completion'])
        ])
        return fig


@app.callback(
    Output(component_id='modality_success_single_bar_chart', component_property='figure'),
    Input(component_id='dept_dropdown', component_property='value')
)
def modalities_single_bar_chart(dept):
    if dept is None:
        # subset_df = df[['Dept', 'Session', 'Class', 'Size', 'Max']]
        group_modalities = df.groupby('Room').agg({'Class':'count', 'Success': 'sum', 'Completion': 'sum'}).reset_index()
        # total_count = group_modalities['Size'].sum()
        group_modalities['Rate'] = group_modalities['Success'] / group_modalities['Completion']
        fig = px.bar(group_modalities, x='Room', y='Rate', text_auto=True)
        return fig

    else:
        # subset_df = df[['Dept', 'Session', 'Class', 'Size', 'Max']]
        dept_df = df[df['Dept'] == dept]
        group_modalities = dept_df.groupby('Room').agg({'Class': 'count', 'Success': 'sum', 'Completion': 'sum'}).reset_index()
        group_modalities['Rate'] = group_modalities['Success'] / group_modalities['Completion']
        fig = px.bar(group_modalities, x='Room', y='Rate', text_auto=True)
        return fig


@app.callback(
    Output(component_id='session_success_single_bar_chart', component_property='figure'),
    Input(component_id='dept_dropdown', component_property='value')
)
def session_single_bar_chart(dept):
    if dept is None:
        # subset_df = df[['Dept', 'Session', 'Class', 'Size', 'Max']]
        group_modalities = df.groupby('Session').agg({'Class':'count', 'Success': 'sum', 'Completion': 'sum'}).reset_index()
        # total_count = group_modalities['Size'].sum()
        group_modalities['Rate'] = group_modalities['Success'] / group_modalities['Completion']
        session_fig = px.bar(group_modalities, y='Rate', x='Session', text_auto=True)
        return session_fig
    else:
        # subset_df = df[['Dept', 'Session', 'Class', 'Size', 'Max']]
        dept_df = df[df['Dept'] == dept]
        group_modalities = dept_df.groupby('Session').agg({'Class': 'count', 'Success': 'sum', 'Completion': 'sum'}).reset_index()
        group_modalities['Rate'] = group_modalities['Success'] / group_modalities['Completion']
        session_fig = px.bar(group_modalities, y='Rate', x='Session', text_auto='True')
        return session_fig




app.run(debug=True)