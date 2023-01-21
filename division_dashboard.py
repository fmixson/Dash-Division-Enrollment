from dash import Dash, dash_table, html, dcc, Input, Output
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import numpy

df = pd.read_csv('C:/Users/fmixson/PycharmProjects/DivisionEnrollment/Spring_Division_Enrollment.csv', encoding='Latin')

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
        dbc.Col(dcc.Graph(id='pie_chart'), width=6),
        dbc.Col(dcc.Graph(id='session_pie_chart'), width=6)
            ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='Modality2_barchart'), width=6),
        dbc.Col(dcc.Graph(id='session_barchart'), width=6)
    ])

    ])

@app.callback(
    Output(component_id='Modality2_barchart', component_property='figure'),
    Input(component_id='dept_dropdown', component_property='value')
)
def modality_barchart(dept):
    if dept is None:
        subset_df = df[['Dept', 'Modality2', 'Class', 'Size', 'Max']]
        group_modalities = subset_df.groupby('Modality2').agg({'Class':'count', 'Size': 'sum', 'Max': 'sum'}).reset_index()
        group_modalities['Fill'] = group_modalities['Size'] / group_modalities['Max']
        # group_modalities = group_modalities.iloc[1:5, :]

        bar_fig = go.Figure(data=[
            go.Bar(name='Size', x=group_modalities['Modality2'], y=group_modalities['Size'], text=group_modalities['Size']),
            go.Bar(name='Capacity', x=group_modalities['Modality2'],y=group_modalities['Max'], text=group_modalities['Max'])
        ])
        bar_fig.update_layout(barmode='group')
        return bar_fig
    else:
        subset_df = df[['Dept', 'Modality2', 'Class', 'Size', 'Max']]
        subset_dff = subset_df[subset_df['Dept'] == dept]
        group_modalities = subset_dff.groupby('Modality2').agg({'Class': 'count', 'Size': 'sum', 'Max': 'sum'}).reset_index()
        group_modalities['Fill'] = group_modalities['Size'] / group_modalities['Max']
        # group_modalities = group_modalities.iloc[1:5, :]

        bar_fig = go.Figure(data=[
            go.Bar(name='Size', x=group_modalities['Modality2'], y=group_modalities['Size'], text=group_modalities['Size']),
            go.Bar(name='Capacity', x=group_modalities['Modality2'], y=group_modalities['Max'], text=group_modalities['Max'])
        ])
        bar_fig.update_layout(barmode='group')

        return bar_fig

@app.callback(
    Output(component_id='pie_chart', component_property='figure'),
    Input(component_id='dept_dropdown', component_property='value')
)
def modality_pie_chart(dept):
    if dept is None:
        subset_df = df[['Dept', 'Modality2', 'Class', 'Size', 'Max']]
        group_modalities = subset_df.groupby('Modality2').agg({'Class':'count', 'Size': 'sum', 'Max': 'sum'}).reset_index()
        total_count = group_modalities['Class'].sum()
        group_modalities['Perc'] = group_modalities['Class'] / total_count
        print(group_modalities)
        fig = px.pie(group_modalities, values='Perc', names='Modality2')
        return fig
    else:
        subset_df = df[['Dept', 'Modality2', 'Class', 'Size', 'Max']]
        subset_dff = subset_df[subset_df['Dept'] == dept]
        group_modalities = subset_dff.groupby('Modality2').agg({'Class': 'count', 'Size': 'sum', 'Max': 'sum'}).reset_index()
        total_count = group_modalities['Class'].sum()
        group_modalities['Perc'] = group_modalities['Class'] / total_count
        fig = px.pie(group_modalities, values='Perc', names='Modality2')
        return fig

@app.callback(
    Output(component_id='session_pie_chart', component_property='figure'),
    Input(component_id='dept_dropdown', component_property='value')
)
def session_pie_chart(dept):
    if dept is None:
        subset_df = df[['Dept', 'Session', 'Class', 'Size', 'Max']]
        group_modalities = subset_df.groupby('Session').agg({'Class':'count', 'Size': 'sum', 'Max': 'sum'}).reset_index()
        total_count = group_modalities['Class'].sum()
        group_modalities['Perc'] = group_modalities['Class'] / total_count
        session_fig = px.pie(group_modalities, values='Perc', names='Session')
        return session_fig
    else:
        subset_df = df[['Dept', 'Session', 'Class', 'Size', 'Max']]
        subset_dff = subset_df[subset_df['Dept'] == dept]
        group_modalities = subset_dff.groupby('Session').agg({'Class': 'count', 'Size': 'sum', 'Max': 'sum'}).reset_index()
        total_count = group_modalities['Class'].sum()
        group_modalities['Perc'] = group_modalities['Class'] / total_count
        session_fig = px.pie(group_modalities, values='Perc', names='Session')
        return session_fig

@app.callback(
        Output(component_id='session_barchart', component_property='figure'),
        Input(component_id='dept_dropdown', component_property='value')
    )
def session_barchart(dept):
        if dept is None:
            subset_df = df[['Dept', 'Session', 'Class', 'Size', 'Max']]
            group_sessions = subset_df.groupby('Session').agg(
                {'Class': 'count', 'Size': 'sum', 'Max': 'sum'}).reset_index()
            group_sessions['Fill'] = group_sessions['Size'] / group_sessions['Max']
            # group_sessions = group_sessions.iloc[1:5, :]
            print(group_sessions)
            bar_fig = go.Figure(data=[
                go.Bar(name='Size', x=group_sessions['Session'], y=group_sessions['Size'], text=group_sessions['Size']),
                go.Bar(name='Capacity', x=group_sessions['Session'], y=group_sessions['Max'], text=group_sessions['Max'])
            ])
            bar_fig.update_layout(barmode='group')
            return bar_fig
        else:
            subset_df = df[['Dept', 'Session', 'Class', 'Size', 'Max']]
            subset_dff = subset_df[subset_df['Dept'] == dept]
            group_sessions = subset_dff.groupby('Session').agg(
                {'Class': 'count', 'Size': 'sum', 'Max': 'sum'}).reset_index()
            group_sessions['Fill'] = group_sessions['Size'] / group_sessions['Max']
            # group_sessions = group_sessions.iloc[1:5, :]
            print(group_sessions)
            bar_fig = go.Figure(data=[
                go.Bar(name='Size', x=group_sessions['Session'], y=group_sessions['Size'], text=group_sessions['Size']),
                go.Bar(name='Capacity', x=group_sessions['Session'], y=group_sessions['Max'], text=group_sessions['Max'])
            ])
            bar_fig.update_layout(barmode='group')

            return bar_fig


app.run(debug=True)