from pkrcomponents.components.players.datafields.postflop import POSTFLOP_FIELDS
from pkrcomponents.components.players.street_hand_stats.postflop import PostflopPlayerHandStats

from pkrdatamapper.actions.action_move.models import DBActionMove
from pkrdatamapper.actions.actions_sequence.models import DBActionsSequence
from pkrdatamapper.histories.hand_history.models import DBHandHistory
from pkrdatamapper.histories.street_player_hand_stats.base import DBStreetPlayerHandStats
from pkrdatamapper.players.player.models import DBPlayer


class DBPostflopPlayerHandStats(DBStreetPlayerHandStats):
    """
    A Database class to store postflop player stats, resulting from the analysis of hand histories.
    """
    data_attr_fields = POSTFLOP_FIELDS
    prefix = ''

    class Meta:
        abstract = True

    @classmethod
    def from_stats(cls, player: DBPlayer, hand_history: DBHandHistory, postflop_stats: PostflopPlayerHandStats):
        """
        Create a new instance of the class from a PostflopPlayerHandStats instance.
        """
        actions_sequence = DBActionsSequence.from_actions_sequence(postflop_stats.actions_sequence)
        move_facing_1bet = DBActionMove.from_action_move(postflop_stats.move_facing_1bet)
        move_facing_2bet = DBActionMove.from_action_move(postflop_stats.move_facing_2bet)
        move_facing_3bet = DBActionMove.from_action_move(postflop_stats.move_facing_3bet)
        move_facing_4bet = DBActionMove.from_action_move(postflop_stats.move_facing_4bet)
        move_facing_cbet = DBActionMove.from_action_move(postflop_stats.move_facing_cbet)
        move_facing_donk_bet = DBActionMove.from_action_move(postflop_stats.move_facing_donk_bet)
        db_postflop_stats, created = cls.objects.update_or_create(
            player=player,
            hand_history=hand_history,
            defaults=dict(
                # flags
                flag_saw=postflop_stats.flag_saw,
                flag_first_to_talk=postflop_stats.flag_first_to_talk,
                flag_has_position=postflop_stats.flag_has_position,
                flag_bet=postflop_stats.flag_bet,
                flag_open_opportunity=postflop_stats.flag_open_opportunity,
                flag_open=postflop_stats.flag_open,
                flag_cbet_opportunity=postflop_stats.flag_cbet_opportunity,
                flag_cbet=postflop_stats.flag_cbet,
                flag_face_cbet=postflop_stats.flag_face_cbet,
                flag_donk_bet_opportunity=postflop_stats.flag_donk_bet_opportunity,
                flag_donk_bet=postflop_stats.flag_donk_bet,
                flag_face_donk_bet=postflop_stats.flag_face_donk_bet,
                flag_first_raise=postflop_stats.flag_first_raise,
                flag_fold=postflop_stats.flag_fold,
                flag_check=postflop_stats.flag_check,
                flag_check_raise=postflop_stats.flag_check_raise,
                flag_face_raise=postflop_stats.flag_face_raise,
                flag_3bet_opportunity=postflop_stats.flag_3bet_opportunity,
                flag_3bet=postflop_stats.flag_3bet,
                flag_face_3bet=postflop_stats.flag_face_3bet,
                flag_4bet_opportunity=postflop_stats.flag_4bet_opportunity,
                flag_4bet=postflop_stats.flag_4bet,
                flag_face_4bet=postflop_stats.flag_face_4bet,
                # counts
                count_player_calls=postflop_stats.count_player_calls,
                count_player_raises=postflop_stats.count_player_raises,
                # sequences
                actions_sequence=actions_sequence,
                # amounts
                amount_effective_stack=postflop_stats.amount_effective_stack,
                amount_to_call_facing_1bet=postflop_stats.amount_to_call_facing_1bet,
                amount_to_call_facing_2bet=postflop_stats.amount_to_call_facing_2bet,
                amount_to_call_facing_3bet=postflop_stats.amount_to_call_facing_3bet,
                amount_to_call_facing_4bet=postflop_stats.amount_to_call_facing_4bet,
                amount_bet_made=postflop_stats.amount_bet_made,
                amount_first_raise_made=postflop_stats.amount_first_raise_made,
                amount_second_raise_made=postflop_stats.amount_second_raise_made,
                ratio_to_call_facing_1bet=postflop_stats.ratio_to_call_facing_1bet,
                ratio_to_call_facing_2bet=postflop_stats.ratio_to_call_facing_2bet,
                ratio_to_call_facing_3bet=postflop_stats.ratio_to_call_facing_3bet,
                ratio_to_call_facing_4bet=postflop_stats.ratio_to_call_facing_4bet,
                ratio_bet_made=postflop_stats.ratio_bet_made,
                ratio_first_raise_made=postflop_stats.ratio_first_raise_made,
                ratio_second_raise_made=postflop_stats.ratio_second_raise_made,
                total_bet_amount=postflop_stats.total_bet_amount,
                # moves
                move_facing_1bet=move_facing_1bet,
                move_facing_2bet=move_facing_2bet,
                move_facing_3bet=move_facing_3bet,
                move_facing_4bet=move_facing_4bet,
                move_facing_cbet=move_facing_cbet,
                move_facing_donk_bet=move_facing_donk_bet)
        )
        return db_postflop_stats
