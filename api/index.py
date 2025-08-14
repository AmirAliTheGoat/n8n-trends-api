# This is the main script for our serverless function
# It will be in a file named: api/index.py

from fastapi import FastAPI, Query
from pytrends.request import TrendReq
import pandas as pd
from typing import List

# Create the FastAPI app
app = FastAPI()

# Define the API endpoint
@app.get("/api/get_trends")
def get_trends_data(keywords: List[str] = Query(None)):
    if not keywords:
        return {"error": "Please provide at least one keyword."}

    pytrends = TrendReq(hl='en-US', tz=360)

    # Build the payload to get data for the last 30 days
    pytrends.build_payload(kw_list=keywords, cat=0, timeframe='today 1-m', geo='', gprop='')

    # Get the interest over time data
    df = pytrends.interest_over_time()

    # If the dataframe is empty (e.g., no data for keywords), return an error
    if df.empty:
        return {"error": "Could not retrieve data for the given keywords."}

    # Reset the index to make 'date' a column
    df = df.reset_index()

    # Keep only the date and keyword columns, drop the 'isPartial' column
    if 'isPartial' in df.columns:
        df = df.drop(columns=['isPartial'])

    # Convert the date to a simpler string format 'YYYY-MM-DD'
    df['date'] = df['date'].dt.strftime('%Y-%m-%d')

    # Convert the dataframe to a JSON format that's easy for n8n to use
    # and return it
    return df.to_dict(orient='records')
