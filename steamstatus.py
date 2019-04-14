from sopel.module import commands
from sopel import formatting

import requests, string

service_translations = {
	'cms': 'Steam CMs',
	'cms-ws': 'Steam WebSocket CMs',
	'community': 'Steam Community',
	'csgo': 'CS:GO Services',
	'csgo_community': 'CS:GO Player Inventories',
	'csgo_mm_scheduler': 'CS:GO Matchmaking Scheduler',
	'csgo_sessions': 'CS:GO Sessions Logon',
	# 'database': 'SteamDB Database',
	# 'dota2': 'DoTA 2 Services',
	# 'graphs': 'SteamDB Graphs',
	'online': 'Players Online',
	# 'realtime': 'SteamDB Realtime Stream',
	'steam': 'Steam',
	'store': 'Steam Store',
	# 'tf2': 'TF2 Services',
	'webapi': 'Steam Web API'
}

@commands("steam")
def main_func(bot, trigger):
    json = get_info()
    result = []
    services = {}

    for name, details in json['services'].items():
    	if name in service_translations:
            name = service_translations[name]
            status = details['status']
            title = details['title']

            if status == 'good':
                status = formatting.color(title, "GREEN")
            else:
                status = formatting.color(title, "RED")

            i = "{0:<30} {1:>30}".format(name, status)
            result.append(i)

    for line in result.sort():
    	bot.say(line)

def get_info():
    response = requests.get('https://crowbar.steamstat.us/Barney', headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'})
    return response.json()
