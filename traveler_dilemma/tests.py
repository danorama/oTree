import traveler_dilemma.views as views
from traveler_dilemma._builtin import Bot
import random


class PlayerBot(Bot):

    def play(self):

        # basic assertions
        assert (self.subsession.max_amount == 1.00)
        assert (self.subsession.min_amount == 0.20)

        # start game
        self.submit(views.Introduction)

        # player 1: claim
        if self.player.id_in_group == 1:
            self.play_p1()

        # player 2: claim
        else:
            self.play_p2()

        self.submit(views.Results)
        print self.player.payoff

    def play_p1(self):
        self.submit(views.Claim, {"claim": random.choice(self.group.claim_choices())})

    def play_p2(self):
        self.submit(views.Claim, {"claim": random.choice(self.group.claim_choices())})
