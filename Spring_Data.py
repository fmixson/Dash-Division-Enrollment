class SpringTableau:

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
    
    def calculate_sessions(self):
        print('first', self.spring_enrollment)
        less_than_ten_df = self.spring_enrollment.loc[(self.spring_enrollment['Size'] <= 10) & ((self.spring_enrollment['Session'] == '18') |
                                                    (self.spring_enrollment['Session'] == '15A') | (self.spring_enrollment['Session'] == '9A'))].reset_index()
                           # & \
                           # (self.spring_enrollment[self.spring_enrollment['Session'] == '15A']) & \
                           # (self.spring_enrollment[self.spring_enrollment['Session'] == '15A'])
        self.spring_enrollment['Session'] = self.spring_enrollment['Session'].replace([''], " ")
        print('Spring', self.spring_enrollment)
        sessions_df = self.spring_enrollment.groupby('Session').agg({'Class': 'count', 'Size':'sum', 'Max': 'sum'}).reset_index()
        sessions_df['Fill'] = sessions_df['Size'] / sessions_df['Max']
        modalities_df = self.spring_enrollment.groupby('Room').agg({'Class': 'count', 'Size':'sum', 'Max': 'sum'}).reset_index()
        modalities_df = modalities_df.iloc[1:5, 0:]
        modalities_df['Fill'] = modalities_df['Size'] / modalities_df['Max']
        # # sessions_df['Fill'] = sessions_df['Size'] / sessions_df['Max']
        print(sessions_df)
        print(modalities_df)
        return sessions_df, modalities_df, less_than_ten_df.loc[0:,3:]