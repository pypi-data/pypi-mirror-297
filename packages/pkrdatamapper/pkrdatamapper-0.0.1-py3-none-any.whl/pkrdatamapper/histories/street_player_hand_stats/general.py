from pkrcomponents.components.players.datafields.general import GENERAL_FIELDS
from pkrcomponents.components.players.street_hand_stats.general import GeneralPlayerHandStats

from pkrdatamapper.actions.action_move.models import DBActionMove
from pkrdatamapper.actions.street.models import DBStreet
from pkrdatamapper.cards.combo.models import DBCombo
from pkrdatamapper.histories.hand_history.models import DBHandHistory
from pkrdatamapper.histories.street_player_hand_stats.base import DBStreetPlayerHandStats
from pkrdatamapper.players.player.models import DBPlayer
from pkrdatamapper.players.position.models import DBPosition


class DBGeneralHandStats(DBStreetPlayerHandStats):
    """
    A Database class to store general player stats, resulting from the analysis of hand histories.
    """
    data_attr_fields = GENERAL_FIELDS
    prefix = 'general'

    class Meta:
        verbose_name = 'General Player Hand Stats'
        db_table = 'general_player_hand_stats'

    @classmethod
    def from_stats(cls, player: DBPlayer, hand_history: DBHandHistory , general_stats: GeneralPlayerHandStats):
        """
        Create a new instance of the class from a pkrcomponents GeneralPlayerHandStats instance.
        """
        combo = DBCombo.from_combo(general_stats.combo) if general_stats.combo else None
        position = DBPosition.from_position(general_stats.position) if general_stats.position else None
        fold_street = DBStreet.from_street(general_stats.fold_street) if general_stats.fold_street else None
        all_in_street = DBStreet.from_street(general_stats.all_in_street) if general_stats.all_in_street else None
        face_covering_bet_street = DBStreet.from_street(general_stats.face_covering_bet_street) \
            if general_stats.face_covering_bet_street else None
        face_all_in_street = DBStreet.from_street(general_stats.face_all_in_street) \
            if general_stats.face_all_in_street else None
        facing_covering_bet_move = DBActionMove.from_action_move(general_stats.facing_covering_bet_move) \
            if general_stats.facing_covering_bet_move else None
        facing_all_in_move = DBActionMove.from_action_move(general_stats.facing_all_in_move) \
            if general_stats.facing_all_in_move else None
        db_general_stats, _ = cls.objects.update_or_create(
            player=player,
            hand_history=hand_history,
            defaults={
                "combo": combo,
                "position": position,
                "starting_stack": general_stats.starting_stack,
                "bounty": general_stats.bounty,
                "seat": general_stats.seat,
                "amount_won": general_stats.amount_won,
                "chips_difference": general_stats.chips_difference,
                "amount_expected_won": general_stats.amount_expected_won,
                "flag_went_to_showdown": general_stats.flag_went_to_showdown,
                "flag_is_hero": general_stats.flag_is_hero,
                "flag_won_hand": general_stats.flag_won_hand,
                "total_bet_amount": general_stats.total_bet_amount,
                "fold_street": fold_street,
                "all_in_street": all_in_street,
                "face_covering_bet_street": face_covering_bet_street,
                "face_all_in_street": face_all_in_street,
                "facing_covering_bet_move": facing_covering_bet_move,
                "facing_all_in_move": facing_all_in_move

            }
        )
        return db_general_stats
