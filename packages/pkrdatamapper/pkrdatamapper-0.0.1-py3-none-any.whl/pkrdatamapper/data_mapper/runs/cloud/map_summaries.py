import django
from django.apps import apps
from django.conf import settings
if not apps.ready:
    django.setup()
from pkrdatamapper.data_mapper.summary_mappers.cloud import CloudSummaryMapper

BUCKET_NAME = settings.BUCKET_NAME

if __name__ == "__main__":

    mapper = CloudSummaryMapper(bucket_name=BUCKET_NAME)
    mapper.map_summaries()
