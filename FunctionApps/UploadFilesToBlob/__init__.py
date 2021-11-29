import logging
import os
import uuid
import re
import azure.functions as func
from azure.storage.blob import BlobServiceClient
from azure.cosmosdb.table.tableservice import TableService


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Received post image request')

    files_number = len(req.files.to_dict().items())

    if files_number == 0:
        msg = 'Missing file in for-data body'
        logging.error(msg)
        return func.HttpResponse(msg, status_code = 400)

    req_keys = req.form.keys()

    if 'email' not in req_keys:
        msg = 'Missing "email" in body'
        logging.error(msg)
        return func.HttpResponse(msg, status_code = 400)
    
    email = req.form.get('email')
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        msg = 'Invalid email'
        logging.error(msg)
        return func.HttpResponse(msg, status_code = 422)

    language = ''
    if 'language' in req_keys:
        language = req.form.get('language')
        logging.info('User requested translation to language: {}'.format(language))

    try:
        db_connection_str = os.environ['AzureWebJobsStorage']
        container_name = os.environ['ContainerName']
        table_service = TableService(connection_string = db_connection_str)
        blob_service = BlobServiceClient.from_connection_string(db_connection_str)

        for user_file in req.files.values():
            logging.info('Adding file to db...')
            extension = user_file.filename.split('.')[1]
            file_uuid = str(uuid.uuid5())
            generated_filename = '{}.{}'.format(file_uuid, extension)

            blob_client = blob_service.get_blob_client(container = container_name, blob = generated_filename)
            blob_client.upload_blob(user_file)

            task = {'PartitionKey': extension, 'RowKey': file_uuid, 'email': email,
                    'language': language, 'translation': '', 'image_text': '', 'data_analysis': ''}
            table_service.insert_entity('Tasks', task)
            logging.info('Added file: {}'.format(file_uuid))

        msg = 'All files added for processing'
        logging.info(msg)
        return func.HttpResponse(msg, status_code = 201)

    except Exception:
        msg = 'Internal server error'
        logging.error(msg)
        return func.HttpResponse(msg, status_code= 500)
