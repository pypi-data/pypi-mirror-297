from pkrcomponents.converters.summary_converter.cloud import CloudSummaryConverter

from pkrdatamapper.data_mapper.summary_mappers.abstract import AbstractSummaryMapper


class CloudSummaryMapper(AbstractSummaryMapper):
    def __init__(self, bucket_name: str):
        self.converter = CloudSummaryConverter(bucket_name=bucket_name)
