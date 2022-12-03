import plotly.graph_objects as go
class BuildDashboard:

    def __init__(self, enrollments, semesters, size, fall_max_enrollments, fall_semesters, fall_size):
        self.enrollments = enrollments
        self.semesters = semesters
        self.size = size
        self.fall_max_enrollments = fall_max_enrollments
        self.fall_semesters = fall_semesters
        self.fall_size = fall_size

    def construct_spring_graphs(self):

        bar_fig = go.Figure(data=[
                                go.Bar(name='actual', x=self.semesters, y=self.size),
                                go.Bar(name='enrollments', x=self.semesters, y=self.enrollments)])
        return bar_fig


    def construct_fall_graphs(self):

        fall_bar_fig = go.Figure(data=[
                                go.Bar(name='actual', x=self.fall_semesters, y=self.fall_size),
                                go.Bar(name='enrollments', x=self.fall_semesters, y=self.fall_max_enrollments)])
        return fall_bar_fig
