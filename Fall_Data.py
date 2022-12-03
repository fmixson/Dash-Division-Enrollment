class FallTableau:

    def __init__(self, fall_tableau_df):
        self.fall_tableau_df = fall_tableau_df

    def fall_semesters_and_enrollment_lists(self):

        self.fall_tableau_df.fillna(0, inplace=True)
        self.fall_tableau_df.replace(',', '', regex=True, inplace=True)

        self.fall_tableau_df[['Fall 2016', 'Fall 2017', 'Fall 2018', 'Fall 2019', 'Fall 2020', 'Fall 2021']] = \
            self.fall_tableau_df[
                ['Fall 2016', 'Fall 2017', 'Fall 2018', 'Fall 2019', 'Fall 2020', 'Fall 2021']].astype(
                str).astype(int)

        subset_fall_tableau_df = self.fall_tableau_df[
            ['Division', 'Department', 'Subject', 'Course', 'Fall 2016', 'Fall 2017', 'Fall 2018', 'Fall 2019', 'Fall 2020', 'Fall 2021']]

        div_totals = subset_fall_tableau_df.groupby('Division').agg(
            {'Fall 2016': 'sum', 'Fall 2017': 'sum', 'Fall 2018': 'sum',
             'Fall 2019': 'sum', 'Fall 2020': 'sum', 'Fall 2021': 'sum'}).reset_index()
        div_totals_series = div_totals.iloc[0]

        div_totals_list = div_totals_series.values.tolist()
        div_index_list = div_totals_series.index.values.tolist()

        fall_semesters = div_index_list[1:]
        fall_enrollments = div_totals_list[1:]

        return fall_semesters, fall_enrollments

class FallDivisionEnrollments:

    def __init__(self, fall_enrollment, fall_semesters, fall_max_enrollments):
        self.fall_enrollment = fall_enrollment
        self.fall_semesters = fall_semesters
        self.fall_max_enrollments = fall_max_enrollments

    def calculate_fall_enrollment(self):
        fall_size = [0, 0, 0, 0, 0, 0]
        fall_size_enrollment = self.fall_enrollment['Size'].sum()
        fall_max_enrollment = self.fall_enrollment['Max'].sum()
        self.fall_max_enrollments.append(fall_max_enrollment)
        fall_size.append(fall_size_enrollment)
        self.fall_semesters.append('Fall 2023')
        return self.fall_max_enrollments, self.fall_semesters, fall_size

    def calculate_sessions(self):

        for i in range(len(self.fall_enrollment)):

            if 'Regular' in self.fall_enrollment.loc[i, 'Session']:
                self.fall_enrollment.loc[i, 'Session'] = '18'
            if 'Fifteen' in self.fall_enrollment.loc[i, 'Session']:
                self.fall_enrollment.loc[i,'Session'] = '15'
            if '10/17' in self.fall_enrollment.loc[i, 'Session']:
                self.fall_enrollment.loc[i,'Session'] = '9A'
            if '10/18' in self.fall_enrollment.loc[i, 'Session']:
                    self.fall_enrollment.loc[i, 'Session'] = '9A'
            if '10/13' in self.fall_enrollment.loc[i, 'Session']:
                self.fall_enrollment.loc[i,'Session'] = '9B'
            if '10/14' in self.fall_enrollment.loc[i, 'Session']:
                self.fall_enrollment.loc[i,'Session'] = '9B'
            if '9/6' in self.fall_enrollment.loc[i, 'Session']:
                self.fall_enrollment.loc[i,'Session'] = '15'
            if '9/26' in self.fall_enrollment.loc[i, 'Session']:
                self.fall_enrollment.loc[i,'Session'] = '12'
            if 'Six' in self.fall_enrollment.loc[i, 'Session']:
                self.fall_enrollment.loc[i,'Session'] = '6'

        sessions_df = self.fall_enrollment.groupby('Session').agg({'Class': 'count', 'Size':'sum', 'Max': 'sum'})

        print(sessions_df)


