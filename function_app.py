import azure.functions as func
import datetime
import json
import logging
import psycopg2
import requests
import pandas as pd
import io
import os
from dotenv import load_dotenv

app = func.FunctionApp()

load_dotenv()

alchemer_endpoint=os.getenv("ALCHEMER_ENDPOINT")
db_host=os.getenv("DB_HOST")
dbname=os.getenv("DB_NAME")
user=os.getenv("DB_USER")
pw=os.getenv("DB_PW")
port=os.getenv("DB_PORT")
sslmode=os.getenv("DB_SSLMODE")

@app.route(route="http_endpoint", auth_level=func.AuthLevel.FUNCTION)
def http_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
        
def get_alchemer_data() -> pd.DataFrame:


    url = alchemer_endpoint

    res = requests.get(url)
    
    if res.status_code is not 200:
        res.raise_for_status() 

    byte_data = io.BytesIO(res.content)

    df = pd.read_csv(byte_data)
    
    return df[df['URL Variable: sguid'].notnull()]


def get_postgres_data():
    conn = psycopg2.connect(
        host=db_host,
        dbname=dbname,
        user=user,
        password=pw,
        port=port,
        sslmode=sslmode,
    )

    with conn.cursor() as cur:
        cur.execute("SELECT uuid, phone FROM public.tracking")
        res = cur.fetchall() # returns a list of tuples
        
    conn.close()
    
    return res

@app.route(route="remove_number_from_cati", auth_level=func.AuthLevel.FUNCTION)
def remove_number_from_cati(req: func.HttpRequest) -> func.HttpResponse:
    
    logging.info('Python HTTP trigger function processed a request to remove number from cati.')
    
    # requires api key
    api_key = req.headers.get('X-API-Key')
    if not api_key:
        raise ValueError("Missing API key")
    
    # takes in id and database id
    
    respondent_id = req.params.get('respondent_id')
    
    if not respondent_id:
        raise ValueError("Missing respondent_id parameter")

    database_id = req.params.get('database_id')
    
    if not database_id:
        raise ValueError("Missing database_id parameter")
    
    # fetch postgres row

    # match id, fetch number

    # call cati api with number and project number and remove it