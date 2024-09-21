import django
import json
from django.apps import apps

if not apps.ready:
    django.setup()

from ..history_mappers.cloud import CloudHistoryMapper


def lambda_handler(event, context):
    for record in event['Records']:
        body = record['body']
        body_dict = json.loads(body)
        message = body_dict["Message"]
        message_dict = json.loads(message)
        message_record = message_dict["Records"][0]
        bucket_name = message_record['s3']['bucket']['name']
        key = message_record['s3']['object']['key']
        print(f"Mapping file {key}")
        try:
            mapper = CloudHistoryMapper(bucket_name)
            mapper.map_history(key)
            return {
                'statusCode': 200,
                'body': f"File {key} processed successfully to the database"
            }
        except Exception as e:
            print(f"Error in lambda_handler: {e}")
            return {
                'statusCode': 500,
                'body': f'Error processing file {key}: {e}'
            }
