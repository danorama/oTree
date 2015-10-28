# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


def vars_for_all_templates(self):
    return {'instructions': 'dictator/Instructions.html',
            'constants': Constants}


class Introduction(Page):

    template_name = 'global/Introduction.html'


class Question1(Page):
    template_name = 'global/Question.html'
    form_model = models.Player
    form_fields = ['training_participant1_payoff', 'training_participant2_payoff']
	question = ('Suppose that Participant 1 starts with $0.50 and Participant 2 starts with $0.75, '
	'then Participant 2 sends $0.10 to Pareticipant 1. How much would participants 1 and 2 have?')

    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        return {'num_q': 1, 'question': self.question}


class Feedback1(Page):
    template_name = 'trust_c/Feedback.html'

    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        p = self.player
        return {'answers': {
                'participant 1': [p.training_participant1_payoff, 0.60],
                'participant 2': [p.training_participant2_payoff, 0.65]}}


class Offer(Page):

    form_model = models.Group
    form_fields = ['sent']

    def is_displayed(self):
        return self.player.id_in_group == 2


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()

    def body_text(self):
        if self.player.id_in_group == 1:
            return "You are participant 1. \
                Waiting for participant 2 to decide."
        return 'Please wait'


class Results(Page):

    def offer(self):
        return 3*self.group.sent

    def vars_for_template(self):
        return {'offer': self.offer}


page_sequence = [Introduction,
            Question1,
            Feedback1,
            Offer,
            ResultsWaitPage,
            Results]
