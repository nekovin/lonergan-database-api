import azure.functions as func
import datetime
import json
import logging

app = func.FunctionApp()

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
    
    #CONNECTION_STRING = 

    # match id, fetch number

    # call cati api with number and project number and remove it
    