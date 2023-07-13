from dash import Dash, dash_table, html, dcc, Input, Output
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import numpy
import openpyxl

df = pd.read_csv('C:/Users/fmixson/PycharmProjects/DivisionEnrollment/lab_test.csv', encoding='Latin')
# modality_and_session_df = pd.read_excel('C:/Users/fmixson/PycharmProjects/DivisionEnrollment/BE_Success_by_Modality.xlsx')
# print(modality_and_session_df)
subset_df = df[['Dept', 'Modality2', 'Class', 'Size', 'Max']]
# print(subset_df.to_string())
group_modalities = subset_df.groupby('Modality2').agg({'Class':'count', 'Size': 'sum', 'Max': 'sum'}).reset_index()
# print(group_modalities.to_string())
total_count = group_modalities['Class'].sum()
# print('total count', total_count)
group_modalities['Perc'] = group_modalities['Class'] / total_count
# print('group modalities', group_modalities)
# fig = px.pie(group_modalities, values='Perc', names='Modality')
# fig.show()

app = Dash(__name__,
           external_stylesheets=[dbc.themes.BOOTSTRAP]
           )
app.layout = html.Div(
    [
    html.Div(
    dcc.Dropdown(id='div_dropdown',
                 options=[{'label': dept, 'value': dept}
                          for dept in df['Dept'].unique()]
                 )),
        # html.Div(
        #     dcc.Dropdown(id='success_dept_dropdown',
        #                  options=[{'label': dept, 'value': dept}
        #                           for dept in modality_and_session_df['Dept'].unique()]
        #                  )),

        dbc.Row([
        dbc.Col(html.H2('Modalities by % of Sections Offered'), width=6 ,style={'textAlign': 'center'}),
        dbc.Col(html.H2('Sessions by % of Sections Offered'), width=6 ,style={'textAlign': 'center'})]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='modality_pie_chart'), width=6),
        dbc.Col(dcc.Graph(id='session_pie_chart'), width=6)
            ]),
    dbc.Row([
        dbc.Col(html.H2('Modalities by % of Enrollment'), width=6 ,style={'textAlign': 'center'}),
        dbc.Col(html.H2('Sessions by % of Enrollment'), width=6 ,style={'textAlign': 'center'})]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='enroll_modality_pie_chart'), width=6),
        dbc.Col(dcc.Graph(id='enroll_session_pie_chart'), width=6)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='modality_barchart'), width=6),
        dbc.Col(dcc.Graph(id='session_barchart'), width=6)
    ]),
    # dbc.Row([
    #     dbc.Col(dcc.Graph(id='success_pie_chart'), width=6),

    # ]),
    # html.Div(
    #     dcc.Dropdown(id='success_dept_dropdown',
    #                  options=[{'label': dept, 'value': dept}
    #                           for dept in modality_and_session_df['Dept'].unique()]
    #                  )),

    ])

@app.callback(
    Output(component_id='modality_barchart', component_property='figure'),
    Input(component_id='div_dropdown', component_property='value')
)
def modality_barchart(dept):
    if dept is None:
        subset_df = df[['DIV', 'Modality2', 'Class', 'Size', 'Max']]
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
        subset_df = df[['DIV', 'Modality2', 'Class', 'Size', 'Max']]
        subset_dff = subset_df[subset_df['DIV'] == dept]
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
    Output(component_id='modality_pie_chart', component_property='figure'),
    Input(component_id='div_dropdown', component_property='value')
)
def modality_pie_chart(div):
    if div is None:
        subset_df = df[['DIV', 'Modality2', 'Class', 'Size', 'Max']]
        group_modalities = subset_df.groupby('Modality2').agg({'Class':'count', 'Size': 'sum', 'Max': 'sum'}).reset_index()
        total_count = group_modalities['Class'].sum()
        group_modalities['Perc'] = group_modalities['Class'] / total_count
        fig = px.pie(group_modalities, values='Perc', names='Modality2')
        return fig
    else:
        subset_df = df[['DIV', 'Modality2', 'Class', 'Size', 'Max']]
        subset_dff = subset_df[subset_df['DIV'] == div]
        group_modalities = subset_dff.groupby('Modality2').agg({'Class': 'count', 'Size': 'sum', 'Max': 'sum'}).reset_index()
        total_count = group_modalities['Class'].sum()
        group_modalities['Perc'] = group_modalities['Class'] / total_count
        fig = px.pie(group_modalities, values='Perc', names='Modality2')
        return fig

@app.callback(
    Output(component_id='session_pie_chart', component_property='figure'),
    Input(component_id='div_dropdown', component_property='value')
)
def session_pie_chart(div):
    if div is None:
        subset_df = df[['DIV', 'Session', 'Class', 'Size', 'Max']]
        group_modalities = subset_df.groupby('Session').agg({'Class':'count', 'Size': 'sum', 'Max': 'sum'}).reset_index()
        total_count = group_modalities['Class'].sum()
        group_modalities['Perc'] = group_modalities['Class'] / total_count
        session_fig = px.pie(group_modalities, values='Perc', names='Session')
        return session_fig
    else:
        subset_df = df[['DIV', 'Session', 'Class', 'Size', 'Max']]
        subset_dff = subset_df[subset_df['DIV'] == div]
        group_modalities = subset_dff.groupby('Session').agg({'Class': 'count', 'Size': 'sum', 'Max': 'sum'}).reset_index()
        total_count = group_modalities['Class'].sum()
        group_modalities['Perc'] = group_modalities['Class'] / total_count
        session_fig = px.pie(group_modalities, values='Perc', names='Session')
        return session_fig

@app.callback(
        Output(component_id='session_barchart', component_property='figure'),
        Input(component_id='div_dropdown', component_property='value')
    )
def session_barchart(div):
        if div is None:
            subset_df = df[['DIV', 'Session', 'Class', 'Size', 'Max']]
            group_sessions = subset_df.groupby('Session').agg(
                {'Class': 'count', 'Size': 'sum', 'Max': 'sum'}).reset_index()
            group_sessions['Fill'] = group_sessions['Size'] / group_sessions['Max']
            print(group_sessions)
            bar_fig = go.Figure(data=[
                go.Bar(name='Size', x=group_sessions['Session'], y=group_sessions['Size'], text=group_sessions['Size']),
                go.Bar(name='Capacity', x=group_sessions['Session'], y=group_sessions['Max'], text=group_sessions['Max'])
            ])
            bar_fig.update_layout(barmode='group')
            return bar_fig
        else:
            subset_df = df[['DIV', 'Session', 'Class', 'Size', 'Max']]
            subset_dff = subset_df[subset_df['DIV'] == div]
            group_sessions = subset_dff.groupby('Session').agg(
                {'Class': 'count', 'Size': 'sum', 'Max': 'sum'}).reset_index()
            group_sessions['Fill'] = group_sessions['Size'] / group_sessions['Max']
            print(group_sessions)
            bar_fig = go.Figure(data=[
                go.Bar(name='Size', x=group_sessions['Session'], y=group_sessions['Size'], text=group_sessions['Size']),
                go.Bar(name='Capacity', x=group_sessions['Session'], y=group_sessions['Max'], text=group_sessions['Max'])
            ])
            bar_fig.update_layout(barmode='group')

            return bar_fig

@app.callback(
    Output(component_id='enroll_modality_pie_chart', component_property='figure'),
    Input(component_id='div_dropdown', component_property='value')
)
def modality_pie_chart(div):
    if div is None:
        subset_df = df[['DIV', 'Modality2', 'Class', 'Size', 'Max']]
        group_modalities = subset_df.groupby('Modality2').agg({'Class':'count', 'Size': 'sum', 'Max': 'sum'}).reset_index()
        total_count = group_modalities['Size'].sum()
        group_modalities['Perc'] = group_modalities['Size'] / total_count
        fig = px.pie(group_modalities, values='Perc', names='Modality2')
        return fig
    else:
        subset_df = df[['DIV', 'Modality2', 'Class', 'Size', 'Max']]
        subset_dff = subset_df[subset_df['DIV'] == div]
        group_modalities = subset_dff.groupby('Modality2').agg({'Class': 'count', 'Size': 'sum', 'Max': 'sum'}).reset_index()
        total_count = group_modalities['Size'].sum()
        group_modalities['Perc'] = group_modalities['Size'] / total_count
        fig = px.pie(group_modalities, values='Perc', names='Modality2')
        return fig


@app.callback(
    Output(component_id='enroll_session_pie_chart', component_property='figure'),
    Input(component_id='div_dropdown', component_property='value')
)
def session_pie_chart(div):
    if div is None:
        subset_df = df[['DIV', 'Session', 'Class', 'Size', 'Max']]
        group_modalities = subset_df.groupby('Session').agg({'Class':'count', 'Size': 'sum', 'Max': 'sum'}).reset_index()
        total_count = group_modalities['Size'].sum()
        group_modalities['Perc'] = group_modalities['Size'] / total_count
        session_fig = px.pie(group_modalities, values='Perc', names='Session')
        return session_fig
    else:
        subset_df = df[['DIV', 'Session', 'Class', 'Size', 'Max']]
        subset_dff = subset_df[subset_df['Dept'] == div]
        group_modalities = subset_dff.groupby('Session').agg({'Class': 'count', 'Size': 'sum', 'Max': 'sum'}).reset_index()
        total_count = group_modalities['Size'].sum()
        group_modalities['Perc'] = group_modalities['Size'] / total_count
        session_fig = px.pie(group_modalities, values='Perc', names='Session')
        return session_fig

# @app.callback(
#     Output(component_id='success_pie_chart', component_property='figure'),
#     Input(component_id='success_dept_dropdown', component_property='value')
# )
# # def success_pie_chart(dept):
#     if dept is None:
#         # modality_and_session_subset = [['Dept', 'Class','Session', 'Completion', 'Success']]
#         # print(type(modality_and_session_df))
#         group_session = modality_and_session_df.groupby('Session').agg({'Class':'count', 'Success': 'sum', 'Completion': 'sum'}).reset_index()
#
#         group_session['Rate'] = group_session['Success'] / group_session['Completion']
#         print(group_session)
#         # group_modalities['Perc'] = group_modalities['Success'] / total_count
#         success_fig = px.bar(group_session, y='Rate', x='Session')
#         success_fig.show()
#         return success_fig
#     else:
#         subset_df = df[['Dept', 'Session', 'Class', 'Size', 'Max']]
#         subset_dff = subset_df[subset_df['Dept'] == dept]
#         group_modalities = subset_dff.groupby('Session').agg({'Class': 'count', 'Size': 'sum', 'Max': 'sum'}).reset_index()
#         total_count = group_modalities['Class'].sum()
#         group_modalities['Perc'] = group_modalities['Class'] / total_count
#         success_fig = px.pie(group_modalities, values='Perc', names='Session')
#         return success_fig

app.run(debug=True)