import logging
import os
import json
import azure.functions as func
from azure.cosmosdb.table.tableservice import TableService


def main(req: func.HttpRequest) -> func.HttpResponse:
    req_keys = req.form.keys()
    token_field_name = "token"

    if token_field_name not in req_keys:
        msg = f'Missing "{token_field_name}" in body'
        logging.error(msg)
        return func.HttpResponse(msg, status_code=400)


    try:       
        connect_str=os.environ["AzureWebJobsStorage"] 
        table_service = TableService(connection_string=connect_str)
        token = req.form.get(token_field_name)
        ocr_results = table_service.query_entities('Tasks', filter=f"token eq '{token}'")
        

        if (len(ocr_results.items) == 0):
            msg = f'Token {token} is incorrect'
            logging.error(msg)
            return func.HttpResponse(msg, status_code=400) 
        
        for item in ocr_results.items:
            del item["Timestamp"]
            del item["etag"]

        return func.HttpResponse(
            json.dumps(ocr_results.items),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        msg = 'Error has occured'
        logging.error(msg)
        return func.HttpResponse(msg, status_code=500)
