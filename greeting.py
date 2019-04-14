from sopel.config.types import StaticSection, ChoiceAttribute, ValidatedAttribute
from sopel.module import rule, event, interval
from sopel.tools import SopelMemory
from sopel.logger import get_logger
import time

timeout = greeting = logger = None

class GreetingSection(StaticSection):
    timeout  = ValidatedAttribute('timeout', int)
    greeting = ValidatedAttribute('greeting')


def configure(config):
    config.define_section('greeting', GreetingSection, validate=False)

    config.greeting.configure_setting('timeout', 'How long after a user joins to listen and respond with the greeting (in seconds)')
    config.greeting.configure_setting('greeting', 'Greeting to use')


def setup(bot):
    global timeout, greeting, logger

    bot.config.define_section('greeting', GreetingSection)

    timeout = bot.config.greeting.timeout
    greeting = bot.config.greeting.greeting
    logger = get_logger(__name__)

    if 'greeting' not in bot.memory:
        bot.memory['greeting'] = SopelMemory()


@event('JOIN')
@rule('.*')
def joined(bot, trigger):
    logger.info(trigger.nick + ' joined')

    if bot.nick == trigger.nick:
        logger.info('Skipping self')

        return
    else:
        uid = bot.db.get_nick_id(trigger.nick, create=True)
        jtime = time.time()

        logger.info('Starting listening for first message from ' + trigger.nick)

        bot.memory['greeting'][uid] = jtime


@rule('.*')
def speak(bot, trigger):
    global timeout, greeting
    ctime = time.time()
    uid = bot.db.get_nick_id(trigger.nick, create=True)

    logger.info('Checking message from ' + trigger.nick)

    if uid in bot.memory['greeting']:
        logger.info('Entry found, checking ' + trigger.nick)

        jtime = bot.memory['greeting'][uid]

        if ctime - jtime <= timeout:
            logger.info('Greeting ' + trigger.nick)

            bot.say(greeting)

        logger.info('Removing entry for ' + trigger.nick)

        del bot.memory['greeting'][uid]


@event('PART')
@event('QUIT')
@rule('.*')
def cleanup_events(bot, trigger):
    logger.info('Cleaning up from PART/QUIT')

    uid = bot.db.get_nick_id(trigger.nick, create=True)

    if uid in bot.memory['greeting']:
        logger.info('Removing entry for ' + trigger.nick)

        del bot.memory['greeting'][uid]


@interval(90)
def cleanup_interval(bot):
    global timeout
    ctime = time.time()

    logger.info('Cleanup time')

    for key, val in bot.memory['greeting'].items():
        if ctime - val > timeout:
            logger.info('Removing entry for ' + key)

            del bot.memory['greeting'][key]
