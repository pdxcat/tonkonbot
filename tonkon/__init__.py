#

commands = []


def command_handler(bot, user, channel, msg):
    for command in commands:
        command(bot, user, channel, msg)


def name(bot, user, channel, msg):
    if msg.startswith(bot.nickname) and 'sup' in msg.lower():
        out = "Sup I'm a bot"
        bot.msg(channel, out)
commands.append(name)



def bdlist(bot, user, channel, msg):
    if '+bd list' == msg:
        out = "2015-04-01 Web Dump with derp"
        bot.msg(channel, out)
commands.append(bdlist)
