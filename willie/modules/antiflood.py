# coding=utf8
from __future__ import unicode_literals

from willie.module import commands, priority, OP, HALFOP, rule
from willie.formatting import bold, color, colors
from willie import tools
import time

@rule('.*')
def is_flooding(bot, trigger):
    try:
        channel = trigger.sender
        user = trigger.nick
        
        try:
            bot.memory['antiflood']
        except KeyError:
            bot.memory['antiflood'] = {}
        try:
            bot.memory['antiflood'][channel]
        except KeyError:
            bot.memory['antiflood'][channel] = {}
        try:
            bot.memory['antiflood'][channel]['users']
        except KeyError:
            bot.memory['antiflood'][channel]['users'] = {}
        try:
            bot.memory['antiflood'][channel]['enabled']
        except KeyError:
            bot.memory['antiflood'][channel]['enabled'] = False
            
        if bot.memory['antiflood'][channel]['enabled']:
            try:
                bot.memory['antiflood'][channel]['users'][user]
            except KeyError:
                bot.memory['antiflood'][channel]['users'][user] = {}
            user_data = bot.memory['antiflood'][channel]['users'][user]
            if bot.privileges[trigger.sender][trigger.nick] > OP:
                return
            user_data['live'] = True
            try:
                user_data['msgcount']
            except KeyError:
                user_data['msgcount'] = 0
            user_data['msgcount'] += 1
            try:
                user_data['firstmsg']
            except KeyError:
                user_data['firstmsg'] = time.time()
            if user_data['firstmsg'] == None:
                user_data['firstmsg'] = time.time()
            if (time.time() - user_data['firstmsg']) > bot.memory['antiflood'][channel]['sec']:
                if user_data['msgcount'] > bot.memory['antiflood'][channel]['max']:
                    floodkick(channel, user, bot)
                    bot.reply("Por hacer {0} mensajes en {1}".format(user_data['msgcount'], (time.time() - user_data['firstmsg'])))
                user_data['firstmsg'] = None
                user_data['msgcount'] = 0
            bot.memory['antiflood'][channel]['users'][user] = user_data
            
    except Exception as e:
        print "{error}: {msg}".format(error=type(e), msg=e)

def floodkick(channel, nick, bot):
    print "Debería ser kickeado " + nick
    
@commands('antiflood')
def EnableFlood(bot, trigger):
    channel = trigger.sender
    try:
            bot.memory['antiflood']
    except KeyError:
            bot.memory['antiflood'] = {}
    try:
            bot.memory['antiflood'][channel]
    except KeyError:
            bot.memory['antiflood'][channel] = {}
    
    if bot.privileges[trigger.sender][trigger.nick] < OP:
        return bot.reply('No eres un operador de este canal en este momento.')
    if not trigger.group(2):
        return bot.reply('Debes indicar si encender o apagar el antiflood con "on" u "off"')
    enable = trigger.group(2).split(' ')
    if enable[0] == 'on' or enable[0] == 'true':
        bot.memory['antiflood'][channel]['enabled'] = True
        if enable.count < 2:
            bot.memory['antiflood'][channel]['sec'] = float(enable[1])
        else:
            bot.memory['antiflood'][channel]['sec'] = 5.0
        if enable.count < 3:
            bot.memory['antiflood'][channel]['max'] = float(enable[2])
        else:
            bot.memory['antiflood'][channel]['max'] = 4.0
    else:
        bot.memory['antiflood'][channel]['enabled'] = False
