import django
from django.apps import apps
from django.conf import settings
if not apps.ready:
    django.setup()
from pkrdatamapper.data_mapper.summary_mappers.local import LocalSummaryMapper

DATA_DIR = settings.DATA_DIR


if __name__ == "__main__":

    mapper = LocalSummaryMapper(data_dir=DATA_DIR)
    mapper.map_new_summaries()
