# coding=utf8
"""
ping.py - Willie Ping Module
Author: Sean B. Palmer, inamidst.com
About: http://willie.dftba.net
"""
from __future__ import unicode_literals

import random
from willie.module import rule, priority, thread, commands


@rule(r'(?i)(hi|hello|hey|hola|buenas|hey)[,]? $nickname[ \t]*$')
def hello(bot, trigger):
    if trigger.owner:
        greeting = random.choice(('No sé quien eres', 'No me has programado bien, error 404', 'Tú no me amas, me cambiaste por Trivial-Bot'))
    else:
        greeting = random.choice(('Hola', 'Hey', 'Buenas'))
    punctuation = random.choice(('', '!'))
    bot.say(greeting + ' ' + trigger.nick + punctuation)


@rule('$nickname!')
@priority('high')
@thread(False)
def interjection(bot, trigger):
    bot.say(trigger.nick + '!')

@commands('ping')
def pong(bot, trigger):
    bot.say(trigger.nick + ': pong')

@commands('acerca')
def pong(bot, trigger):
    bot.say(trigger.nick + ': Soy un bot irc llamado UnivBot mi web es: http://univspace.tk/')


@commands('panconmortadela')
def mortadela(bot, trigger):
    bot.say(trigger.nick + ': es lo mas rico del mundo 7w7')
