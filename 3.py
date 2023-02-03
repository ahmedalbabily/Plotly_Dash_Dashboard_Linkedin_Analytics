import dash                              
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input
from dash_extensions import Lottie       
import dash_bootstrap_components as dbc  
import plotly.express as px              
import pandas as pd                      
from datetime import date
import calendar
from wordcloud import WordCloud 


# Lottie Icons (Animations)
url_conections = "https://assets9.lottiefiles.com/private_files/lf30_5ttqPi.json"
url_companies = "https://assets9.lottiefiles.com/packages/lf20_EzPrWM.json"
url_msg_in = "https://assets9.lottiefiles.com/packages/lf20_8wREpI.json"
url_msg_out = "https://assets2.lottiefiles.com/packages/lf20_Cc8Bpg.json"
url_reactions = "https://assets2.lottiefiles.com/packages/lf20_nKwET0.json"
options = dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio='xMidYMid slice'))


# Importing the data 
df_cnt = pd.read_csv(r"c:\\Users\\123\\Desktop\\Freelance Job\\Connections.csv")
df_cnt["Connected On"] = pd.to_datetime(df_cnt["Connected On"])
df_cnt["month"] = df_cnt["Connected On"].dt.month
df_cnt['month'] = df_cnt['month'].apply(lambda x: calendar.month_abbr[x])

df_invite = pd.read_csv("c:\\Users\\123\\Desktop\\Freelance Job\\Invitations.csv")
df_invite["Sent At"] = pd.to_datetime(df_invite["Sent At"])

df_react = pd.read_csv(r"c:\\Users\\123\\Desktop\\Freelance Job\\Reactions.csv")
df_react["Date"] = pd.to_datetime(df_react["Date"])

df_msg = pd.read_csv("c:\\Users\\123\\Desktop\\Freelance Job\\messages.csv")
df_msg["DATE"] = pd.to_datetime(df_msg["DATE"])


# Bootstrap Theme for the dashboard, LUX in this case
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])


app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardImg(src='/assets/linkedin-logo2.png') # 150px by 45px
            ],className='mb-2'),
            dbc.Card([
                dbc.CardBody([
                    dbc.CardLink("Visit My Profile",target="_blank",href="https://www.linkedin.com/in/ahmedosamaamin/"
                                 
                    )
                ])
            ]),
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.DatePickerSingle(
                        id='my-date-picker-start',
                        date=date(2021, 1, 1),
                        className='ml-5'
                    ),
                    dcc.DatePickerSingle(
                        id='my-date-picker-end',
                        date=date(2023, 1, 1),
                        className='mb-2 ml-2'
                    ),
                ])
            ], color="info", style={'height':'18vh'}),
        ], width=8),
    ],className='mb-2 mt-2'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="67%", height="67%", url=url_conections)),
                dbc.CardBody([
                    html.H6('Connections'),
                    html.H2(id='content-connections', children="000")
                ], style={'textAlign':'center'})
            ]),
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="32%", height="32%", url=url_companies)),
                dbc.CardBody([
                    html.H6('Companies'),
                    html.H2(id='content-companies', children="000")
                ], style={'textAlign':'center'})
            ]),
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="25%", height="25%", url=url_msg_in)),
                dbc.CardBody([
                    html.H6('Invites received'),
                    html.H2(id='content-msg-in', children="000")
                ], style={'textAlign':'center'})
            ]),
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="53%", height="53%", url=url_msg_out)),
                dbc.CardBody([
                    html.H6('Invites sent'),
                    html.H2(id='content-msg-out', children="000")
                ], style={'textAlign': 'center'})
            ]),
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="25%", height="25%", url=url_reactions)),
                dbc.CardBody([
                    html.H6('Reactions'),
                    html.H2(id='content-reactions', children="000")
                ], style={'textAlign': 'center'})
            ]),
        ], width=2),
    ],className='mb-2'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='line-chart', figure={}, config={'displayModeBar': False}),
                ])
            ]),
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='bar-chart', figure={}, config={'displayModeBar': False}),
                ])
            ]),
        ], width=4),
    ],className='mb-2'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='TBD', figure={}),
                ])
            ]),
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='pie-chart', figure={}, config={'displayModeBar': False}),
                ])
            ]),
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='wordcloud', figure={}, config={'displayModeBar': False}),
                ])
            ]),
        ], width=4),
    ],className='mb-2'),
], fluid=True)


# Updating the 5 number cards ******************************************
@app.callback(
    Output('content-connections','children'),
    Output('content-companies','children'),
    Output('content-msg-in','children'),
    Output('content-msg-out','children'),
    Output('content-reactions','children'),
    Input('my-date-picker-start','date'),
    Input('my-date-picker-end','date'),
)
def update_small_cards(start_date, end_date):
    # Connections
    dff_c = df_cnt.copy()

    dff_c = dff_c[(dff_c['Connected On']>=start_date) & (dff_c['Connected On']<=end_date)]
    conctns_num = len(dff_c)
    compns_num = len(dff_c['Company'].unique())

    # Invitations
    dff_i = df_invite.copy()
    dff_i = dff_i[(dff_i['Sent At']>=start_date) & (dff_i['Sent At']<=end_date)]
    # print(dff_i)
    in_num = len(dff_i[dff_i['Direction']=='INCOMING'])
    out_num = len(dff_i[dff_i['Direction']=='OUTGOING'])

    # Reactions
    dff_r = df_react.copy()
    dff_r = dff_r[(dff_r['Date']>=start_date) & (dff_r['Date']<=end_date)]
    reactns_num = len(dff_r)

    return conctns_num, compns_num, in_num, out_num, reactns_num


# Line Chart ***********************************************************
@app.callback(
    Output('line-chart','figure'),
    Input('my-date-picker-start','date'),
    Input('my-date-picker-end','date'),
)
def update_line(start_date, end_date):
    dff = df_cnt.copy()
    dff = dff[(dff['Connected On']>=start_date) & (dff['Connected On']<=end_date)]
    dff = dff[["month"]].value_counts()
    dff = dff.to_frame()
    dff.reset_index(inplace=True)
    dff.rename(columns={0: 'Total connections'}, inplace=True)

    fig_line = px.line(dff, x='month', y='Total connections', template='ggplot2',
                  title="Total Connections by Month Name")
    fig_line.update_traces(mode="lines+markers", fill='tozeroy',line={'color':'blue'})
    fig_line.update_layout(margin=dict(l=20, r=20, t=30, b=20))

    return fig_line


# Bar Chart ************************************************************
@app.callback(
    Output('bar-chart','figure'),
    Input('my-date-picker-start','date'),
    Input('my-date-picker-end','date'),
)
def update_bar(start_date, end_date):
    dff = df_cnt.copy()
    dff = dff[(dff['Connected On']>=start_date) & (dff['Connected On']<=end_date)]

    dff = dff[["Company"]].value_counts().head(6)
    dff = dff.to_frame()
    dff.reset_index(inplace=True)
    dff.rename(columns={0:'Total connections'}, inplace=True)
    # print(dff_comp)
    fig_bar = px.bar(dff, x='Total connections', y='Company', template='ggplot2',
                      orientation='h', title="Total Connections by Company")
    fig_bar.update_yaxes(tickangle=45)
    fig_bar.update_layout(margin=dict(l=20, r=20, t=30, b=20))
    fig_bar.update_traces(marker_color='blue')

    return fig_bar


# Pie Chart ************************************************************
@app.callback(
    Output('pie-chart','figure'),
    Input('my-date-picker-start','date'),
    Input('my-date-picker-end','date'),
)
def update_pie(start_date, end_date):
    dff = df_msg.copy()
    dff = dff[(dff['DATE']>=start_date) & (dff['DATE']<=end_date)]
    msg_sent = len(dff[dff['FROM']=='Ahmed ElBably'])
    msg_rcvd = len(dff[dff['FROM'] != 'Ahmed ElBably'])
    fig_pie = px.pie(names=['Sent','Received'], values=[msg_sent, msg_rcvd],
                     template='ggplot2', title="Messages Sent & Received"
                     )
    fig_pie.update_layout(margin=dict(l=20, r=20, t=30, b=20))
    fig_pie.update_traces(marker_colors=['red','blue'])

    return fig_pie


# Word Cloud ************************************************************
@app.callback(
    Output('wordcloud','figure'),
    Input('my-date-picker-start','date'),
    Input('my-date-picker-end','date'),
)
def update_pie(start_date, end_date):
    dff = df_cnt.copy()
    dff = dff.Position[(dff['Connected On']>=start_date) & (dff['Connected On']<=end_date)].astype(str)

    my_wordcloud = WordCloud(
        background_color='white',
        height=275
    ).generate(' '.join(dff))

    fig_wordcloud = px.imshow(my_wordcloud, template='ggplot2',
                              title="Total Connections by Position")
    fig_wordcloud.update_layout(margin=dict(l=20, r=20, t=30, b=20))
    fig_wordcloud.update_xaxes(visible=False)
    fig_wordcloud.update_yaxes(visible=False)

    return fig_wordcloud

@app.callback(
Output('TBD', 'figure'),
[Input('my-date-picker-start', 'date'),
Input('my-date-picker-end', 'date')]
)
def update_bar(start_date, end_date):
    dff = df_msg.copy()
    dff = dff[(dff['DATE'] >= start_date) & (dff['DATE'] <= end_date)]
    dff['FROM'] = dff['FROM'].astype('category')
    count = dff.groupby('FROM').count().reset_index()
    count = count.sort_values(by='CONTENT', ascending=False)
    fig_bar = px.bar(count, x='FROM', y='CONTENT', color='CONTENT',
    title='Number of Messages Sent and Received')
    fig_bar.update_layout(margin=dict(l=20, r=20, t=30, b=20))
    fig_bar.update_traces(marker_color='red')
    return fig_bar



if __name__=='__main__':
    app.run_server(debug=False, port=8004)