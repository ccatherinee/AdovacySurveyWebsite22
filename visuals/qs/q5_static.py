# color scheme

import constants as C
import dataframe_init as D

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime
import dash_bootstrap_components as dbc
from django_plotly_dash import DjangoDash

# constants
# column titles with formatting
COLUMN_TITLES = ['', 'My first-year <br> academic advisor <br> <br>', 'Residential advising,<br>such as house <br>tutors or proctors <br> <br>',
                 'Department <br> heads <br> <br>', 'Department <br> faculty <br> <br>', 'Department-specific <br> advising programs <br> <br>', 
                 'Peer <br> Advising <br> Fellows (PAFs) <br> <br>']

# label names used to extract data
ANSWER_OPTIONS = ['My first-year academic advisor', 'Residential advising resources, such as house tutors or proctors',
                  'Department heads',  'Department faculty', 'Department-specific advising programs', 
                  'Peer Advising Fellows (PAFs)']

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = DjangoDash('q5_static', external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = html.Div([

    html.Div([
        html.H1('Explore'),
        html.P('Which of the following on-campus resources have helped you decide your concentration(s)?')
    ], style={'width': '30%', 'display': 'none', 'margin-top': 60, 'margin-left': 50}),
    html.Div([
        html.H4('Split by'),
        html.Div([
            dcc.Dropdown(
                id='axis',
                options=[{'label': i, 'value': i} for i in C.VIZ_AXES],
                value='Class Year',
                clearable=False
            )
        ])
    ], style={'width': '20%', 'display': 'none', 'margin-top': 20, 'margin-left': 50}),
    html.Div([
        html.H4('Filter'),
        dbc.Button("Select Filters", color="info",
                   id="open-filter", className="mr-1"),
        dbc.Modal(
            [
                dbc.ModalHeader("Filter Options"),
                dbc.ModalBody(
                    "You may only select up to two filters at a time, and you may not filter on the basis of your selected split."),
                html.Div([
                    html.Div([
                        html.P('Gender'),
                        dcc.Dropdown(
                            id='filter-gender-dropdown',
                            options=[{'label': i, 'value': i}
                                     for i in C.GENDER_FILTER_OPTIONS],
                            value='All',
                            clearable=False
                        )
                    ],
                        style={'width': '40%', 'display': 'none', 'margin': 15}),
                    html.Div([
                        html.P('Race/Ethnicity'),
                        dcc.Dropdown(
                            id='filter-race-ethnicity-dropdown',
                            options=[{'label': i, 'value': i}
                                     for i in C.RACE_ETHNICITY_FILTER_OPTIONS],
                            value='All',
                            clearable=False
                        )
                    ],
                        style={'width': '40%', 'display': 'none', 'margin': 15})
                ]),
                html.Div([
                    html.Div([
                        html.P('BGLTQ+'),
                        dcc.Dropdown(
                            id='filter-bgltq-dropdown',
                            options=[{'label': i, 'value': i}
                                     for i in C.BGLTQ_FILTER_OPTIONS],
                            value='All',
                            clearable=False
                        )
                    ],
                        style={'width': '40%', 'display': 'none', 'margin': 15}),
                    html.Div([
                        html.P('First Generation, Low Income (FGLI)'),
                        dcc.Dropdown(
                            id='filter-fgli-dropdown',
                            options=[{'label': i, 'value': i}
                                     for i in C.FGLI_FILTER_OPTIONS],
                            value='All',
                            clearable=False
                        )
                    ],
                        style={'width': '40%', 'display': 'none', 'margin': 15}),
                ]),
                html.Div([
                    html.Div([
                        html.P('Class Year'),
                        dcc.Dropdown(
                            id='filter-class-year-dropdown',
                            options=[{'label': i, 'value': i}
                                     for i in C.CLASS_YEAR_FILTER_OPTIONS],
                            value='All',
                            clearable=False
                        )
                    ],
                        style={'width': '40%', 'display': 'none', 'margin': 15}),
                    html.Div([
                        html.P('School of Primary Concentration'),
                        dcc.Dropdown(
                            id='filter-school-dropdown',
                            options=[{'label': i, 'value': i}
                                     for i in C.SCHOOL_FILTER_OPTIONS],
                            value='All',
                            clearable=False
                        )
                    ],
                        style={'width': '40%', 'display': 'none', 'margin': 15})
                ]),
                html.Div([
                    html.Div([
                        html.P('Primary Concentration'),
                        dcc.Dropdown(
                            id='filter-concentration-dropdown',
                            options=[{'label': i, 'value': i}
                                     for i in C.CONCENTRATION_FILTER_OPTIONS],
                            value='All',
                            clearable=False
                        )
                    ],
                        style={'width': '40%', 'display': 'none', 'margin': 15})
                ]),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close-filter", className="ml-auto")
                ),
            ],
            id="filter-modal",
            size="lg",
        ),
        html.P('Filters: None', id='filters-label',
               style={'font-style': 'italic'})
    ], style={'width': '30%', 'display': 'none', 'margin-top': 20, 'margin-left': 50}),  
    html.Div([
        html.P("Which of the following on-campus resources have helped you decide your concentration(s)?")
    ], style={'font-family':'Arial', 'color':'rgb(42, 63, 95)','font-size':'14pt','height':'auto', 'margin-left':50}),
    dcc.Graph(id='visualization', config={'displayModeBar':False}), 
    html.P("Generally, upperclassmen have found more use/value from their advisors, proctors, department heads, faculty members, and advising programs. 72.2% of freshmen get their primary concentration-related help from their first-year academic advisors, the most out of all four years.", style = {'font-size': '14pt'})
])


def is_sample_size_insufficient(dff, axis):
    # get number of responses per category
    category_counts = dff[axis].value_counts().reset_index(name='counts')[
        'counts'].tolist()
    # check number of responses per category is greater than minimum sample size
    return any(c < C.MIN_SAMPLE_SIZE for c in category_counts)


@app.callback(
    Output('filter-modal', 'is_open'),
    Input('open-filter', 'n_clicks'),
    Input('close-filter', 'n_clicks'),
    State('filter-modal', 'is_open'))
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    Output('filter-gender-dropdown', 'disabled'),
    Output('filter-race-ethnicity-dropdown', 'disabled'),
    Output('filter-bgltq-dropdown', 'disabled'),
    Output('filter-fgli-dropdown', 'disabled'),
    Output('filter-class-year-dropdown', 'disabled'),
    Output('filter-school-dropdown', 'disabled'),
    Output('filter-concentration-dropdown', 'disabled'),
    Input('axis', 'value'),
    Input('filter-gender-dropdown', 'value'),
    Input('filter-race-ethnicity-dropdown', 'value'),
    Input('filter-bgltq-dropdown', 'value'),
    Input('filter-fgli-dropdown', 'value'),
    Input('filter-class-year-dropdown', 'value'),
    Input('filter-school-dropdown', 'value'),
    Input('filter-concentration-dropdown', 'value'))
def toggle_filters(axis, gender_filter, race_ethnicity_filter, bgltq_filter, fgli_filter,
                   class_year_filter, school_filter, concentration_filter):
    filter_count = 0
    filter_enable_list = [False, False, False, False, False, False, False]
    filter_enable_list[C.VIZ_AXES.index(axis)] = True
    filter_disable_list = filter_enable_list.copy()

    filter_selections = [gender_filter, race_ethnicity_filter, bgltq_filter,
                         fgli_filter, class_year_filter, school_filter, concentration_filter]
    for i in range(len(filter_selections)):
        if filter_selections[i] == 'All':
            filter_disable_list[i] = (True)
        else:
            filter_count += 1

    if filter_count >= 2:
        return filter_disable_list
    return filter_enable_list


@app.callback(
    Output('filter-gender-dropdown', 'value'),
    Output('filter-race-ethnicity-dropdown', 'value'),
    Output('filter-bgltq-dropdown', 'value'),
    Output('filter-fgli-dropdown', 'value'),
    Output('filter-class-year-dropdown', 'value'),
    Output('filter-school-dropdown', 'value'),
    Output('filter-concentration-dropdown', 'value'),
    Input('axis', 'value'))
def reset_filters(axis):
    return ['All', 'All', 'All', 'All', 'All', 'All', 'All']


@app.callback(
    Output('filters-label', 'children'),
    Input('filter-gender-dropdown', 'value'),
    Input('filter-race-ethnicity-dropdown', 'value'),
    Input('filter-bgltq-dropdown', 'value'),
    Input('filter-fgli-dropdown', 'value'),
    Input('filter-class-year-dropdown', 'value'),
    Input('filter-school-dropdown', 'value'),
    Input('filter-concentration-dropdown', 'value'))
def set_filters_label(gender_filter, race_ethnicity_filter, bgltq_filter, fgli_filter,
                      class_year_filter, school_filter, concentration_filter):
    filter_str_list = []
    filter_selections = [gender_filter, race_ethnicity_filter, bgltq_filter,
                         fgli_filter, class_year_filter, school_filter, concentration_filter]
    for sel in filter_selections:
        if sel != 'All':
            filter_str_list.append(sel)

    if len(filter_str_list) == 0:
        return 'Filters: None'
    return 'Filters: ' + ', '.join(filter_str_list)


def filter_df(df, gender_filter, race_ethnicity_filter, bgltq_filter, fgli_filter,
              class_year_filter, school_filter, concentration_filter):
    df = D.filter_gender(df, gender_filter)
    df = D.filter_race_ethnicity(df, race_ethnicity_filter)
    df = D.filter_bgltq(df, bgltq_filter)
    df = D.filter_fgli(df, fgli_filter)
    df = D.filter_class_year(df, class_year_filter)
    df = D.filter_school(df, school_filter)
    df = D.filter_conc(df, concentration_filter)
    return df


@app.callback(
    Output('visualization', 'figure'),
    Input('axis', 'value'),
    Input('filter-gender-dropdown', 'value'),
    Input('filter-race-ethnicity-dropdown', 'value'),
    Input('filter-bgltq-dropdown', 'value'),
    Input('filter-fgli-dropdown', 'value'),
    Input('filter-class-year-dropdown', 'value'),
    Input('filter-school-dropdown', 'value'),
    Input('filter-concentration-dropdown', 'value'))
def update_graph(axis, gender_filter, race_ethnicity_filter, bgltq_filter, fgli_filter,
                 class_year_filter, school_filter, concentration_filter):

    # extract relevant data
    dff = filter_df(D.AXIS_DF[axis], gender_filter, race_ethnicity_filter, bgltq_filter,
                    fgli_filter, class_year_filter, school_filter, concentration_filter)
    columnOptions = []
    for choice in ANSWER_OPTIONS:
        columnOptions.append(dff[dff['Q5'].str.contains(
            choice, na=False)])
            
    # names is used for labelling
    names = list(dff[axis].unique())

    # initialize subplot
    generateSpecs = [[{"type": "pie"}
                      for _ in range(len(columnOptions)+1)] for _ in names]
    figSub = make_subplots(rows=len(names), cols=len(
        columnOptions)+1, specs=generateSpecs, column_titles=COLUMN_TITLES)
    rowNum = 1

    for label in names:
        colNum = 1
        # add row title
        figSub.add_trace(go.Table(
            header=dict(values=[label], fill_color='rgba(0,0,0,0)', font=dict(
                color='RebeccaPurple', size=12), align='center'),
            cells=dict(values=[' '],
                       fill_color='rgba(0,0,0,0)',
                       align='center')
        ),
            row=rowNum, col=colNum)
        colNum += 1

        # construct pie chart
        for colOption in columnOptions:

            votes = [0, 0]
            for x in colOption[axis]:
                if x == label:
                    votes[0] += 1

            total = dff[dff[axis] == label]['Q5'].count()

            votes[1] = total - votes[0]
            figSub.add_trace(go.Pie(
                labels=['Yes', 'No'],
                values=votes,
                textinfo='none',
                hoverinfo='label+percent',
                marker={'colors': ['rgb(71,159,118)','rgb(233,236,239)']},
                showlegend = False),
                row=rowNum, col=colNum)

            colNum += 1
        rowNum+=1
        #print(total)
    figSub.update_annotations(font_size=10)

    figSub.update_layout(
        margin=dict(l=0, r=0, t=40, b=40),
    )
    # figSub.update_layout(
        # title='Which of the following on-campus resources have helped you decide your concentration(s)?'
    # )
    # check for errors
    if figSub == None or is_sample_size_insufficient(dff, axis):
        print("ERROR")
        return C.EMPTY_FIGURE
    return figSub


if __name__ == '__main__':
    app.run_server(debug=True)
