from sopel.modules.admin import *
from sopel.module import commands


@commands('say')
def say(bot, trigger):
	 return msg(bot, trigger)