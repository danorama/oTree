# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


def vars_for_all_templates(self):
    return {'instructions': 'trust_b/Instructions.html', 'constants': Constants}


class Introduction(Page):

    template_name = 'global/Introduction.html'

    def vars_for_template(self):
        return {'amount_allocated': Constants.allocated_amount}

    timeout_seconds = 90
    def before_next_page(self):
        if self.timeout_happened:
            self.player.page_timed_out = True

class Question1(Page):
    template_name = 'global/Question.html'
    form_model = models.Player
    form_fields = ['training_participant1_payoff', 'training_participant2_payoff']
    question = ('Suppose that both participants start with $1.00, then participant 1 sends $0.20 to participant 2. '
    'How much would participants 1 and 2 have?')

    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        return {'num_q': 1, 'question': self.question}

    timeout_seconds = 75
    def before_next_page(self):
        if self.timeout_happened:
            self.player.page_timed_out = True


class Feedback1(Page):
    template_name = 'trust_b/Feedback.html'

    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        p = self.player
        return {'answers': {
                'participant 1': [p.training_participant1_payoff, 0.80],
                'participant 2': [p.training_participant2_payoff, 1.60]}}

    timeout_seconds = 75
    def before_next_page(self):
        if self.timeout_happened:
            self.player.page_timed_out = True


class Offer(Page):

    form_model = models.Group
    form_fields = ['sent']

    def is_displayed(self):
        return self.player.id_in_group == 1

    timeout_seconds = 75
    def before_next_page(self):
        if self.timeout_happened:
            self.player.page_timed_out = True


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()

    def body_text(self):
        if self.player.id_in_group == 2:
            return "You are participant 2. \
                Waiting for participant 1 to decide."
        return 'Please wait'


class Results(Page):

    def offer(self):
        return self.group.sent

    def vars_for_template(self):
        return {'offer': self.offer}

    timeout_seconds = 75
    def before_next_page(self):
        if self.timeout_happened:
            self.player.page_timed_out = True


page_sequence = [Introduction,
            Question1,
            Feedback1,
            Offer,
            ResultsWaitPage,
            Results]
