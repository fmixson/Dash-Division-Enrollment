import numpy as np
import pandas as pd
import openpyxl
import plotly.express as px

df = pd.read_csv('C:/Users/fmixson/Desktop/Dashboard_files/Copy of Liberal Arts AHC and Undecided Spring 2023 ENR 2023.01.17.csv', encoding='Latin')
pd.set_option('display.max_columns', None)
df.sort_values(by=['Employee ID', 'Course'], inplace=True)
print(df)
df = df[df['Enrollment Drop Date'].isnull()].reset_index()
for i in range(len(df)-1):
    if df.loc[i, 'Employee ID'] == df.loc[i+1, 'Employee ID']:
        if df.loc[i, 'Course'] == df.loc[i+1, 'Course']:
            df.loc[i,'Instruction Mode Description'] = 'Laboratory'
df = df[df['Instruction Mode Description'] != 'Laboratory']
df['Enrollment Add Date'] = pd.to_datetime(df['Enrollment Add Date'], infer_datetime_format=True)
df.to_excel('test_sheet.xlsx')
# print(df)
subset_df = df[['Enrollment Add Date', 'Course']]
# print(subset_df.to_string())
group_dates = subset_df.groupby('Enrollment Add Date').count().reset_index()
print(group_dates.to_string())

eighteen = df[df['Session Code'] == '1']

day_count = 1
week_count = 1
for i in range(len(group_dates)):
    if day_count < 7:
        group_dates.loc[i, 'Week'] = week_count
        day_count += 1
    else:
        group_dates.loc[i, 'Week'] = week_count
        day_count = 1
        week_count += 1


group_weeks = group_dates.groupby('Week').agg({'Course': 'sum'}).reset_index()
print(type(group_weeks))
group_weeks.loc[0,'Total'] = group_weeks.loc[0, 'Course']
for i in range(1, len(group_weeks)):
    group_weeks.loc[i, 'Total'] = group_weeks.loc[i, 'Course'] + group_weeks.loc[i-1, 'Total']
print(group_weeks)

sessions = ['1', '15L', '15B', '9A', '9B', '6A', '6B', '6C']
for session in sessions:
    session_df = df[df['Session Code'] == session]
    subset_df = session_df[['Enrollment Add Date', 'Session Code', 'Course']]
    group_dates = subset_df.groupby('Enrollment Add Date').count().reset_index()


    day_count = 1
    week_count = 1
    for i in range(len(group_dates)):
        if day_count < 7:
            group_dates.loc[i, 'Week'] = week_count
            day_count += 1
        else:
            group_dates.loc[i, 'Week'] = week_count
            day_count = 1
            week_count += 1

    group_weeks = group_dates.groupby('Week').agg({'Course': 'sum'}).reset_index()
    # print(type(group_weeks))
    group_weeks.loc[0, 'Total'] = group_weeks.loc[0, 'Course']
    for i in range(1, len(group_weeks)):
        group_weeks.loc[i, 'Total'] = group_weeks.loc[i, 'Course'] + group_weeks.loc[i - 1, 'Total']
        sessions_df[session] = group_weeks['Total']
        # print('sessions', sessions_df)

fig = px.line(group_weeks, x=group_weeks['Week'], y=group_weeks['Total'])
# fig2 = px.scatter(group_dates, x=group_dates['Enrollment Add Date'], y=group_dates['Course'])
fig.show()
# fig2.show()
