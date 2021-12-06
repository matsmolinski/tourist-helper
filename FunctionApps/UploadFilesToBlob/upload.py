import json

from UploadFilesToBlob.common import create_message
from UploadFilesToBlob.validation import validate_request

import logging
import os
import uuid
import azure.functions as func
from azure.storage.blob import BlobServiceClient
from azure.cosmosdb.table.tableservice import TableService

__logger = logging.getLogger('upload')

FILES_PROCESSING = "Files added for processing"
INTERNAL_ERROR = "Internal server error has occurred"


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Received post image request')

    validation_reports = validate_request(req)
    if len(validation_reports) > 0:
        return func.HttpResponse(
            json.dumps(validation_reports),
            mimetype="application/json",
            status_code=400
        )

    language = __resolve_language(req.form)
    email = req.form.get('email')

    try:
        db_connection_str, container_name, table_service, blob_service = __get_connection_parameters()

        for user_file in req.files.values():
            logging.info('Adding file to db...')
            extension = user_file.filename.split('.')[1]
            file_uuid = str(uuid.uuid4())
            generated_filename = '{}.{}'.format(file_uuid, extension)
            token = __resolve_token(req.form)
            blob_client = blob_service.get_blob_client(container=container_name, blob=generated_filename)
            blob_client.upload_blob(user_file)
            task = {'PartitionKey': extension, 'RowKey': file_uuid, 'email': email,
                    'language': language, 'translation': '', 'image_text': '', 'data_analysis': '',
                    'token': token}
            table_service.insert_entity('Tasks', task)
            logging.info('Added file: {}'.format(file_uuid))

        logging.info(FILES_PROCESSING)
        return func.HttpResponse(
            json.dumps(FILES_PROCESSING),
            mimetype="application/json",
            status_code=201
        )
    except Exception:
        logging.error(INTERNAL_ERROR)
        return func.HttpResponse(
            json.dumps(INTERNAL_ERROR),
            mimetype="application/json",
            status_code=500
        )


def __get_connection_parameters():
    db_connection_str = os.environ['AzureWebJobsStorage']
    return db_connection_str, os.environ['ContainerName'], TableService(
        connection_string=db_connection_str), BlobServiceClient.from_connection_string(db_connection_str)


def __resolve_language(request_data: dict):
    language = request_data.get('language', '')
    logging.info(f'User requested translation to language: {language}')
    return language

def __resolve_token(request_data: dict):
    # user send token or generate new for anonymous user
    token = request_data.get('token', str(uuid.uuid4()))
    return token
