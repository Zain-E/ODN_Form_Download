
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash
import pandas as pd #For some reason version 1.1.5 worked.  If you cannot deploy ensure that you copy and paste the requirements.txt file from this app!  As it seems to work.
from dash.dependencies import Input, Output
from dash_extensions import Download
from dash_extensions.snippets import send_data_frame
import psycopg2
from sqlalchemy import create_engine
import dash_auth

#================================== AMAZON RDS CONNECTION ==============================================================

#Amazon RDS database connection details
username = 'zaineisa'
password = 'Mastersword4!'
port = '5432'
host = 'postgres-aws-database.cldk6shvy1yf.eu-west-2.rds.amazonaws.com'
database = 'postgres'

#SQL Alchemy connection
sql_alchemy_engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}')

#Connect to DB
conn = psycopg2.connect(
    database=database,
    user=username,
    password=password,
    host=host,
    port=port
)


VALID_USERNAME_PASSWORD_PAIRS = {
     'BenParker': 'ODNform444'
}

#=========================================== LAYOUT ====================================================================

app = dash.Dash(__name__, external_stylesheets=['https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/lux/bootstrap.min.css'],prevent_initial_callbacks=True)
server = app.server
auth = dash_auth.BasicAuth(
   app,
   VALID_USERNAME_PASSWORD_PAIRS
)

app.layout = html.Div([
                                #html.Img inside html.A means you can use the image as a hyperlink to whatever website is needed.
                        dbc.Row([dbc.Col(width=2),
                                 dbc.Col(html.H1('ODN FORM DOWNLOAD',className='dark'),style={'text-align': 'center','vertical-align':'middle'},width=8),
                                 dbc.Col(width=2)]),

                        html.Hr(),

                        html.Br(),

                        dbc.Row(dbc.Col(html.H4('Each Button will allow you to save the full dataset '),style={'text-align': 'center','vertical-align':'middle'}, width =12)),

                        html.Hr(),

                        html.Br(),

                        dbc.Col(html.Div([dbc.Button("Download paediatric surgery data as CSV",
                                                     style={'backgroundColor': 'rgb(235, 104, 100)', 'color': 'white'}, id="Download Paeds Data"),
                                          Download(id="download_paed")]), style={'text-align': 'center', 'vertical-align': 'center'}, width=12),
                        html.Hr(),

                        html.Br(),

                        dbc.Col(html.Div([dbc.Button("Download Cardiology data as CSV",
                                                     style={'backgroundColor': 'rgb(255,153,0)', 'color': 'white'}, id="Download Cardiac Data"),
                                          Download(id="download_card")]), style={'text-align': 'center', 'vertical-align': 'center'}, width=12),

])

#======================================== CALL BACK DOWNLOAD - PAEDS ===================================================

#Callback for the download button
@app.callback(
    Output("download_paed", "data"),
    [Input("Download Paeds Data", "n_clicks")],
)

def generate_csv(n):

    if n > 0:
        # Open a cursor to perform actions on the DB - remember, must close at the end of the query if it makes any changes!
        cur = conn.cursor()
        # conn.commit()

        # Execute a Query

        cur.execute('SELECT * FROM public."Paediatric_Surgery";')
        SQL_Query = cur.fetchall()
        #print(SQL_Query)

        # Extract the column names
        col_names = []
        for elt in cur.description:
            col_names.append(elt[0])

        # Create the dataframe, passing in the list of col_names extracted from the description
        df_RDS = pd.DataFrame(SQL_Query, columns=col_names)

    return send_data_frame(df_RDS.to_csv, filename="PAEDS_Data.csv", index=False)

#=========================================== CALL BACK DOWNLOAD - CARD =================================================

# Callback for the download button
@app.callback(
    Output("download_card", "data"),
    [Input("Download Cardiac Data", "n_clicks")],
)
def generate_csv(n):
    if n > 0:
        # Open a cursor to perform actions on the DB - remember, must close at the end of the query if it makes any changes!
        cur = conn.cursor()
        # conn.commit()

        # Execute a Query

        cur.execute('SELECT * FROM public."Cardiology";')
        SQL_Query = cur.fetchall()
        # print(SQL_Query)

        # Extract the column names
        col_names = []
        for elt in cur.description:
            col_names.append(elt[0])

        # Create the dataframe, passing in the list of col_names extracted from the description
        df_RDS_c = pd.DataFrame(SQL_Query, columns=col_names)

    return send_data_frame(df_RDS_c.to_csv, filename="CARDIO_Data.csv", index=False)

#============================================== RUN ====================================================================
if __name__ == "__main__":
    app.run_server(debug=True)
