# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
import otree.models
import otree.constants
from otree import widgets
from otree.common import Currency as c, currency_range
# </standard imports>


doc = """
One player decides how to divide a certain amount between himself and the other
player.
"""

source_code = "https://github.com/oTree-org/oTree/tree/master/dictator"


bibliography = (
    (
        'Kahneman, Daniel, Jack L. Knetsch, and Richard H. Thaler. "Fairness '
        'and the assumptions of economics." Journal of business (1986): '
        'S285-S300.'
    ),
    (
        'Hoffman, Elizabeth, Kevin McCabe, and Vernon L. Smith. "Social '
        'distance and other-regarding behavior in dictator games." The '
        'American Economic Review(1996): 653-660.'
    )
)


links = {
    "Wikipedia": {
        "Dictator Game": "https://en.wikipedia.org/wiki/Dictator_game"
    }
}


keywords = ("Dictator Game", "Fairness", "Homo Economicus")


class Constants(otree.constants.BaseConstants):
    name_in_url = 'trust_b'
    players_per_group = 2
    num_rounds = 1

    bonus = c(0.50)
    # Initial amount allocated to each player
    allocated_amount = c(1.00)


class Subsession(otree.models.BaseSubsession):

    pass


class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    sent = models.CurrencyField(
        doc="""Amount dictator decided to send""",
        min=0, max=Constants.allocated_amount,
        verbose_name='I will send (from 0 to %i)' % Constants.allocated_amount
    )

    def set_payoffs(self):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p1.payoff = Constants.bonus + Constants.allocated_amount - self.sent
        p2.payoff = Constants.bonus + Constants.allocated_amount + 3*self.sent


class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    training_participant1_payoff = models.CurrencyField(verbose_name="Participant 1's payoff would be")
    training_participant2_payoff = models.CurrencyField(verbose_name="Participant 2's payoff would be")

