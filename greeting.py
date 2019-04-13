from sopel.module import rule, event, interval
from sopel.tools import SopelMemory
import time


# in seconds
ttl = 90
cleanup = 1800

greeting = 'Greetings!'


def setup(bot):
    bot.memory['greetings'] = SopelMemory()


@event('JOIN')
@rule('.*')
def joined(bot, trigger):
    uid = bot.db.get_nick_id(trigger.nick, create=True)
    jtime = time.time()

    if bot.nick == trigger.nick:
        return
    else:
        bot.memory['greetings'][uid] = jtime


@rule('.*')
def speak(bot, trigger):
    uid = bot.db.get_nick_id(trigger.nick, create=True)
    ctime = time.time()

    if uid in bot.memory['greetings']:
        jtime = bot.memory['greetings'][uid]

        if ctime - jtime <= ttl:
            bot.say(greeting)

        del bot.memory['greetings'][uid]


@event('PART')
@event('QUIT')
@rule('.*')
def cleanup_events(bot, trigger):
    uid = bot.db.get_nick_id(trigger.nick, create=True)

    if uid in bot.memory['greetings']:
        del bot.memory['greetings'][uid]


@interval(cleanup)
def cleanup_interval(bot):
    ctime = time.time()

    for key, val in bot.memory['greetings'].items():
        if ctime - val > ttl:
            del bot.memory['greetings'][key]
