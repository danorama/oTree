# -*- coding: utf-8 -*-
import ptree.views
import ptree.views.concrete
import public_goods.forms as forms
from public_goods.utilities import ParticipantMixin, ExperimenterMixin
from django.utils.translation import ugettext as _
from ptree.common import currency


class Introduction(ParticipantMixin, ptree.views.Page):

    """Description of the game: How to play and returns expected"""

    template_name = 'public_goods/Introduction.html'

    def show_skip_wait(self):
        return self.PageActions.show

    def variables_for_template(self):
        return {'no_of_participants': self.match.participants_per_match,
                'amount_allocated': currency(self.treatment.amount_allocated),
                'multiplication_factor': self.treatment.multiplication_factor}


class Contribute(ParticipantMixin, ptree.views.Page):

    """Participant: Choose how much to contribute"""

    template_name = 'public_goods/Contribute.html'

    def get_form_class(self):
        return forms.ContributeForm


class Results(ParticipantMixin, ptree.views.Page):

    """Participants payoff: How much each has earned"""

    template_name = 'public_goods/Results.html'

    def show_skip_wait(self):
        if self.participant.payoff is None:
            return self.PageActions.wait
        return self.PageActions.show

    def wait_page_body_text(self):
        return "Waiting for other group members to contribute."

    def variables_for_template(self):

        participants = self.match.participants()

        return {'amount_allocated': currency(self.treatment.amount_allocated),
                'contributed_amount': currency(self.participant.contributed_amount),
                'participants': participants,
                'id': self.participant.index_among_participants_in_match}


class ExperimenterPage(ExperimenterMixin, ptree.views.ExperimenterPage):

    """This page is only for the experimenter,
    and because the experimenter doesn't have to do anything in this game,
    this page is a waiting screen and is updated once all participants are finished"""

    template_name = 'public_goods/ExperimenterPage.html'

    def show_skip_wait(self):
        if any(p.contributed_amount is None for p in self.subsession.participants()):
            return self.PageActions.wait
        for m in self.subsession.matches():
            m.set_contributions()
            m.set_individual_share()
            m.save()
        for p in self.subsession.participants():
            p.set_payoff()
            p.save()
        return self.PageActions.show

    def wait_page_title_text(self):
        return _('Public Goods Game: Experimenter Page')

    def wait_page_body_text(self):
        participant_count = len(self.subsession.participants())
        participant_string = "participants" if participant_count > 1 else "participant"
        return """All {} {} have started playing the game.
                  As the experimenter in this game, you have no particular role to play.
                  This page will change once all participants have been given a
                  payoff.""".format(participant_count, participant_string)

    def variables_for_template(self):
        return {'participant_count': len(self.subsession.participants())}


def experimenter_pages():

    return [ExperimenterPage]


def pages():
    return [
        Introduction,
        Contribute,
        Results
    ]
