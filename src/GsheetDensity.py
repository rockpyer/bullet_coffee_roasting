import os
from dotenv import load_dotenv
import pygsheets
import pandas as pd
import requests
from io import StringIO

# Load environment variables from .env file
# private .env file is not included in the repository, has all the info about my gsheet
load_dotenv()

def getDensityGSheetPublic():

    # Your Google Sheet's URL
    sheet_url = os.getenv('GSHEET_PUBLIC_URL')
    # Remember that if you are using just a shared link you have to,
    # Convert the URL to the CSV export format
    csv_url = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')

    response = requests.get(sheet_url, verify=False)

    # Check if the request was successful
    if response.status_code == 200:
        # Use StringIO to read the content of the response into a pandas DataFrame
        df = pd.read_csv(StringIO(response.text))
        return df
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")
