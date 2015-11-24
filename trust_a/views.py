# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range

from ._builtin import Page, WaitPage
from . import models
from .models import Constants


def vars_for_all_templates(self):
    return {'instructions': 'trust_a/Instructions.html', 'total_q': 1}


class Introduction(Page):

    template_name = 'global/Introduction.html'

    def vars_for_template(self):
        return {'amount_allocated': Constants.amount_allocated}

    timeout_seconds = 90
    def before_next_page(self):
        if self.timeout_happened:
            self.player.page_timed_out = True


class Question1(Page):
    template_name = 'global/Question.html'
    form_model = models.Player
    form_fields = ['training_answer_x', 'training_answer_y']
    question = (
        'Suppose that both participants start with $1.00, then Participant 1 sends $0.20 to Participant 2. '
        'The experimenter triples this amount, so Participant 2 receives $0.60.'
        'Having received the tripled amount, Participant 2 sends $0.50 to '
        'Participant 1. In the end, how much would Participants 1 and 2 '
        'have?'
    )

    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        return {'num_q': 1, 'question': self.question}

    timeout_seconds = 75
    def before_next_page(self):
        if self.timeout_happened:
            self.player.page_timed_out = True


class Feedback(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        return {
            'num_q': 1,
        }

    timeout_seconds = 75
    def before_next_page(self):
        if self.timeout_happened:
            self.player.page_timed_out = True



class Send(Page):

    """This page is only for P1
    P1 sends amount (all, some, or none) to P2
    This amount is tripled by experimenter,
    i.e if sent amount by P1 is 5, amount received by P2 is 15"""

    form_model = models.Group
    form_fields = ['sent_amount']

    def is_displayed(self):
        return self.player.id_in_group == 1

    timeout_seconds = 75
    def before_next_page(self):
        if self.timeout_happened:
            self.player.page_timed_out = True

class SendBack(Page):

    """This page is only for P2
    P2 sends back some amount (of the tripled amount received) to P1"""

    form_model = models.Group
    form_fields = ['sent_back_amount']

    def is_displayed(self):
        return self.player.id_in_group == 2

    def vars_for_template(self):
        tripled_amount = self.group.sent_amount * Constants.multiplication_factor
        available_amount = Constants.amount_allocated + tripled_amount

        return {'amount_allocated': Constants.amount_allocated,
                'tripled_amount': tripled_amount,
                'prompt':
                'Please enter a number from 0 to %s:' % available_amount}

    def sent_back_amount_max(self):
        return self.group.sent_amount * Constants.multiplication_factor + Constants.amount_allocated

    timeout_seconds = 75
    def before_next_page(self):
        if self.timeout_happened:
            self.player.page_timed_out = True

class ResultsWaitPage(WaitPage):


    def after_all_players_arrive(self):
        self.group.set_payoffs()

class Results(Page):

    """This page displays the earnings of each player"""

    def vars_for_template(self):
        tripled_amount = self.group.sent_amount * Constants.multiplication_factor

        return {'amount_allocated': Constants.amount_allocated,
                'result': self.player.payoff - Constants.bonus,
                'tripled_amount': self.group.sent_amount * Constants.multiplication_factor
                }
    timeout_seconds = 75
    def before_next_page(self):
        if self.timeout_happened:
            self.player.page_timed_out = True


page_sequence =  [
        Introduction,
        Question1,
        Feedback,
        Send,
        WaitPage,
        SendBack,
        ResultsWaitPage,
        Results,
    ]
