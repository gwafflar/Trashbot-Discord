"""
This is a basic discord bot that notifies everyone in the kolok when it's the day
we have to take out the garbage.
This way, we avoid bad smells do to oversight and everyone is happy.

@author : Guillaume Wafflard
Date : 13/09/2021

Licence : Open Source/ GNU (seriously, if anyone ever use this bot, just tell me I'd be happy)
"""

import datetime
import time
from discord.ext import commands, tasks

TOKEN = ''
channelIdKoloK = 0 #channelID where to send notifications
channelIdTraining = 0  #channelID server to get notification from the bot, without spamming the kolok server
TRASH_DAYS = [1, 4] #Mardi et Vendredi
DAYS_IN_WEEK = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
#the task starts at 7:00p.m and run every 24 hours
NOTIFICATION_TIME = datetime.timedelta(0, 0, 0, 0 , 0, 18, 0)# class datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)¶
bot = commands.Bot("!")


@bot.event
async def on_ready():
    print('Connecté en tant que {0.user}'.format(bot))
    channel = bot.get_channel(channelIdTraining)
    await channel.send("Bonjour, je suis Trashbot")
    waitUntil7pm()
    warnIfTrashDay.start()


@tasks.loop(hours=24)
async def warnIfTrashDay() :
    if isTrashDay() :
        channel = bot.get_channel(channelIdKolok)
        await channel.send("@everyone, c'est le jour de sortir les poubelles !")
    else :
        channel = bot.get_channel(channelIdTraining)
        await channel.send("Ce n'est pas le jour de sortir les poubelles")


def isTrashDay() :
    today=datetime.date.today()
    weekday=today.weekday()
    print("Aujourd'hui est " + DAYS_IN_WEEK[weekday])
    if weekday in TRASH_DAYS :
        print("C'est le jour de sortir les poubelles !")
        return True
    else :
        print("Ce n'est pas le jour de sortir les poubelles")
        return False
    #return weekday in TRASH_DAY

def waitUntil7pm() :
    now = datetime.datetime.now().time()
    now = datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second)
    print("Il est " + str(now))
    print("Heure de notification " + str(NOTIFICATION_TIME))
    if (now<NOTIFICATION_TIME) :
        pause=NOTIFICATION_TIME-now
        print("Démarrage dans " + str(pause))
        time.sleep(pause.total_seconds())
        
bot.run(TOKEN)
