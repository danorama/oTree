import otree.test
import lemon_market.views as views
from lemon_market._builtin import Bot
import random
from otree.common import money_range

class PlayerBot(Bot):

    def play(self):

        # start
        self.submit(views.Introduction)

        # bid
        self.submit(views.Bid, {'bid_amount': random.choice(money_range(0, self.subsession.max_bid_amount))})

        # results
        self.submit(views.Results)