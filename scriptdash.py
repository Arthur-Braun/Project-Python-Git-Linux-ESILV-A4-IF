import os
import dash
from dash import dcc
from dash import html
import datetime
import plotly.express as px
import pandas as pd
import matplotlib

# Get the extracted text from the environment variable
with open('output.txt', 'r') as file:
	text=file.read()

now=datetime.datetime.now()
time=now.strftime("%Y-%m-%d %H:%M:%S")

data_file = 'dataframe.txt'


with open(data_file, 'a') as f:
    f.write(time+';'+text)

# Create the Dash app
app = dash.Dash()


df = pd.read_csv("dataframe.txt", sep=";", header=None, names=["Time", "Rates"])
df['Time']=pd.to_datetime(df['Time'], format="%Y-%m-%d %H:%M:%S")

fig = px.line(df, x="Time", y="Rates")

# Define the layout of the app

app.layout = html.Div([
    html.P("Latest EUR/KRW rate at : " + time + " UTC"),
    html.B(text),
   dcc.Graph(
       id='EUR/KRW',
      figure=fig
    )
])

# Run the app
if __name__ == '__main__':
	app.run_server(host= '0.0.0.0',port=8050, debug=True)

