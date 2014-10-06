# -*- coding: utf-8 -*-
from __future__ import division
"""Documentation at https://github.com/oTree-org/otree/wiki"""

from otree.db import models
import otree.models


doc = """
In Stackelberg competition, firms decide sequentially on how many units to produce. The unit selling price depends on the total units produced. 
In this one-period implementation, the order of play is randomly determined.
<br />
Source code <a href="https://github.com/oTree-org/oTree/tree/master/stackelberg_competition" target="_blank">here</a>.
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'stackelberg_competition'

    total_capacity = models.PositiveIntegerField(
        default=60,
        doc="""Total production capacity of BOTH players"""
    )

    currency_per_point = models.MoneyField(
        default=0.01,
        doc="""Currency units for a single point"""
    )

    def max_units_per_player(self):
        return self.total_capacity / 2




class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    price_in_points = models.PositiveIntegerField(
        default=None,
        doc="""Unit price: P = T - Q1 - Q2, where T is total capacity and Q_i are the units produced by the players"""
    )

    players_per_group = 2


class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    payoff_in_points = models.PositiveIntegerField(
        default=None,
    )

    quantity = models.PositiveIntegerField(
        default=None,
        doc="""Quantity of units to produce"""
    )

    def quantity_choices(self):
        return range(0, self.subsession.max_units_per_player()+1)

    def other_player(self):
        """Returns the opponent of the current player"""
        return self.other_players_in_group()[0]

    def set_payoff(self):
        self.group.price_in_points = self.subsession.total_capacity - self.quantity - self.other_player().quantity
        self.payoff_in_points = self.group.price_in_points * self.quantity
        self.payoff = self.payoff_in_points * self.subsession.currency_per_point


