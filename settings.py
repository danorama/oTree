import os

import dj_database_url
from boto.mturk import qualification

import otree.settings

# using below to actually parse our config files
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('otree_config.properties')


# to get the right name from the forward and fix the link problem
USE_X_FORWARDED_HOST = True


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# OTREE_PRODUCTION just controls whether Django runs in
# DEBUG mode. If OTREE_PRODUCTION==1, then DEBUG=False
# os.environ.get('OTREE_PRODUCTION')
if config.get('oTreeSettings', 'otree.production') not in {None, '', '0'}:
    DEBUG = False
else:
    DEBUG = True

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'otree'
# don't share this with anybody.
# Change this to something unique (e.g. mash your keyboard),
# and then delete this comment.
SECRET_KEY = 'zzzzzzzzzzzzzzzzzzzzzzzzzzz'

PAGE_FOOTER = ''

#DATABASES = {
#    'default': dj_database_url.config(
#        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
#    )
#}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config.get('DatabaseSettings', 'database.name'),
        'USER': config.get('DatabaseSettings', 'database.user'),
        'PASSWORD': config.get('DatabaseSettings', 'database.password'),
        'HOST': config.get('DatabaseSettings', 'database.host'),   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}

# AUTH_LEVEL:
# If you are launching an experiment and want visitors to only be able to
# play your app if you provided them with a start link, set the
# environment variable OTREE_AUTH_LEVEL to EXPERIMENT.
# If you would like to put your site online in public demo mode where
# anybody can play a demo version of your game, set OTREE_AUTH_LEVEL
# to DEMO. This will allow people to play in demo mode, but not access
# the full admin interface.

#os.environ.get('OTREE_AUTH_LEVEL')
AUTH_LEVEL = config.get('oTreeSettings', 'otree.auth.level')

# ACCESS_CODE_FOR_DEFAULT_SESSION:
# If you have a "default session" set,
# then an access code will be appended to the URL for authentication.
# You can change this as frequently as you'd like,
# to prevent unauthorized server access.

ACCESS_CODE_FOR_DEFAULT_SESSION = 'my_access_code'

# setting for integration with AWS Mturk
#os.environ.get('AWS_ACCESS_KEY_ID')
AWS_ACCESS_KEY_ID = config.get('MechanicalTurkSettings', 'mturk.access_key_id')
#os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = config.get('MechanicalTurkSettings', 'mturk.secret_access_key')


# e.g. EUR, CAD, GBP, CHF, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

# The following line was added to prevent extra players from being created.
MTURK_NUM_PARTICIPANTS_MULT = 1


# e.g. en-gb, de-de, it-it, fr-fr.
# see: https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'en-us'


INSTALLED_APPS = [
    'otree',
]

if 'SENTRY_DSN' in os.environ:
    INSTALLED_APPS += [
        'raven.contrib.django.raven_compat',
    ]

DEMO_PAGE_INTRO_TEXT = """
<ul>
    <li>
        <a href="https://github.com/oTree-org/otree" target="_blank">
            Source code
        </a> for the below games.
    </li>
    <li>
        <a href="http://www.otree.org/" target="_blank">
            oTree homepage
        </a>.
    </li>
</ul>
<p>
    Below are various games implemented with oTree. These games are all open
    source, and you can modify them as you wish to create your own variations.
    Click one to learn more and play.
</p>
"""

# from here on are qualifications requirements for workers
# see description for requirements on Amazon Mechanical Turk website:
# http://docs.aws.amazon.com/AWSMechTurk/latest/AWSMturkAPI/ApiReference_QualificationRequirementDataStructureArticle.html
# and also in docs for boto:
# https://boto.readthedocs.org/en/latest/ref/mturk.html?highlight=mturk#module-boto.mturk.qualification

mturk_hit_settings = {
    'keywords': ['easy', 'bonus', 'choice', 'study'],
    'title': 'A Brief Economic Experiment - CSN ',
    'description': 'This is a simple economic experiment that should only take a minute or two.',
    'frame_height': 500,
    'preview_template': 'global/MTurkPreview.html',
    'minutes_allotted_per_assignment': 60,
    'expiration_hours': 7*24, # 7 days
    #'grant_qualification_id': '3Q1RN8J3I90RAYEZ2YY7UEFAD26M8P',# to prevent retakes
    'qualification_requirements': [
        qualification.LocaleRequirement("EqualTo", "US"),
        #qualification.PercentAssignmentsApprovedRequirement("GreaterThanOrEqualTo", 95),
        #qualification.NumberHitsApprovedRequirement("GreaterThanOrEqualTo", 500),
        qualification.Requirement('3Q1RN8J3I90RAYEZ2YY7UEFAD26M8P', 'DoesNotExist')
    ]
}

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 0.01,
    'participation_fee': 0.25,
    'num_bots': 12,
    'doc': "",
    'group_by_arrival_time': True,
    'mturk_hit_settings': mturk_hit_settings,
}

SESSION_CONFIGS = [
    {
        'name': 'public_goods',
        'display_name': "Public Goods",
        'num_demo_participants': 3,
        'app_sequence': ['public_goods', 'payment_info'],
    },
    {
        'name': 'public_goods_simple',
        'display_name': "Public Goods (simple version from tutorial)",
        'num_demo_participants': 3,
        'app_sequence': ['public_goods_simple', 'survey', 'payment_info'],
    },
    {
        'name': 'trust',
        'display_name': "Trust Game",
        'num_demo_participants': 2,
        'app_sequence': ['trust', 'payment_info'],
    },
    {
        'name': 'trust_simple',
        'display_name': "Trust Game (simple version from tutorial)",
        'num_demo_participants': 2,
        'app_sequence': ['trust_simple'],
    },
    {
        'name': 'trust_a',
        'display_name': "Trust Game A",
        'num_demo_participants': 2,
        'app_sequence': ['trust_a'],
    },
    {
        'name': 'trust_b',
        'display_name': "Trust Game B",
        'num_demo_participants': 2,
        'app_sequence': ['trust_b'],
    },
    {
        'name': 'trust_c',
        'display_name': "Trust Game C",
        'num_demo_participants': 2,
        'app_sequence': ['trust_c'],
    },
    {
        'name': 'trust_d',
        'display_name': "Trust Game D",
        'num_demo_participants': 2,
        'app_sequence': ['trust_d'],
    },
    {
        'name': 'trust_e',
        'display_name': "Trust Game E",
        'num_demo_participants': 2,
        'app_sequence': ['trust_e'],
    },
    {
        'name': 'trust_f',
        'display_name': "Trust Game F",
        'num_demo_participants': 2,
        'app_sequence': ['trust_f'],
    },
    {
        'name': 'trust_def',
        'display_name': "Trust Game D_E_F",
        'num_demo_participants': 2,
        'app_sequence': ['trust_session_instructions', 'trust_d', 'trust_e', 'trust_f'],
    },
    {
        'name': 'beauty',
        'display_name': "Beauty Contest",
        'num_demo_participants': 5,
        'num_bots': 5,
        'app_sequence': ['beauty', 'payment_info'],
    },
    {
        'name': 'survey',
        'display_name': "Survey",
        'num_demo_participants': 1,
        'app_sequence': ['survey', 'payment_info'],
    },
    {
        'name': 'prisoner',
        'display_name': "Prisoner's Dilemma",
        'num_demo_participants': 2,
        'app_sequence': ['prisoner', 'payment_info'],
    },
    {
        'name': 'ultimatum',
        'display_name': "Ultimatum (randomized: strategy vs. direct response)",
        'num_demo_participants': 2,
        'app_sequence': ['ultimatum', 'payment_info'],
    },
    {
        'name': 'ultimatum_strategy',
        'display_name': "Ultimatum (strategy method treatment)",
        'num_demo_participants': 2,
        'app_sequence': ['ultimatum', 'payment_info'],
        'treatment': 'strategy',
    },
    {
        'name': 'ultimatum_non_strategy',
        'display_name': "Ultimatum (direct response treatment)",
        'num_demo_participants': 2,
        'app_sequence': ['ultimatum', 'payment_info'],
        'treatment': 'direct_response',
    },
    {
        'name': 'battle_of_the_sexes',
        'display_name': "Battle of the Sexes",
        'num_demo_participants': 2,
        'app_sequence': [
            'battle_of_the_sexes', 'payment_info'
        ],
    },
    {
        'name': 'vickrey_auction',
        'display_name': "Vickrey Auction",
        'num_demo_participants': 3,
        'app_sequence': ['vickrey_auction', 'payment_info'],
    },
    {
        'name': 'volunteer_dilemma',
        'display_name': "Volunteer's Dilemma",
        'num_demo_participants': 3,
        'app_sequence': ['volunteer_dilemma', 'payment_info'],
    },
    {
        'name': 'cournot_competition',
        'display_name': "Cournot Competition",
        'num_demo_participants': 2,
        'app_sequence': [
            'cournot_competition', 'payment_info'
        ],
    },
    {
        'name': 'principal_agent',
        'display_name': "Principal Agent",
        'num_demo_participants': 2,
        'app_sequence': ['principal_agent', 'payment_info'],
    },
    {
        'name': 'dictator',
        'display_name': "Dictator Game",
        'num_demo_participants': 2,
        'app_sequence': ['dictator', 'payment_info'],
    },
    {
        'name': 'matching_pennies',
        'display_name': "Matching Pennies",
        'num_demo_participants': 2,
        'app_sequence': [
            'matching_pennies', 'payment_info'
        ],
    },
    {
        'name': 'matching_pennies_tutorial',
        'display_name': "Matching Pennies (tutorial version)",
        'num_demo_participants': 2,
        'app_sequence': [
            'matching_pennies_tutorial',
        ],
    },
    {
        'name': 'traveler_dilemma',
        'display_name': "Traveler's Dilemma",
        'num_demo_participants': 2,
        'app_sequence': ['traveler_dilemma', 'payment_info'],
    },
    {
        'name': 'bargaining',
        'display_name': "Bargaining Game",
        'num_demo_participants': 2,
        'app_sequence': ['bargaining', 'payment_info'],
    },
    {
        'name': 'common_value_auction',
        'display_name': "Common Value Auction",
        'num_demo_participants': 3,
        'app_sequence': ['common_value_auction', 'payment_info'],
    },
    {
        'name': 'stackelberg_competition',
        'display_name': "Stackelberg Competition",
        'real_world_currency_per_point': 0.01,
        'num_demo_participants': 2,
        'app_sequence': [
            'stackelberg_competition', 'payment_info'
        ],
    },
    {
        'name': 'bertrand_competition',
        'display_name': "Bertrand Competition",
        'num_demo_participants': 2,
        'app_sequence': [
            'bertrand_competition', 'payment_info'
        ],
    },
    {
        'name': 'stag_hunt',
        'display_name': "Stag Hunt",
        'num_demo_participants': 2,
        'app_sequence': ['stag_hunt', 'payment_info'],
    },
    {
        'name': 'real_effort',
        'display_name': "Real-effort transcription task",
        'num_demo_participants': 1,
        'app_sequence': [
            'real_effort',
        ],
    },
    {
        'name': 'lemon_market',
        'display_name': "Lemon Market Game",
        'num_demo_participants': 3,
        'app_sequence': [
            'lemon_market', 'payment_info'
        ],
    },
]


otree.settings.augment_settings(globals())
