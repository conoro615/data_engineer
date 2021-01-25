from requests.auth import HTTPBasicAuth
from datetime import datetime
import requests
import json
import pandas as pd
import sqlalchemy
import time

# Extract data from API
def extract():

    # URL and headers for API
    fixerurl = 'http://data.fixer.io/api/latest?access_key=9d477103b00cd919a49251802b0acc2e&symbols=BTC,USD,GBP'
    headers = {'User-Agent': 'XY', 'Content-type': 'application/json'}

    # Send GET request to API
    print('Connecting to API . . .')
    fixerRequest = requests.get(fixerurl, headers = headers)
    # Output status code 
    print('Connected to API with code ' + str(fixerRequest.status_code))

    # Get the raw response
    j = fixerRequest.json()

    # Return raw json response
    return(j)


# Transfrom raw response into dataframe to load into DB
def transform():

    # Call extract function to get raw JSON from API
    df = pd.DataFrame(extract())

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
    # Connect to postrges database and update table, create it if it doesnt exist for first run

    # Call transfrom to ge the transfromed dataframe for DB update
    dataframe = transform()

    # Connect to DB (Postgres DB for this example)
    print('Loading dataframes into Database . . .')
    engine = sqlalchemy.create_engine('postgres://postgres:password@consciousgrowth.1234.com:5432/databank')
    conn = engine.connect()

    # Create the table is it doesnt exist and append to it if it exists already, 
    table_name = 'fx_price_index'
    dataframe.to_sql(table_name, conn, if_exists = 'append', index = False)

    conn.close()

def main():
    
    # Create a simple timer to moniter how long the process takes
    print("Starting Process . . .")
    start = time.time() 

    # Call Load function to get the process started
    load()

    end = time.time()
    elapsed = end - start
 
    print('Process Completed in ' + str(elapsed) + ' seconds!')


if __name__ == '__main__':
    main()
