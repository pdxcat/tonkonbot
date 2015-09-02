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

# list the bd that is asked for by date
def bdlistone(bot, user, channel, msg):
    pattern = re.compile("^\+bd [0-9]{4}\-[0-9]{2}\-[0-9]{2}")
    
    # if the msg matches the pattern then find the braindump that matches the date
    if pattern.match(msg):

        # extract the date from the msg
        date = msg.split(' ')[1]

        # sanitize input
        safe = (date,)

        # get the bd that matches the date
        db = bot.factory.db.cursor()
        db.execute('SELECT * from main.braindumps where date=(?)', safe)
        dump = db.fetchone()

        # make sure the bd exists before trying to display
        if dump:
            out = "{0} | {1}".format(dump[0], dump[1])
            bot.msg(channel, out)
        else:
            bot.msg(channel, "No bd matches that date")

commands.append(bdlistone)

def bdadd(bot, user, channel, msg):
    if msg.startswith('+bd add'):
        # process input
        date = msg.split(' ')[2]

        # make sure the date is in a yyyy-mm-dd format if it isnt respond in irc
        pattern = re.compile("^[0-9]{4}\-[0-9]{2}\-[0-9]{2}")

        # make sure the user trying to add a bd is allowed to
        if user == "relsqui" or user == "squid" or user == "nibalizer":
            if pattern.match(date):

                # extract the topic from the msg
                topic = " ".join(msg.split(' ')[3:])
                bot.msg(channel, "Addding {0}, {1}".format(date, topic))

                # sanitize input
                safe = (date, topic)

                # Add a bd with the date and topic specified
                db = bot.factory.db.cursor()
                db.execute('INSERT INTO main.braindumps VALUES (?, ?)', safe)
                bot.factory.db.commit()

            # if the date isnt in the right format, tell the user
            else:
                bot.msg(channel, "please input date in a 'yyyy-mm-dd' format")

        # if the user is not allowed to make the change tell them
        else:
            bot.msg(channel, "You are not authorized to make that change")

commands.append(bdadd)

def bdedit(bot, user, channel, msg):
    if msg.startswith('+bd edit'):
        # process input
        date = msg.split(' ')[2]

        # make sure the date is in a yyyy-mm-dd format if it isnt respond in irc
        pattern = re.compile("^[0-9]{4}\-[0-9]{2}\-[0-9]{2}")

        # make sure the user is allowed to make an edit
        if user == "relsqui" or user == "squid" or user == "nibalizer":
            if pattern.match(date):

                # cut the topic out of the message
                topic = " ".join(msg.split(' ')[3:])
                bot.msg(channel, "editing {0}".format(date))

                # sanitize input to prevent SQL injection
                safe = (topic, date)

                # update the bd that matches the date with the new topic
                db = bot.factory.db.cursor()
                db.execute("UPDATE braindumps SET topic=? WHERE date=?", safe)
                bot.factory.db.commit()

            # if the date is not in a "yyyy-mm-dd" format inform the user that that is required
            else:
                bot.msg(channel, "please input date in a 'yyyy-mm-dd' format")

        # if the user is not allowed to make a change tell them
        else:
            bot.msg(channel, "You are not authorized to make that change")

commands.append(bdedit)

def bdrm(bot, user, channel, msg):
    if msg.startswith('+bd rm'):
        
        # make sure the user is allowed to remove a bd from the db
        if user == "relsqui" or user == "squid" or user == "nibalizer":
            # process input
            date = msg.split(' ')[2]

            # sanitize input
            safe = (date,)

            bot.msg(channel, "Deleting " + date)

            # delete the entry that matches the date provided
            db = bot.factory.db.cursor()
            db.execute('DELETE FROM main.braindumps WHERE date=?', safe)
            bot.factory.db.commit()

        # if the user is not allowed to remove a bd tell them
        else:
            bot.msg(channel, "You are not authorized to make that change")

commands.append(bdrm)

# Provide help if the user asks for it
def bdhelp(bot, user, channel, msg):
    if msg.startswith('+bd help') or msg.startswith(bot.nickname + ": help") or msg.startswith(bot.nickname + " help"):
        bot.msg(channel, "This is a bot that keeps track of the braindump list, commands are \"+bd list\", \"+bd add\", \"+bd edit\", \"+bd $date\", and \"+bd rm\" ")

commands.append(bdhelp)
