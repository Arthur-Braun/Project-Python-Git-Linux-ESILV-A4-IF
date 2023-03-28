import os
import dash
from dash import dash_table
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import datetime
import plotly.express as px
import pandas as pd
import matplotlib



#Extraire la data actualisée scrapée par le script bash

with open('output.txt', 'r') as file:
	text=file.read()

#Extraire la date et l'heure du scrapping

now=datetime.datetime.now()
time=now.strftime("%Y-%m-%d %H:%M:%S")

#Le fichier dans lequel on stocke toutes les données
data_file = 'timeseries.txt'


#Inscription des données dans le fichier
with open(data_file, 'a') as f:
    f.write(time+';'+text)

#Récupération des données depuis le fichier pour créer un dataframe
def load_data(file_path):
    df = pd.read_csv(file_path, sep=';', header=None)
    df.columns = ['Time', 'EUR/KRW']
    df['Time'] = pd.to_datetime(df['Time'])
    return df

#Calcul des données du daily report et mise en forme
def daily_report(df):
    today=df['EUR/KRW'].tail(288)
    low=today.min()
    high=today.max()
    mean=sum(today)/len(today)
    variance=sum((mean-x) for x in today)/len(today)
    volatility=(variance**(1/2))*100
    ret=((today[len(today)-1]/today[0])-1)*100
    return ("Daily low : " + str(round(low,2)) + ' | ' +  "Daily high : " + str(round(high,2))  + ' | ' +  "Daily mean : " + str(round(mean,2))  + ' | ' + "Daily volatility : " + str(round(volatility,2))  + ' % | ' + "Daily return : " + str(round(ret,2)) + ' %')

#Création du dashboard
def create_app():
    app = dash.Dash(__name__)
    app.layout = html.Div([
        dcc.Graph(id='timeseries-plot'),
        dcc.Interval(id='interval-component', interval=5*60*1000, n_intervals=0),
	html.H2('Daily Report, last updated at 20:00 (Paris Time) : '),
        html.Div(id='daily-report'),
        dcc.Interval(id='daily-report-update', interval=60*1000, n_intervals=0)
])

    @app.callback(Output('timeseries-plot', 'figure'), Input('interval-component', 'n_intervals'))
    def update_timeseries(n):
                df = load_data('timeseries.txt')
                fig = px.line(df, x='Time', y='EUR/KRW', title='EUR/KRW rate')
                return fig

    @app.callback(Output('daily-report', 'children'), Input('daily-report-update', 'n_intervals'))
    def update_daily_report(n):                            #le daily report est généré à partir d'une sauvegarde (dailysave.txt)
                df = load_data('dailysave.txt')            #la sauvegarde est écrasée tous les jours à 18h UTC via le crontab (20h heure de Paris)
                return daily_report(df)


    return app



#Lancement de l'app

if __name__ == '__main__':
	app=create_app()
	app.run_server(host= '0.0.0.0', debug=True)
