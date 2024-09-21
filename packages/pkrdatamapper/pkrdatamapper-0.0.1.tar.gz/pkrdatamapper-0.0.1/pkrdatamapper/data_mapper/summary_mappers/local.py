from pkrcomponents.converters.summary_converter.local import LocalSummaryConverter

from pkrdatamapper.data_mapper.summary_mappers.abstract import AbstractSummaryMapper


class LocalSummaryMapper(AbstractSummaryMapper):

    def __init__(self, data_dir: str):
        self.converter = LocalSummaryConverter(data_dir=data_dir)