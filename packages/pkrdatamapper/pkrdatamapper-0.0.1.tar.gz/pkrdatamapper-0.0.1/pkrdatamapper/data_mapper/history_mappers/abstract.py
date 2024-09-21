from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

from pkrcomponents.converters.utils.exceptions import HandConversionError
from pkrcomponents.converters.history_converter.abstract import AbstractHandHistoryConverter

from pkrdatamapper.histories.hand_history.models import DBHandHistory
from pkrdatamapper.histories.player_hand_stats.models import DBPlayerHandStats
from pkrdatamapper.players.player_stats.models import DBPlayerStats


class AbstractHistoryMapper(ABC):
    converter: AbstractHandHistoryConverter

    def map_history(self, history_key: str) -> None:
        try:
            table = self.converter.convert_history(history_key)
            DBHandHistory.from_table(table)
            for table_player in table.players:
                db_player_hand_stats = DBPlayerHandStats.from_table_player(table_player)
                db_player_hand_stats.save()
        except HandConversionError as e:
            print(f"Error converting hand {history_key}: {e}")
            self.converter.send_to_corrections(history_key)
        except Exception as e:
            print(f"Error on {history_key}: {e}")
            # self.converter.send_to_corrections(history_key)

    def map_histories(self) -> None:
        history_keys = self.converter.list_parsed_histories_keys()[::-1]
        for history_key in tqdm(history_keys):
            self.map_history(history_key)
        DBPlayerStats.update_all_stats()

    @staticmethod
    def check_is_mapped(history_key: str) -> bool:
        hand_id = history_key.split("/")[-1].split("\\")[-1].split(".")[0]
        return DBHandHistory.objects.filter(hand_id=hand_id).exists()

    def map_new_histories(self) -> None:
        history_keys = self.converter.list_parsed_histories_keys()
        histories_to_map = [history_key for history_key in history_keys if not self.check_is_mapped(history_key)]
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.map_history, history_key) for history_key in histories_to_map]
            for future in tqdm(as_completed(futures)):
                future.result()
        DBPlayerStats.update_all_stats()



