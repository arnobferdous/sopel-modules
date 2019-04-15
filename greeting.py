from sopel.config.types import StaticSection, ValidatedAttribute, ListAttribute    
from sopel.module import rule, event, interval, commands
from sopel.tools import SopelMemory
from sopel.logger import get_logger
import time


class GreetingSection(StaticSection):
    timeout   = ValidatedAttribute('timeout', int)
    greeting  = ValidatedAttribute('greeting')
    whitelist = ListAttribute('whitelist')


def configure(config):
    config.define_section('greeting', GreetingSection, validate=False)

    config.greeting.configure_setting('timeout', 'How long after a user joins to listen and respond with the greeting (in seconds)')
    config.greeting.configure_setting('greeting', 'Greeting to use')
    config.greeting.configure_setting('whitelist', 'List of channels to greet in')


def setup(bot):
    global timeout, greeting, whitelist, logger

    bot.config.define_section('greeting', GreetingSection)

    timeout   = bot.config.greeting.timeout
    greeting  = bot.config.greeting.greeting
    whitelist = bot.config.greeting.whitelist
    logger    = get_logger(__name__)

    if 'greeting' not in bot.memory:
        bot.memory['greeting'] = SopelMemory()


def send_greeting(bot, nick=None):
    target = ''

    if nick:
        target = nick + ': '

    bot.say(target + greeting)


@commands('greet')
def greet(bot, trigger):
    if trigger.sender not in whitelist:
        logger.info('Ignoring channel ' + trigger.sender)
        return

    nick = None
    if trigger.match.group(3) is not None:
        nick = trigger.match.group(3)

    send_greeting(bot, nick)


@event('JOIN')
@rule('.*')
def joined(bot, trigger):
    logger.info(trigger.nick + ' joined')

    if trigger.sender not in whitelist:
        logger.info('Ignoring channel ' + trigger.sender)
        return
    elif bot.nick == trigger.nick:
        logger.info('Skipping self')
        return

    uid = bot.db.get_nick_id(trigger.nick, create=True)
    jtime = time.time()

    logger.info('Adding entry for ' + trigger.nick)

    bot.memory['greeting'][uid] = jtime


@rule('.*')
def speak(bot, trigger):
    if trigger.sender not in whitelist:
        logger.info('Ignoring channel ' + trigger.sender)
        return

    ctime = time.time()
    uid = bot.db.get_nick_id(trigger.nick, create=True)

    logger.info('Checking message from ' + trigger.nick)

    if uid in bot.memory['greeting']:
        logger.info('Entry found, checking ' + trigger.nick)

        jtime = bot.memory['greeting'][uid]

        if ctime - jtime <= timeout:
            logger.info('Greeting ' + trigger.nick)

            send_greeting(bot, trigger.nick)

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
    ctime = time.time()

    logger.info('Cleanup time')

    for key, val in bot.memory['greeting'].items():
        if ctime - val > timeout:
            logger.info('Removing entry for ' + str(key))

            del bot.memory['greeting'][key]
