import datetime
import re

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
        out = "Source at https://github.com/pdxcat/tonkonbot"
        bot.msg(channel, out)

commands.append(source)

def bdlist(bot, user, channel, msg):
    if '+bd list' == msg:
        #from pdb import set_trace; set_trace()
        db = bot.factory.db.cursor()
        dumps = db.execute("SELECT * FROM main.braindumps ORDER BY date ASC")
        today = datetime.date.today()
        count = 0
        for row in dumps:
            curr = row[0].split('-')
            curr[0] = int(curr[0])
            curr[1] = int(curr[1])
            curr[2] = int(curr[2])
            # Make sure the bd being displayed has not already passed
            if (curr[0] > today.year or (curr[0] == today.year and curr[1] > today.month) or (curr[0] == today.year and curr[1] == today.month and curr[2] >= today.day)) and count < 5 :
                out = "{0} | {1}".format(row[0], row[1])
                bot.msg(channel, out)
                count = count + 1

commands.append(bdlist)

def bdlistone(bot, user, channel, msg):
    pattern = re.compile("^\+bd [0-9]{4}\-[0-9]{2}\-[0-9]{2}")
    if pattern.match(msg):

        date = msg.split(' ')[1]

        safe = (date,)

        db = bot.factory.db.cursor()
        #dumps = db.execute("SELECT * FROM main.braindumps")
        db.execute('SELECT * from main.braindumps where date=(?)', safe)
        dump = db.fetchone()
        out = "{0} | {1}".format(dump[0], dump[1])
        bot.msg(channel, out)

commands.append(bdlistone)

def bdadd(bot, user, channel, msg):
    if msg.startswith('+bd add'):
        # process input
        date = msg.split(' ')[2]

        # make sure the date is in a yyyy-mm-dd format if it isnt respond in irc
        pattern = re.compile("^[0-9]{4}\-[0-9]{2}\-[0-9]{2}")
        if user == "relsqui" or user == "squid" or user == "nibalizer":
            if pattern.match(date):
                topic = " ".join(msg.split(' ')[3:])
                #topic = " ".join(msg.split(' ')[4:])
                bot.msg(channel, "Addding {0}, {1}".format(date, topic))

                # sanitize input

                #date_s = (date,)
                safe = (date, topic)

                db = bot.factory.db.cursor()
                #dumps = db.execute("SELECT * FROM main.braindumps")
                db.execute('INSERT INTO main.braindumps VALUES (?, ?)', safe)
                bot.factory.db.commit()
            else:
                bot.msg(channel, "please input date in a 'yyyy-mm-dd' format")
        else:
            bot.msg(channel, "You are not authorized to make that change")

commands.append(bdadd)

def bdedit(bot, user, channel, msg):
    if msg.startswith('+bd edit'):
        # process input
        date = msg.split(' ')[2]

        # make sure the date is in a yyyy-mm-dd format if it isnt respond in irc
        pattern = re.compile("^[0-9]{4}\-[0-9]{2}\-[0-9]{2}")
        if user == "relsqui" or user == "squid" or user == "nibalizer":
            if pattern.match(date):
                topic = " ".join(msg.split(' ')[3:])
                #topic = " ".join(msg.split(' ')[4:])
                bot.msg(channel, "editing {0}".format(date))

                # sanitize input

                #date_s = (date,)
                #topic_s = (topic,)
                safe = (topic, date)

                db = bot.factory.db.cursor()
                #dumps = db.execute("SELECT * FROM main.braindumps")
                db.execute("UPDATE braindumps SET topic=? WHERE date=?", safe)
                bot.factory.db.commit()
            else:
                bot.msg(channel, "please input date in a 'yyyy-mm-dd' format")
        else:
            bot.msg(channel, "You are not authorized to make that change")

commands.append(bdedit)

def bdrm(bot, user, channel, msg):
    if msg.startswith('+bd rm'):
        if user == "relsqui" or user == "squid" or user == "nibalizer":
            # process input
            date = msg.split(' ')[2]

            # sanitize input
            #date_s = (date,)
            safe = (date,)

            bot.msg(channel, "Deleting " + date)
            db = bot.factory.db.cursor()
            #dumps = db.execute("SELECT * FROM main.braindumps")
            db.execute('DELETE FROM main.braindumps WHERE date=?', safe)
            bot.factory.db.commit()
        else:
            bot.msg(channel, "You are not authorized to make that change")

commands.append(bdrm)

def bdhelp(bot, user, channel, msg):
    if msg.startswith('+bd help'):
        bot.msg(channel, "This is a bot that keeps track of the braindump list, commands are \"+bd list\", \"+bd add\", \"+bd edit\", \"+bd $date\", and \"+bd rm\" ")

commands.append(bdhelp)
