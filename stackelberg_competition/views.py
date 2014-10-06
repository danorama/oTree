# -*- coding: utf-8 -*-
from __future__ import division
import stackelberg_competition.models as models
from stackelberg_competition._builtin import Page, WaitPage


class Introduction(Page):

    template_name = 'stackelberg_competition/Introduction.html'

    def variables_for_template(self):
        return {'player_id': self.player.id_in_group,
                'total_capacity': self.subsession.total_capacity,
                'max_units_per_player': self.subsession.max_units_per_player(),
                'currency_per_point': self.subsession.currency_per_point}


class ChoiceOne(Page):

    def participate_condition(self):
        return self.player.id_in_group == 1

    template_name = 'stackelberg_competition/ChoiceOne.html'

    form_model = models.Player
    form_fields = ['quantity']


class ChoiceTwo(Page):

    def participate_condition(self):
        return self.player.id_in_group == 2

    template_name = 'stackelberg_competition/ChoiceTwo.html'

    form_model = models.Player
    form_fields = ['quantity']

    def variables_for_template(self):
        return {'other_quantity': self.player.other_player().quantity}


class ResultsWaitPage(WaitPage):

    scope = models.Group

    def after_all_players_arrive(self):
        for p in self.group.players:
            p.set_payoff()


class Results(Page):

    template_name = 'stackelberg_competition/Results.html'

    def variables_for_template(self):

        return {'quantity': self.player.quantity,
                'total_quantity': self.player.quantity + self.player.other_player().quantity,
                'price_in_points': self.group.price_in_points,
                'payoff_in_points': self.player.payoff_in_points,
                'payoff': self.player.payoff}


def pages():

    return [Introduction,
            ChoiceOne,
            ChoiceTwo,
            ResultsWaitPage,
            Results]
