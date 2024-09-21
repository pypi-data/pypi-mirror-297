from pkrcomponents.components.players.street_hand_stats.preflop import PreflopPlayerHandStats
from pkrcomponents.components.players.datafields.preflop import PREFLOP_FIELDS
from pkrdatamapper.actions.action_move.models import DBActionMove
from pkrdatamapper.actions.actions_sequence.models import DBActionsSequence
from pkrdatamapper.histories.hand_history.models import DBHandHistory
from pkrdatamapper.histories.street_player_hand_stats.base import DBStreetPlayerHandStats
from pkrdatamapper.players.player.models import DBPlayer


class DBPreflopHandStats(DBStreetPlayerHandStats):
    """
    A Database class to store preflop player stats, resulting from the analysis of hand histories.
    """
    data_attr_fields = PREFLOP_FIELDS
    prefix = 'preflop'

    class Meta:
        verbose_name = 'Preflop Player Hand Stats'
        db_table = 'preflop_player_hand_stats'

    @classmethod
    def from_stats(cls, player: DBPlayer, hand_history: DBHandHistory, preflop_stats: PreflopPlayerHandStats):
        actions_sequence = DBActionsSequence.from_actions_sequence(preflop_stats.actions_sequence)
        move_facing_2bet = DBActionMove.from_action_move(preflop_stats.move_facing_2bet)
        move_facing_3bet = DBActionMove.from_action_move(preflop_stats.move_facing_3bet)
        move_facing_4bet = DBActionMove.from_action_move(preflop_stats.move_facing_4bet)
        move_facing_squeeze = DBActionMove.from_action_move(preflop_stats.move_facing_squeeze)
        move_facing_steal_attempt = DBActionMove.from_action_move(preflop_stats.move_facing_steal_attempt)
        db_preflop_stats, _ = cls.objects.update_or_create(
            player=player,
            hand_history=hand_history,
            defaults={
                "flag_vpip": preflop_stats.flag_vpip,
                "flag_open_opportunity": preflop_stats.flag_open_opportunity,
                "flag_open": preflop_stats.flag_open,
                "flag_first_raise": preflop_stats.flag_first_raise,
                "flag_fold": preflop_stats.flag_fold,
                "flag_limp": preflop_stats.flag_limp,
                "flag_cold_called": preflop_stats.flag_cold_called,
                "flag_raise_opportunity": preflop_stats.flag_raise_opportunity,
                "flag_raise": preflop_stats.flag_raise,
                "flag_face_raise": preflop_stats.flag_face_raise,
                "flag_3bet_opportunity": preflop_stats.flag_3bet_opportunity,
                "flag_3bet": preflop_stats.flag_3bet,
                "flag_face_3bet": preflop_stats.flag_face_3bet,
                "flag_4bet_opportunity": preflop_stats.flag_4bet_opportunity,
                "flag_4bet": preflop_stats.flag_4bet,
                "flag_face_4bet": preflop_stats.flag_face_4bet,
                "flag_squeeze_opportunity": preflop_stats.flag_squeeze_opportunity,
                "flag_squeeze": preflop_stats.flag_squeeze,
                "flag_face_squeeze": preflop_stats.flag_face_squeeze,
                "flag_steal_opportunity": preflop_stats.flag_steal_opportunity,
                "flag_steal_attempt": preflop_stats.flag_steal_attempt,
                "flag_face_steal_attempt": preflop_stats.flag_face_steal_attempt,
                "flag_fold_to_steal_attempt": preflop_stats.flag_fold_to_steal_attempt,
                "flag_blind_defense_opportunity": preflop_stats.flag_blind_defense_opportunity,
                "flag_blind_defense": preflop_stats.flag_blind_defense,
                "flag_open_shove": preflop_stats.flag_open_shove,
                "flag_voluntary_all_in": preflop_stats.flag_voluntary_all_in,
                    # counts
                "count_player_calls": preflop_stats.count_player_calls,
                "count_player_raises": preflop_stats.count_player_raises,
                "count_faced_limps": preflop_stats.count_faced_limps,
                    # sequences
                "actions_sequence": actions_sequence,
                    # amounts
                "amount_effective_stack": preflop_stats.amount_effective_stack,
                "amount_to_call_facing_1bet": preflop_stats.amount_to_call_facing_1bet,
                "amount_to_call_facing_2bet": preflop_stats.amount_to_call_facing_2bet,
                "amount_to_call_facing_3bet": preflop_stats.amount_to_call_facing_3bet,
                "amount_to_call_facing_4bet": preflop_stats.amount_to_call_facing_4bet,
                "amount_first_raise_made": preflop_stats.amount_first_raise_made,
                "amount_second_raise_made": preflop_stats.amount_second_raise_made,
                "ratio_to_call_facing_1bet": preflop_stats.ratio_to_call_facing_1bet,
                "ratio_to_call_facing_2bet": preflop_stats.ratio_to_call_facing_2bet,
                "ratio_to_call_facing_3bet": preflop_stats.ratio_to_call_facing_3bet,
                "ratio_to_call_facing_4bet": preflop_stats.ratio_to_call_facing_4bet,
                "ratio_first_raise_made": preflop_stats.ratio_first_raise_made,
                "ratio_second_raise_made": preflop_stats.ratio_second_raise_made,
                "total_bet_amount": preflop_stats.total_bet_amount,
                    # moves
                "move_facing_2bet": move_facing_2bet,
                "move_facing_3bet": move_facing_3bet,
                "move_facing_4bet": move_facing_4bet,
                "move_facing_squeeze": move_facing_squeeze,
                "move_facing_steal_attempt": move_facing_steal_attempt
            }
            # flags

        )
        return db_preflop_stats
