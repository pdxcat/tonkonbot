import datetime
import re
import requests

commands = []
bd_source = "http://web.cecs.pdx.edu/~mwilliam/braindumps"

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
    if '+source' == msg or msg.startswith(bot.nickname + ": source") or\
        msg.startswith(bot.nickname + " source") or '!source' == msg :
        out = "Source at https://github.com/pdxcat/tonkonbot"
        bot.msg(channel, out)

commands.append(source)

# list 5 braindumps that have not already passsed
def bdlist(bot, user, channel, msg):
    if re.match("^(\+|!)bd( list)?( -a)?$", msg):
        r = requests.get(bd_source)
        count = 0

        if "-a" in msg:
            max_bds = 5
        else:
            max_bds = 1

        for line in r.text.split('\n')[::-1]:
            if '|' not in line or not re.match("^[0-9]{4}-[0-9]{2}-[0-9]{2}", line):
                continue
            date = line.split('|')[0]
            date_obj = datetime.datetime.strptime(date, "%Y-%m-%d ")
            now = datetime.datetime.now()
            if date_obj.year > now.year or (date_obj.year == now.year and
                    date_obj.month > now.month) or (date_obj.year == now.year and
                    date_obj.month == now.month and date_obj.day >= now.day):
                count += 1
                bot.msg(channel, line.encode('ascii'))
                if count == max_bds:
                    break

commands.append(bdlist)

def bddate(bot, user, channel, msg):
    if re.match("^(\+)?!?bd [0-9]{4}-[0-9]{2}-[0-9]{2}$", msg):
        r = requests.get(bd_source)

        requested_date = msg.split(' ')[1]

        for line in r.text.split('\n')[::-1]:
            if '|' not in line or not re.match("^[0-9]{4}-[0-9]{2}-[0-9]{2}", line):
                continue

            date = line.split('|')[0].split(' ')[0]
            if requested_date == date:
                bot.msg(channel, line.encode('ascii'))
                break

commands.append(bddate)

# Provide help if the user asks for it
def bdhelp(bot, user, channel, msg):
    if msg.startswith('+bd help') or msg.startswith(bot.nickname + ": help") or\
        msg.startswith(bot.nickname + " help")  or msg.startswith('!bd help'):
        bot.msg(channel, "This is a bot that keeps track of the braindump list, commands are \"+bd list [-a]\" and \"+bd $date\"")

commands.append(bdhelp)
