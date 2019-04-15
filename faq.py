from sopel.module import commands
from sopel.config.types import StaticSection, ValidatedAttribute
import json, os


class FaqSection(StaticSection):
    path = ValidatedAttribute('path')


def configure(config):
    config.define_section('faq', FaqSection, validate=False)

    config.faq.configure_setting('path', 'Path where questions/answers are stored')


def setup(bot):
    global answers

    bot.config.define_section('faq', FaqSection)


@commands("faq")
def faq(bot, trigger):
    path     = bot.config.faq.path
    answers  = json.load(open(path))

    question = trigger.match.group(2)

    if question in answers:
        bot.say(answers[question])
