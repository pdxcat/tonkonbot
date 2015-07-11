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
        #from pdb import set_trace; set_trace()
        db = bot.factory.db.cursor()
        dumps = db.execute("SELECT * FROM main.braindumps")
        for row in dumps:
            out = "{0} | {1} | {2}".format(row[0], row[1], row[2])
            bot.msg(channel, out)
commands.append(bdlist)
