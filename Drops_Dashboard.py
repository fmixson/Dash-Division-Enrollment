import numpy as np
import pandas as pd
import openpyxl
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv('C:/Users/fmixson/Desktop/Dashboard_files/Copy of Liberal Arts AHC and Undecided Spring 2023 ENR 2023.01.30.csv', encoding='Latin')
scheduleplus_df = pd.read_csv('C:/Users/fmixson/PycharmProjects/DivisionEnrollment/Fall_Division_Enrollment.csv')
scheduleplus_df = scheduleplus_df.drop('index', axis=1).reset_index()
# print(df.dtypes, scheduleplus_df.dtypes)
print(scheduleplus_df)
pd.set_option('display.max_columns', None)
df.sort_values(by=['Employee ID', 'Course'], inplace=True)
# print(df)
for i in range(len(df)):
    if df.loc[i, 'Enrollment Drop Date'] != 'NaN':
        df.loc[i, 'Enrollment Drop Date'] = -1
print(df)
df = df[df['Enrollment Drop Date'].isnull()].reset_index()
for i in range(len(df)-1):
    if df.loc[i, 'Employee ID'] == df.loc[i+1, 'Employee ID']:
        if df.loc[i, 'Course'] == df.loc[i+1, 'Course']:
            df.loc[i,'Instruction Mode Description'] = 'Laboratory'
df = df[df['Instruction Mode Description'] != 'Laboratory']
df['Enrollment Add Date'] = pd.to_datetime(df['Enrollment Add Date'], infer_datetime_format=True)
print(df.to_string())
df = df.reset_index()
del df['level_0']
del df['index']
print(df.to_string())
subset_df = df[['Enrollment Add Date', 'Course']]
# print(scheduleplus_df.to_string())
group_dates = subset_df.groupby('Enrollment Add Date').count().reset_index()

for i in range(len(df)):
    for j in range(len(scheduleplus_df)):
        # print(df.loc[i, 'Section Number'], scheduleplus_df.loc[j, 'Class'])
        if df.loc[i, 'Section Number'] == scheduleplus_df.loc[j, 'Class']:
            df.loc[i, 'Session Code'] = scheduleplus_df.loc[j, 'Session']
            df.loc[i, 'Instruction Mode Description'] = scheduleplus_df.loc[j, 'Modality2']


df.to_excel('test_sheet.xlsx')
# subset_df = df[['Enrollment Add Date', 'Course']]
group_dates = subset_df.groupby('Enrollment Add Date').count().reset_index()


day_count = 1
week_count = 1
week_of = {}
for i in range(len(group_dates)):
    if day_count < 7:
        group_dates.loc[i, 'Week'] = week_count
        day_count += 1
    else:
        group_dates.loc[i, 'Week'] = week_count
        day_count = 1
        week_count += 1


group_weeks = group_dates.groupby('Week').agg({'Course': 'sum'}).reset_index()
# print('1', group_weeks)
# print(type(group_weeks))
# print(group_weeks.dtypes)
# group_weeks.columns=['Week', 'Course']
group_weeks.loc[0,'Total'] = group_weeks.loc[0, 'Course']
for i in range(1, len(group_weeks)):
    group_weeks.loc[i, 'Total'] = group_weeks.loc[i, 'Course'] + group_weeks.loc[i-1, 'Total']
# print(group_weeks)
# fig = px.line(group_weeks, x='Week', y='Total')
# fig.show()

division_df = group_weeks.rename(columns={'Total': 'Division'})
Total_df = division_df.drop('Course', axis=1)
# sessions_df.loc[0: ,'Division'] = group_weeks.loc[0: ,'Total']
# sessions_df = group_weeks['Total']
# print(group_weeks)
# print(Total_df)
#
sessions = ['18', '15A', '15B', '9A', '9B', '6']
for session in sessions:
    session_df = df[df['Session Code'] == session]
    # print('ses', session_df)
    subset_df = session_df[['Enrollment Add Date', 'Course']]
    print('sub', subset_df)
    session_group_dates = subset_df.groupby('Enrollment Add Date').count().reset_index()
    # print('sgd', session_group_dates)
    day_count = 1
    week_count = 1
    for i in range(len(session_group_dates)):
        if day_count < 7:
            session_group_dates.loc[i, 'Week'] = week_count
            day_count += 1
        else:
            session_group_dates.loc[i, 'Week'] = week_count
            day_count = 1
            week_count += 1
    print('sgd', session_group_dates)
    session_group_weeks = session_group_dates.groupby('Week').agg({'Course': 'sum'}).reset_index()
    session_group_weeks.columns = ['Weeks', 'Course']
    print('sgw',session_group_weeks)
    session_group_weeks.loc[0, 'Total'] = session_group_weeks.loc[0, 'Course']
    print('weeks', group_weeks)
    for i in range(1, len(session_group_weeks)):
        session_group_weeks.loc[i, 'Total'] = session_group_weeks.loc[i, 'Course'] + session_group_weeks.loc[i - 1, 'Total']
        Total_df[session] = session_group_weeks['Total']
        print(Total_df)
session_fig = go.Figure()
#
session_fig.add_trace(go.Scatter(x=Total_df['Week'], y=Total_df['Division'],
                          mode='lines',
                          name='Division'))
session_fig.add_trace(go.Scatter(x=Total_df['Week'], y=Total_df['18'],
                          mode='lines',
                          name='18 Week'))
session_fig.show()

# """
# THIS SECTION IDENTIFIES TREND BY MODALITY
# """
#
# modalities = ['Online', 'In Person', 'Hybrid', 'Remote']
# for modality in modalities:
#     modalities_df = df[df['Modality'] == session]
#     subset_df = modalities_df[['Enrollment Add Date', 'Modality', 'Course']]
#     group_dates = subset_df.groupby('Enrollment Add Date').count().reset_index()
#
#
#     day_count = 1
#     week_count = 1
#     for i in range(len(group_dates)):
#         if day_count < 7:
#             group_dates.loc[i, 'Week'] = week_count
#             day_count += 1
#         else:
#             group_dates.loc[i, 'Week'] = week_count
#             day_count = 1
#             week_count += 1
#
#     group_weeks = group_dates.groupby('Week').agg({'Course': 'sum'}).reset_index()
#     # print(type(group_weeks))
#     group_weeks.loc[0, 'Total'] = group_weeks.loc[0, 'Course']
#     for i in range(1, len(group_weeks)):
#         group_weeks.loc[i, 'Total'] = group_weeks.loc[i, 'Course'] + group_weeks.loc[i - 1, 'Total']
#         modalities_df[modality] = group_weeks['Total']


""" 
THIS SECTION IDENTIFIES TREND BY Race and Ethnicity
"""

# ethnicities = ['Native Hawaiian or Other Pacific Islander', 'Asian', 'Black or African American', 'Hispanic or Latino', 'Two or More Races', 'Race/ethnicity Unknown',
# 'American Indian or Alaskan Native', 'Decline to State', 'White']
# for ethnicity in ethnicities:
#     ethnicity_df = df[df['Race/Ethnicity'] == ethnicity]
#     subset_df = ethnicity_df.groupby('Enrollment Add Date').count().reset_index()
#     # print(ethnicity, ethnicity_df)
#
#     day_count = 1
#     week_count = 1
#     for i in range(len(group_dates)):
#         if day_count < 7:
#             group_dates.loc[i, 'Week'] = week_count
#             day_count += 1
#         else:
#             group_dates.loc[i, 'Week'] = week_count
#             day_count = 1
#             week_count += 1
#     # print(group_dates)
#     group_weeks = group_dates.groupby('Week').agg({'Course': 'sum'}).reset_index()
#     # print(type(group_weeks))
#     group_weeks.loc[0, 'Total'] = group_weeks.loc[0, 'Course']
#     for i in range(1, len(group_weeks)):
#         group_weeks.loc[i, 'Total'] = group_weeks.loc[i, 'Course'] + group_weeks.loc[i - 1, 'Total']
#         ethnicity_df[ethnicity] = group_weeks['Total']
#     print('ethnicity', ethnicity_df.head())
# ethnicity_fig = go.Figure()
#
# # ethnicity_fig.add_trace(go.Scatter(x=ethnicity_df['Week'], y=ethnicity_df['Division'],
# #                          mode='lines',
# #                          name='Division'))
#
# # ethnicity_fig.add_trace(go.Scatter(x=ethnicity_df['Week'], y=ethnicity_df['American Indian or Alaskan Native'],
# #                          mode='lines',
# #                          name='Online'))
#
# ethnicity_fig.add_trace(go.Scatter(x=ethnicity_df['Week'], y=ethnicity_df['Asian'],
#                          mode='lines',
#                          name='In Person'))
#
# ethnicity_fig.add_trace(go.Scatter(x=ethnicity_df['Week'], y=ethnicity_df['Black or African American'],
#                          mode='lines',
#                          name='Hybrid'))
#
# ethnicity_fig.add_trace(go.Scatter(x=ethnicity_df['Week'], y=ethnicity_df['Decline to State'],
#                          mode='lines',
#                          name='Remote'))
#
# ethnicity_fig.add_trace(go.Scatter(x=ethnicity_df['Week'], y=ethnicity_df['Two or more Races'],
#                          mode='lines',
#                          name='Remote'))
#
# ethnicity_fig.add_trace(go.Scatter(x=ethnicity_df['Week'], y=ethnicity_df['Native Hawaiian or Other Pacific Islander'],
#                          mode='lines',
#                          name='Remote'))
#
# ethnicity_fig.add_trace(go.Scatter(x=ethnicity_df['Week'], y=ethnicity_df['Hispanic or Latino'],
#                          mode='lines',
#                          name='Remote'))
#
# ethnicity_fig.add_trace(go.Scatter(x=ethnicity_df['Week'], y=ethnicity_df['Hispanic or Latino'],
#                          mode='lines',
#                          name='Remote'))

#
#
# modality_fig = go.Figure()
#
# modality_fig.add_trace(go.Scatter(x=modalities_df['Week'], y=modalities_df['Division'],
#                          mode='lines',
#                          name='Division'))
#
# modality_fig.add_trace(go.Scatter(x=modalities_df['Week'], y=modalities_df['Online'],
#                          mode='lines',
#                          name='Online'))
#
# modality_fig.add_trace(go.Scatter(x=modalities_df['Week'], y=modalities_df['In Person'],
#                          mode='lines',
#                          name='In Person'))
#
# modality_fig.add_trace(go.Scatter(x=modalities_df['Week'], y=modalities_df['Hybrid'],
#                          mode='lines',
#                          name='Hybrid'))
#
# modality_fig.add_trace(go.Scatter(x=modalities_df['Week'], y=modalities_df['Remote'],
#                          mode='lines',
#                          name='Remote'))




# fig = go.Figure()
# fig.add_line(x=sessions_df['Week'], y=sessions_df['Total'])

# fig.add_trace(go.Scatter(x=sessions_df['Week'], y=sessions_df['Division'],
#                          mode='lines',
#                          name='Division'))
#
# fig.add_trace(go.Scatter(x=sessions_df['Week'], y=sessions_df['18'],
#                          mode='lines',
#                          name='Regular'))
#
# # fig.add_trace(go.Scatter(x=sessions_df['Week'], y=sessions_df['15A'],
# #                          mode='lines',
# #                          name='15A'))
#
# fig.add_trace(go.Scatter(x=sessions_df['Week'], y=sessions_df['15B'],
#                          mode='lines',
#                          name='15B'))
#
# fig.add_trace(go.Scatter(x=sessions_df['Week'], y=sessions_df['9A'],
#                          mode='lines',
#                          name='9A'))
#
# fig.add_trace(go.Scatter(x=sessions_df['Week'], y=sessions_df['9B'],
#                          mode='lines',
#                          name='9B'))

# fig.show()