import json
import requests
from pathlib import Path
import pandas as pd
import sqlalchemy
from datetime import datetime

client_id = 'A8f8B0300v456j7n'
client_secret = 'N35620nff35Ndb05'

# First authorisation with credentials to get access tokens
def first_auth():

    # Use 'client_credentials' grant type to get access token
    exchange_code_url = 'https://data.fixer.io/oauth/token'
    response = requests.post(exchange_code_url, 
                            headers = {
                                'Content-Type': 'application/x-www-form-urlencoded'
                            },
                            data = {
                                'grant_type': 'client_credentials',
                                'client_id' : client_id,
                                'client_secret' : client_secret
                            })
    json_response = response.json()
    
    return [json_response['access_token'], json_response['refresh_token']]

# Getting tokens and storing them in file for use and later freshreshment 
def refresh_token(refresh_token):

    # Use 'refresh_token' grant type to get refresh token
    exchange_code_url = 'https://data.fixer.io/oauth/token'
    response = requests.post(exchange_code_url, 
                            headers = {
                                'Content-Type': 'application/x-www-form-urlencoded'
                            },
                            data = {
                                'grant_type': ' refresh_token',
                                'client_id' : client_id,
                                'client_secret' : client_secret
                            })
    json_response = response.json()
    
    # write refresh token to a file for refreshment in later runs
    new_refresh_token = json_response['refresh_token']
    rt_file = open('C:/path/to/refresh_token.txt', 'w')
    rt_file.write(new_refresh_token)
    rt_file.close()
    
    return [json_response['access_token'], json_response['refresh_token']]

# Calling the API with the refresh token
def call_api():

    # Get a new access token using the old refresh token
    old_refresh_token = open('C:/path/to/refresh_token.txt', 'r').read()
    new_tokens = refresh_token(old_refresh_token)
    
    get_url = 'http://data.fixer.io/api/latest&symbols=BTC,USD,GBP'
    response = requests.get(get_url,
                           headers = {
                               'Authorization': 'Bearer ' + new_tokens[0],
                               'Accept': 'application/json'
                           })
    json_response = response.json()

    return(json_response)

# Transfrom raw response into dataframe to load into DB
def transform():

    # Call extract function to get raw JSON from API
    df = pd.DataFrame(call_api())

    print('transforming response . . .')

    # Add current datetime
    df['datetime'] = datetime.now() 

    # Add the index as its own column 'symbol' and reset the index
    df['symbol'] = df.index
    df.reset_index(level=0, inplace=True,)

    # select the columns required
    df = df[['symbol', 'timestamp', 'rates', 'datetime']]

    # add a description column for labeling currencies along with their symbol
    df['description'] = df.apply (lambda row: label_currency(row), axis=1)

    return(df)

# Function to properly label currency as the free fixer plan doesnt include them
def label_currency (row):
   if row['symbol'] == 'BTC' :
      return 'Bitcoin'
   if row['symbol'] == 'USD':
      return 'United States Dollar'
   if row['symbol']  == 'GBP':
      return 'British Pound Sterling'
 
# Load dataframe into DB 
def load():
    # Connect to postgres database and update table, create it if it doesnt exist for first run

    # Call transfrom to ge the transfromed dataframe for DB update
    dataframe = transform()

    # Connect to DB (Postgres for this example)
    print('Loading dataframes into Database . . .')
    engine = sqlalchemy.create_engine('postgres://postgres:password@consciousgrowth.1234.com:5432/databank')
    conn = engine.connect()

    # Create the table is it doesnt exist and append to it if it exists already, 
    table_name = 'fx_price_index'
    dataframe.to_sql(table_name, conn, if_exists = 'append', index = False)

    conn.close()

def main():
    
    # running the script for the first time to autherise and get tokens
    # if the refresh token file doesnt exist
    my_file = Path("C:/path/to/refresh_token.txt")
    if not my_file.is_file():
        old_tokens = first_auth()
        refresh_token(old_tokens[1])
    
    load()


if __name__ == '__main__':
    main()
