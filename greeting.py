from sopel.config.types import StaticSection, ChoiceAttribute, ValidatedAttribute
from sopel.module import rule, event, interval
from sopel.tools import SopelMemory
import time


timeout = greeting = None


class GreetingSection(StaticSection):
    timeout  = ValidatedAttribute('timeout', int)
    greeting = ValidatedAttribute('greeting')


def configure(config):
    config.define_section('greeting', GreetingSection, validate=False)

    config.greeting.configure_setting('timeout', 'How long after a user joins to listen and respond with the greeting (in seconds)')
    config.greeting.configure_setting('greeting', 'Greeting to use')


def setup(bot):
    global timeout, greeting

    bot.config.define_section('greeting', GreetingSection)

    timeout = bot.config.greeting.timeout
    greeting = bot.config.greeting.greeting

    if 'greeting' not in bot.memory:
        bot.memory['greeting'] = SopelMemory()


@event('JOIN')
@rule('.*')
def joined(bot, trigger):
    if bot.nick == trigger.nick:
        return
    else:
        uid = bot.db.get_nick_id(trigger.nick, create=True)
        jtime = time.time()

        bot.memory['greeting'][uid] = jtime


@rule('.*')
def speak(bot, trigger):
    global timeout, greeting
    uid = bot.db.get_nick_id(trigger.nick, create=True)
    ctime = time.time()

    if uid in bot.memory['greeting']:
        jtime = bot.memory['greeting'][uid]

        if ctime - jtime <= timeout:
            bot.say(greeting)

        del bot.memory['greeting'][uid]


@event('PART')
@event('QUIT')
@rule('.*')
def cleanup_events(bot, trigger):
    uid = bot.db.get_nick_id(trigger.nick, create=True)

    if uid in bot.memory['greeting']:
        del bot.memory['greeting'][uid]


@interval(90)
def cleanup_interval(bot):
    global timeout
    ctime = time.time()

    for key, val in bot.memory['greeting'].items():
        if ctime - val > timeout:
            del bot.memory['greeting'][key]