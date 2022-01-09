import os, requests, uuid, json, time, logging
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials
import azure.functions as func
from datetime import datetime, timedelta
from azure.storage.blob import ResourceTypes, AccountSasPermissions, generate_account_sas
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity


def main(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")
    
    vision_key = os.environ["CognitiveServicesVisionKey"]
    vision_endpoint = os.environ["CognitiveServicesVisionEndpoint"]
    sentiment_key = os.environ["CognitiveServicesSentimentKey"]
    sentiment_enpoint = os.environ["CognitiveServicesSentimentEndpoint"]
    translation_key = os.environ["CognitiveServicesTranslationKey"]
    translation_endpoint = os.environ["CognitiveServicesTranslationEndpoint"]
    translation_loc = "westeurope"
    connect_str = os.environ["AzureWebJobsStorage"]

    rowkey = myblob.name.split('.')[0].split('/')[1]
    partkey = myblob.name.split('.')[1]
      
    table_service = TableService(connection_string=connect_str)
    logging.info(f"row: {rowkey}\n"
                f"part: {partkey}\n")
    task = table_service.get_entity('Tasks', partkey, rowkey)
    del task['etag']
    logging.info(task)
    language = task.language

    #Computer vision
    computervision_client = ComputerVisionClient(vision_endpoint, CognitiveServicesCredentials(vision_key))

    read_results = computervision_client.recognize_printed_text(myblob.uri)
    text = ""
    for region in read_results.regions:       
        for line in region.lines:
            for word in line.words:
                text = text + word.text + '\n'

    
    #Sentiment
    textdoc = [text]
    text_sentiment = ""
    sen_credential = AzureKeyCredential(sentiment_key)
    text_analytics_client = TextAnalyticsClient(endpoint=sentiment_enpoint, credential=sen_credential)
    response = text_analytics_client.analyze_sentiment(documents = textdoc)[0]
    text_sentiment = text_sentiment + "Document Sentiment: {}".format(response.sentiment)
    text_sentiment = text_sentiment +"Overall scores: positive={0:.2f}; neutral={1:.2f}; negative={2:.2f} \n".format(
        response.confidence_scores.positive,
        response.confidence_scores.neutral,
        response.confidence_scores.negative,
    )
    for idx, sentence in enumerate(response.sentences):
        text_sentiment = text_sentiment +"Sentence: {}".format(sentence.text)
        text_sentiment = text_sentiment +"Sentence {} sentiment: {}".format(idx+1, sentence.sentiment)
        text_sentiment = text_sentiment +"Sentence score:\nPositive={0:.2f}\nNeutral={1:.2f}\nNegative={2:.2f}\n".format(
                sentence.confidence_scores.positive,
                sentence.confidence_scores.neutral,
                sentence.confidence_scores.negative,
            )

    #translation
    if language is None or len(language)<2:
        translation = ''
    else:
        path = '/translate?api-version=3.0'
        params = '&to={}'.format(language)
        constructed_url = translation_endpoint + path + params
        headers = {
            'Ocp-Apim-Subscription-Key': translation_key,
            'Ocp-Apim-Subscription-Region': translation_loc,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }
        body = [{
            'text' : text
        }]
        request = requests.post(constructed_url, headers=headers, json=body)
        response = request.json()
        #print(json.dumps(response, sort_keys=True, indent=4, separators=(',', ': ')))
        response = json.dumps(response)
        response = response.split("text")
        response = response[1]
        size = len(response)
        response = response[4:size-5]
        response = response.split(", \"to\":")
        size = len(response)
        translate_lang=response[size-1]
        response.pop()
        translate_text = ""
        for elem in response:
            translate_text = translate_text + elem
        translate_lang = translate_lang.replace("\"","")
        translate_lang = translate_lang.strip()
        translation = "Language: {}, Text: {}".format(translate_lang, translate_text)

    task['translation'] = translation
    task['image_text'] = text
    task['data_analysis'] = text_sentiment
    table_service.update_entity('Tasks', task)
    logging.info('Table storage updated')

    url = os.environ["EmailURL"]
    results_url = os.environ["GetOcrResultURL"]
    results_url = results_url + str(task.token)
    content = {
        'email': task.email,
        'url': results_url
    }
    x = requests.post(url, json=content)
