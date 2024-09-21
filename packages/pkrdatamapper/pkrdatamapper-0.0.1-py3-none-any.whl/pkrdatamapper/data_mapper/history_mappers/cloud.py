from pkrcomponents.converters.history_converter.cloud import CloudHandHistoryConverter

from pkrdatamapper.data_mapper.history_mappers.abstract import AbstractHistoryMapper


class CloudHistoryMapper(AbstractHistoryMapper):
    def __init__(self, bucket_name: str):
        self.converter = CloudHandHistoryConverter(bucket_name=bucket_name)