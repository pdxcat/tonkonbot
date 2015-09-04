import datetime
import re
import requests

commands = []

# Loop through all of the commands the bot has
def command_handler(bot, user, channel, msg):
    for command in commands:
        command(bot, user, channel, msg)

# if the user says "^$nick.*sup.*" reply with "Sup I'm a bot"
def name(bot, user, channel, msg):
    if msg.startswith(bot.nickname) and 'sup' in msg.lower():
        out = "Sup I'm a bot"
        bot.msg(channel, out)

commands.append(name)

# if the bot's source is asked for reply with a link to the github repo
def source(bot, user, channel, msg):
    if '+source' == msg or msg.startswith(bot.nickname + ": source") or msg.startswith(bot.nickname + " source"):
        out = "Source at https://github.com/pdxcat/tonkonbot"
        bot.msg(channel, out)

commands.append(source)

# list 5 braindumps that have not already passsed
def bdlist(bot, user, channel, msg):
    if msg.startswith("+bd list") or msg.startswith("+bd"):
        r = requests.get("http://web.cecs.pdx.edu/~finnre/braindumps")
        count = 0

        if "-a" in msg:
            max_bds = 5
        else:
            max_bds = 1

        for line in r.text.split('\n')[::-1]:
            if '|' not in line:
                continue
            date = line.split('|')[0]
            date_obj = datetime.datetime.strptime(date, "%Y-%m-%d ")
            now = datetime.datetime.now()
            if date_obj.year >= now.year and date_obj.month >= now.month and date_obj.day >= now.day:
                count += 1
                bot.msg(channel, line.encode('ascii'))
                if count == max_bds:
                    break

commands.append(bdlist)

# Provide help if the user asks for it
def bdhelp(bot, user, channel, msg):
    if msg.startswith('+bd help') or msg.startswith(bot.nickname + ": help") or msg.startswith(bot.nickname + " help"):
        bot.msg(channel, "This is a bot that keeps track of the braindump list, commands are \"+bd list\", \"+bd add\", \"+bd edit\", \"+bd $date\", and \"+bd rm\" ")

commands.append(bdhelp)
