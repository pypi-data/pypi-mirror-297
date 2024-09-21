import django
from django.apps import apps
from django.conf import settings
if not apps.ready:
    django.setup()

from pkrdatamapper.data_mapper.history_mappers.local import LocalHistoryMapper

DATA_DIR = settings.DATA_DIR


if __name__ == "__main__":
    mapper = LocalHistoryMapper(data_dir=DATA_DIR)
    mapper.map_new_histories()
