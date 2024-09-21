from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from pkrcomponents.converters.summary_converter.abstract import AbstractSummaryConverter

from pkrdatamapper.tournaments.tournament.models import DBTournament


class AbstractSummaryMapper(ABC):
    converter: AbstractSummaryConverter

    def map_summary(self, summary_key: str) -> None:
        print(f"Mapping summary {summary_key}")
        tournament = self.converter.convert_summary(summary_key)
        db_tournament = DBTournament.from_tournament(tournament)
        db_tournament.save()

    def map_summaries(self) -> None:
        print("Mapping summaries")
        summary_keys = self.converter.list_parsed_summaries_keys()
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.map_summary, summary_key) for summary_key in summary_keys]
            for future in tqdm(as_completed(futures)):
                future.result()
        # for summary_key in tqdm(summary_keys):
        #     self.map_summary(summary_key)

    def check_is_mapped(self, summary_key: str) -> bool:
        tournament = self.converter.convert_summary(summary_key)
        tournament_id = tournament.id
        return DBTournament.objects.filter(tournament_id=tournament_id).exists()

    def map_new_summaries(self) -> None:
        summary_keys = self.converter.list_parsed_summaries_keys()
        summaries_to_map = [summary_key for summary_key in summary_keys if not self.check_is_mapped(summary_key)]
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.map_summary, summary_key) for summary_key in summaries_to_map]
            for future in tqdm(as_completed(futures)):
                future.result()
        # for summary_key in tqdm(summary_keys):
        #     if not self.check_is_mapped(summary_key):
        #         self.map_summary(summary_key)