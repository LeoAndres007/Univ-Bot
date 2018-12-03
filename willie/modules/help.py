# coding=utf8
"""
help.py - Willie Help Module
Copyright 2008, Sean B. Palmer, inamidst.com
Copyright © 2013, Elad Alfassa, <elad@fedoraproject.org>
Copyright 2014, Miguel Peláez, <miguel2706@outlook.com>
Licensed under the Eiffel Forum License 2.
"""
from __future__ import unicode_literals

from willie.module import commands, rule, example, priority
from willie.tools import iterkeys


def setup(bot=None):
    if not bot:
        return

    if bot.config.has_option('help', 'threshold') and not bot.config.help.threshold.isdecimal():#non-negative integer
        from willie.config import ConfigurationError
        raise ConfigurationError("Attribute threshold of section [help] must be a nonnegative integer")

@rule('$nick' '(?i)(help|doc|ayuda) +([A-Za-z]+)(?:\?+)?$')
@example('-help part')
@commands('help', 'ayuda')
@priority('low')
def help(bot, trigger):
    """Muestra la documentación de un comando, e información adicional de este."""
    if not trigger.group(2):
        bot.reply('Hola soy un bot de version UnivBot 1.0 :) Puedes ver mis comandos escribiendo -comandos')
    else:
        name = trigger.group(2)
        name = name.lower()
        
        if bot.config.has_option('help', 'threshold'):
            threshold=int(bot.config.help.threshold)
        else:
            threshold=3
        
        if name in bot.doc:
            if len(bot.doc[name][0]) + (1 if bot.doc[name][1] else 0) > threshold:
                if trigger.nick != trigger.sender: #don't say that if asked in private
                    bot.reply('La documentación de ese comando es muy larga; Te lo envio en un mensaje privdo para no molestar a los usuarios.')
                msgfun=lambda l: bot.msg(trigger.nick,l)
            else:
                msgfun=bot.reply

            for line in bot.doc[name][0]:
                msgfun(line)
            if bot.doc[name][1]:
                msgfun('e.g. ' + bot.doc[name][1])
        else:
            bot.reply('No se ha encontrado el comando introducido.')

@commands('comandos')
@priority('low')
def commands(bot, trigger):
    """Devuelve una lista de comandos"""
    names = ', '.join(sorted(iterkeys(bot.doc)))
    if not trigger.is_privmsg:
        bot.reply("Los Comandos Estan En Este wiki: https://github.com/Leandro2243/UnivBot/wiki")
