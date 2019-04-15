from sopel.config.types import StaticSection, ListAttribute
from sopel.module import commands
from sopel import formatting
import requests, string, os, json


class SteamStatusSection(StaticSection):
    blacklist = ListAttribute('blacklist')


def configure(config):
    config.define_section('steamstatus', SteamStatusSection, validate=False)

    config.steamstatus.configure_setting('blacklist', 'Services not to print')


def setup(bot):
    global blacklist, service_translations

    bot.config.define_section('steamstatus', SteamStatusSection)

    blacklist = bot.config.steamstatus.blacklist

    service_translations = json.load(open(os.path.dirname(os.path.realpath(__file__)) + '/data/steamstatus'))


@commands("steam")
def status(bot, trigger):
    global blacklist, service_translations

    json = get_info()
    result = []
    services = {}

    for name, details in json['services'].items():
        if name not in blacklist and name in service_translations:
            name = service_translations[name]
            status = details['status']
            title = details['title']

            if status == 'good':
                status = formatting.color(title, "GREEN")
            else:
                status = formatting.color(title, "RED")

            i = "{0:<30} {1:>30}".format(name, status)
            result.append(i)

    result.sort()

    for line in result:
    	bot.say(line)


def get_info():
    response = requests.get('https://crowbar.steamstat.us/Barney', headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'})

    return response.json()
