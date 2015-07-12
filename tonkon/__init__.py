#
import datetime

commands = []


def command_handler(bot, user, channel, msg):
    for command in commands:
        command(bot, user, channel, msg)


def name(bot, user, channel, msg):
    if msg.startswith(bot.nickname) and 'sup' in msg.lower():
        out = "Sup I'm a bot"
        bot.msg(channel, out)
commands.append(name)

def source(bot, user, channel, msg):
    if '+source' == msg:
        out = "Source at https://github.com/nibalizer/tonkonbot"
        bot.msg(channel, out)
commands.append(source)


def bdlist(bot, user, channel, msg):
    if '+bd list' == msg:
        #from pdb import set_trace; set_trace()
        db = bot.factory.db.cursor()
        dumps = db.execute("SELECT * FROM main.braindumps")
        for row in dumps:
            out = "{0} | {1} | {2}".format(row[0], row[1], row[2])
            bot.msg(channel, out)
commands.append(bdlist)

def bdadd(bot, user, channel, msg):
    if msg.startswith('+bd add'):
        # process input
        date = msg.split(' ')[2]
        dumper  = msg.split(' ')[3]
        topic = " ".join(msg.split(' ')[3:])
        bot.msg(channel, "Addding {0}, {1}, {2}".format(date, dumper, topic))

        # sanitize input

        #date_s = (date,)
        safe = (date, dumper, topic)

        db = bot.factory.db.cursor()
        #dumps = db.execute("SELECT * FROM main.braindumps")
        db.execute('INSERT INTO main.braindumps VALUES (?, ?, ?)', safe)
        bot.factory.db.commit()

commands.append(bdadd)

def bdrm(bot, user, channel, msg):
    if msg.startswith('+bd rm'):
        # process input
        date = msg.split(' ')[2]

        # sanitize input
        #date_s = (date,)
        safe = (date,)

        db = bot.factory.db.cursor()
        #dumps = db.execute("SELECT * FROM main.braindumps")
        db.execute('DELETE FROM main.braindumps WHERE date=?', safe)
        bot.factory.db.commit()

commands.append(bdrm)
