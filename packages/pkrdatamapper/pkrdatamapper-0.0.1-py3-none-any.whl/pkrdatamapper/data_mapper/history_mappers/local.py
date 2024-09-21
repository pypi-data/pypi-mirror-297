from pkrcomponents.converters.history_converter.local import LocalHandHistoryConverter

from pkrdatamapper.data_mapper.history_mappers.abstract import AbstractHistoryMapper


class LocalHistoryMapper(AbstractHistoryMapper):
    def __init__(self, data_dir):
        self.converter = LocalHandHistoryConverter(data_dir=data_dir)
