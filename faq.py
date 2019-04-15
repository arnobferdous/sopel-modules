from sopel.module import commands
import json, os


def setup(bot):
    global answers

    answers = json.load(open(os.path.dirname(os.path.realpath(__file__)) + '/data/faq'))


@commands("faq")
def faq(bot, trigger):
    question = trigger.match.group(2)

    if question in answers:
        bot.say(answers[question])
