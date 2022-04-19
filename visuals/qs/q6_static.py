import constants as C
import dataframe_init as D

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import textwrap
from django_plotly_dash import DjangoDash

import pandas as pd
from datetime import datetime

app = DjangoDash('q6_static', external_stylesheets=[dbc.themes.BOOTSTRAP])

legend_labels = ['In middle school or earlier (including summer after graduation)', 'In high school (including summer after graduation)', 'In college', 'I have never been taught programming or computer science in an academic or extracurricular program']
bar_colors = ["rgb(10,54,34)", "rgb(20,108,67)", "rgb(71,159,118)", "rgb(162,207,187)"]
QUESTION_ID = 'Q6'
app.layout = html.Div([
    html.Div([
        html.H1('Explore'),
        html.P('Explore the experiences of Harvard undergraduate students with computer science, as they relate to gender and other aspects of identity.')
    ], style={'width': '30%', 'display': 'none', 'margin-top' : 60, 'margin-left' : 50}),
    html.Div([
        html.H4('Split by'),
        html.Div([
            dcc.Dropdown(
                id='axis',
                options=[{'label': i, 'value': i} for i in C.VIZ_AXES],
                value='Gender',
                clearable=False
            )
        ])
    ], style={'width': '20%', 'display': 'none', 'margin-top' : 20, 'margin-left' : 50}),
    html.Div([
        html.H4('Filter'),
        dbc.Button("Select Filters", color="info", id="open-filter", className="mr-1"),
        dbc.Modal(
            [
                dbc.ModalHeader("Filter Options"),
                dbc.ModalBody("You may only select up to two filters at a time, and you may not filter on the basis of your selected split."),
                html.Div([
                    html.Div([
                        html.P('Gender'),
                        dcc.Dropdown(
                            id='filter-gender-dropdown',
                            options=[{'label': i, 'value': i} for i in C.GENDER_FILTER_OPTIONS],
                            value='All',
                            clearable=False
                        )
                    ],
                    style={'width': '40%', 'display': 'none', 'margin' : 15}),
                    html.Div([
                        html.P('Race/Ethnicity'),
                        dcc.Dropdown(
                            id='filter-race-ethnicity-dropdown',
                            options=[{'label': i, 'value': i} for i in C.RACE_ETHNICITY_FILTER_OPTIONS],
                            value='All',
                            clearable=False
                        )
                    ],
                    style={'width': '40%', 'display': 'none', 'margin' : 15})
                ]),
                html.Div([
                    html.Div([
                        html.P('BGLTQ+'),
                        dcc.Dropdown(
                            id='filter-bgltq-dropdown',
                            options=[{'label': i, 'value': i} for i in C.BGLTQ_FILTER_OPTIONS],
                            value='All',
                            clearable=False
                        )
                    ],
                    style={'width': '40%', 'display': 'none', 'margin' : 15}),
                    html.Div([
                        html.P('First Generation, Low Income (FGLI)'),
                        dcc.Dropdown(
                            id='filter-fgli-dropdown',
                            options=[{'label': i, 'value': i} for i in C.FGLI_FILTER_OPTIONS],
                            value='All',
                            clearable=False
                        )
                    ],
                    style={'width': '40%', 'display': 'none', 'margin' : 15}),
                ]),
                html.Div([
                    html.Div([
                        html.P('Class Year'),
                        dcc.Dropdown(
                            id='filter-class-year-dropdown',
                            options=[{'label': i, 'value': i} for i in C.CLASS_YEAR_FILTER_OPTIONS],
                            value='All',
                            clearable=False
                        )
                    ],
                    style={'width': '40%', 'display': 'none', 'margin' : 15}),
                    html.Div([
                        html.P('School of Primary Concentration'),
                        dcc.Dropdown(
                            id='filter-school-dropdown',
                            options=[{'label': i, 'value': i} for i in C.SCHOOL_FILTER_OPTIONS],
                            value='All',
                            clearable=False
                        )
                    ],
                    style={'width': '40%', 'display': 'none', 'margin' : 15})
                ]),
                html.Div([
                    html.Div([
                        html.P('Primary Concentration'),
                        dcc.Dropdown(
                            id='filter-concentration-dropdown',
                            options=[{'label': i, 'value': i} for i in C.CONCENTRATION_FILTER_OPTIONS],
                            value='All',
                            clearable=False
                        )
                    ],
                    style={'width': '40%', 'display': 'none', 'margin' : 15})
                ]),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close-filter", className="ml-auto")
                ),
            ],
            id="filter-modal",
            size="lg",
        ),
        html.P('Filters: None', id='filters-label', style={'font-style' : 'italic'})
    ], style={'width': '30%', 'display': 'none', 'margin-top' : 20, 'margin-left' : 50}),
    html.Div([
        html.P("If you have been taught programming or computer science through an academic or extracurricular program, when did you enroll in your first course?")
    ], style={'font-family':'Arial', 'color':'rgb(42, 63, 95)','font-size':'14pt','height':'auto', 'margin-left':50}),
    dcc.Graph(id='visualization',
              config={'displayModeBar': False}),
              #style={'margin-top':'-40'}), 
    html.P("With regards to programming background, 62.9% of BGLTQ+ respondents have learned programming before college, while 80.0% of non-BGLTQ+ students have done the same. In addition, 34.8% of non-male students surveyed claim that they have never been taught programming before coming to Harvard, while 0.0% of reported male students fall under that category. Furthermore, 83.3% of surveyed male students have been taught programming in middle school or earlier, compared to 65.2% of non-male students.", style = {'font-size': '14pt'}), 
    html.P("Compared to the results from last year, a lower proportion of students overall reported taking a programming course in middle school or earlier. However, both years’ survey results encapsulate the fact that male students tend to learn programming earlier than their non-male counterparts.", style = {'font-size': '14pt'})
])

def is_sample_size_insufficient(dff, axis):
    # get number of responses per category
    category_counts = dff[axis].value_counts().reset_index(name='counts')['counts'].tolist()
    # check number of responses per category is greater than minimum sample size
    return any(c < C.MIN_SAMPLE_SIZE for c in category_counts)

def calculate_percentages(dff, axis, y_data):
    data = []
    for y_label in y_data:
        filt_dff = dff[dff[axis] == y_label]
        eval_counts = []
        total = 0
        row = []
        for eval_label in legend_labels:
            count = filt_dff[filt_dff[QUESTION_ID] == eval_label].shape[0]
            eval_counts.append(count)
            total += count
        for count in eval_counts:
            value = 0
            if total != 0:
                value = round(count * 100 / total, 2)
            row.append(value)
        data.append(row)
        #print(y_label + ": " + str(total))
    return data

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
    Output('filter-gender-dropdown', 'enabled'),
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

    filter_selections = [gender_filter, race_ethnicity_filter, bgltq_filter, fgli_filter, class_year_filter, school_filter, concentration_filter]
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
    filter_selections = [gender_filter, race_ethnicity_filter, bgltq_filter, fgli_filter, class_year_filter, school_filter, concentration_filter]
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
    dff = filter_df(D.AXIS_DF[axis], gender_filter, race_ethnicity_filter, bgltq_filter,
        fgli_filter, class_year_filter, school_filter, concentration_filter)

    fig = go.Figure()
    y_data = dff[axis].unique()[::-1]
    x_data = calculate_percentages(dff, axis, y_data)

    # return empty plot if there is not enough data (or if figure is not yet implemented)
    if fig == None or is_sample_size_insufficient(dff, axis):
        return C.EMPTY_FIGURE

    for row in range(len(x_data)):
        for col in range(len(x_data[0])):
            leg=(row==0)
            hovertext = str(x_data[row][col]) + '% - ' + legend_labels[col]
            fig.add_trace(go.Bar(
                x=[x_data[row][col]], y=[row],
                orientation='h',
                hoverinfo='text',
                hovertext=hovertext,
                name=legend_labels[col],
                showlegend=leg,
                marker=dict(
                    color=bar_colors[col],
                    line=dict(color='rgb(248, 248, 249)', width=1)
                )
            ))

    fig.update_layout(
        xaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=True,
            zeroline=False,
            domain=[0.15, 1], 
            fixedrange=True,
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
            fixedrange=True,
        ),
        barmode='stack',
        #paper_bgcolor='rgb(248, 248, 255)',
        #plot_bgcolor='rgb(248, 248, 255)',
        margin=dict(l=0, r=0, t=20, b=150),
        showlegend=True,
        legend = dict(orientation='h')
    )

    annotations = []
    for i in range(len(y_data)):
        # labeling the y-axis
        split_label = textwrap.wrap(str(y_data[i]), width=18)
        annotations.append(dict(xref='paper', yref='y',
                                x=0.13, y=i,
                                xanchor='right',
                                text='<br>'.join(split_label),
                                font=dict(family='Arial', size=14,
                                          color='rgb(67, 67, 67)'),
                                showarrow=False, align='right'))

    split_text = textwrap.wrap(D.QUESTION_KEY[QUESTION_ID][0], width=100)
    fig.update_layout(annotations=annotations) #, title_text='<br>'.join(split_text)[:-17]
    

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
