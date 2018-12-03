# -*- coding: utf-8 -*-

import re
from willie.module import commands, priority, OP, HALFOP


def setup(bot):
    #Having a db means pref's exists. Later, we can just use `if bot.db`.
    if bot.db and not bot.db.preferences.has_columns('topic_mask'):
        bot.db.preferences.add_columns(['topic_mask'])

def _detectservices(args):
    if args == "":
        return False
    else:
        args = args.split()
        if "-s" in args or "--services" in args:
            return True
        else:
            return False

def _op(trigger):
    channel = trigger.sender
    if trigger.group(2):
        args = trigger.group(2).replace("-s", "").replace("--services", "")
    else:
        args = ""
    if args.split() == []:
        nick = trigger.nick
        return [channel, nick]
    else:
        nick = args
        return [channel, nick]

@commands('op')
def op(bot, trigger):
    if trigger.admin:
        services = _detectservices(trigger.group(0))
        args = _op(trigger)
        if services == True:
            bot.msg('ChanServ', 'op ' + args[0] + ' ' + args[1])
        else:
            amount = ""
            for i in args[1].split():
                amount += "o"
            bot.write(('MODE', args[0] + ' +' + amount + ' ' + args[1]))
    else:
        return

@commands('deop')
def deop(bot, trigger):
    if trigger.admin:
        services = _detectservices(trigger.group(0))
        args = _op(trigger)
        if services == True:
            bot.msg('ChanServ', 'deop ' + args[0] + ' ' + args[1])
        else:
            amount = ""
            for i in args[1].split():
                amount += "o"
            bot.write(('MODE', args[0] + ' -' + amount + ' ' + args[1]))
    else:
        return

@commands('voice')
def voice(bot, trigger):
    if trigger.admin:
        services = _detectservices(trigger.group(0))
        args = _op(trigger)
        if services == True:
            bot.msg('ChanServ', 'voice ' + args[0] + ' ' + args[1])
        else:
            amount = ""
            for i in args[1].split():
                amount += "v"
            bot.write(('MODE', args[0] + ' +' + amount + ' ' + args[1]))
    else:
        return
            
@commands('devoice', 'dv')
def devoice(bot, trigger):
    if trigger.admin:
        services = _detectservices(trigger.group(0))
        args = _op(trigger)
        if services == True:
            bot.msg('ChanServ', 'devoice ' + args[0] + ' ' + args[1])
        else:
            amount = ""
            for i in args[1].split():
                amount += "v"
            bot.write(('MODE', args[0] + ' -' + amount + ' ' + args[1]))
    else:
        return


@commands('kick')
@priority('high')
def kick(bot, trigger):
    if not trigger.admin:
        return
    if bot.privileges[trigger.sender][bot.nick] < HALFOP:
            bot.reply("Lo siento no tengo op :v")
    if trigger.group(2).startswith('#'):
        bot.write(('KICK', trigger.group(2) + ' [%s]' % trigger.nick))
    else:
        bot.write(('KICK', trigger.sender + ' ' + trigger.group(2) + ' [%s]' % trigger.nick))

def configureHostMask(mask):
    if mask == '*!*@*':
        return mask
    if re.match('^[^.@!/]+$', mask) is not None:
        return '%s!*@*' % mask
    if re.match('^[^@!]+$', mask) is not None:
        return '*!*@%s' % mask

    m = re.match('^([^!@]+)@$', mask)
    if m is not None:
        return '*!%s@*' % m.group(1)

    m = re.match('^([^!@]+)@([^@!]+)$', mask)
    if m is not None:
        return '*!%s@%s' % (m.group(1), m.group(2))

    m = re.match('^([^!@]+)!(^[!@]+)@?$', mask)
    if m is not None:
        return '%s!%s@*' % (m.group(1), m.group(2))
    return ''

@commands('ban')
@priority('high')
def ban(bot, trigger):
    if not trigger.admin:
            bot.reply("Tu no tienes derecho ha hacer eso :v")        
    if bot.privileges[trigger.sender][bot.nick] < HALFOP:
            bot.reply("Lo siento, no tengo op")
    text = trigger.group().split()
    argc = len(text)
    if argc < 2:
        return
    opt = text[1]
    banmask = opt
    channel = trigger.sender
    if opt.startswith('#'):
        if argc < 3:
            return
        channel = opt
        banmask = text[2]
    banmask = configureHostMask(banmask)
    if banmask == '':
        return
    bot.write(['MODE', channel, '+b', banmask])


@commands('unban')
def unban(bot, trigger):
    if not trigger.admin:
            bot.reply("Tu no tienes derecho ha hacer eso :v")    
    if bot.privileges[trigger.sender][bot.nick] < HALFOP:
            bot.reply("Lo siento, no tengo op")
    text = trigger.group().split()
    argc = len(text)
    if argc < 2:
        return
    opt = text[1]
    banmask = opt
    channel = trigger.sender
    if opt.startswith('#'):
        if argc < 3:
            return
        channel = opt
        banmask = text[2]
    banmask = configureHostMask(banmask)
    if banmask == '':
        return
    bot.write(['MODE', channel, '-b', banmask])


@commands('quiet')
def quiet(bot, trigger):
    if not trigger.admin:
            bot.reply("Tu no tienes derecho ha hacer eso :v")    
    if bot.privileges[trigger.sender][bot.nick] < HALFOP:
            bot.reply("Lo siento, no tengo op")
    text = trigger.group().split()
    argc = len(text)
    if argc < 2:
        return
    opt = text[1]
    quietmask = opt
    channel = trigger.sender
    if opt.startswith('#'):
        if argc < 3:
            return
        channel = opt
        quietmask = text[2]
    quietmask = configureHostMask(quietmask)
    if quietmask == '':
        return
    bot.write(['MODE', channel, '+q', quietmask])


@commands('unquiet')
def unquiet(bot, trigger):
    if not trigger.admin:
            bot.reply("Tu no tienes derecho ha hacer eso :v")
    if bot.privileges[trigger.sender][bot.nick] < HALFOP:
            bot.reply("Lo siento, no tengo op")
    text = trigger.group().split()
    channel = trigger.sender
    quietmask = text[1]
    quietmask = configureHostMask(quietmask)
    if quietmask == '':
        return
    bot.write(['MODE', channel, '-q', quietmask])


@commands('kickban', 'kb')
@priority('high')
def kickban(bot, trigger):
    if not trigger.admin:
            bot.reply("Tu no tienes derecho ha hacer eso :v")        
    if bot.privileges[trigger.sender][bot.nick] < HALFOP:
            bot.reply("Lo siento, no tengo op")
    text = trigger.group().split()
    argc = len(text)
    if argc < 2:
        return
    opt = text[1]
    reason = text[2]
    banmask = opt
    channel = trigger.sender
    if opt.startswith('#'):
        if argc < 3:
            return
        channel = opt
    banmask = configureHostMask(banmask)
    if banmask == '':
        return
    bot.write(['MODE', channel, '+b', banmask])
    bot.write(['KICK', channel, opt, ' :', reason])

@commands('topic')
def topic(bot, trigger):
    purple, green, bold = '\x0306', '\x0310', '\x02'
    if not trigger.admin:
            bot.reply("Tu no tienes derecho ha hacer eso :v")        
    if bot.privileges[trigger.sender][bot.nick] < HALFOP:
            bot.reply("Lo siento, no tengo op")
    text = trigger.group(2)
    if text == '':
        return
    channel = trigger.sender.lower()

    narg = 1
    mask = None
    if bot.db and channel in bot.db.preferences:
        mask = bot.db.preferences.get(channel, 'topic_mask')
        narg = len(re.findall('%s', mask))
    if not mask or mask == '':
        mask = '%s'

    top = trigger.group(2)
    text = tuple()
    if top:
        text = tuple(unicode.split(top, '~', narg))

    if len(text) != narg:
            message = "Faltan argumentos. Me has dado " + str(len(text)) + ', pero hacen falta ' + str(narg) + '.'

            bot.say(message)
    topic = mask % text

    bot.write(['TOPIC', channel + ' :' + topic])


@commands('tmask')
def set_mask(bot, trigger):
    if bot.privileges[trigger.sender][trigger.nick] < OP:
        return
    if not bot.db:
            bot.say(u"No tengo bien configurada la base de datos y no he podido hacer esa accion.")
    else:
        bot.db.preferences.update(trigger.sender.lower(), {'topic_mask': trigger.group(2)})
        if bot.config.lang == 'es':
            bot.say("Hecho, " + trigger.nick)

@commands('showmask')
def show_mask(bot, trigger):
    if bot.privileges[trigger.sender][trigger.nick] < OP:
        return
    if not bot.db:
            bot.say(u"No tengo bien configurada la base de datos y no he podido hacer esa accion.")
    elif trigger.sender.lower() in bot.db.preferences:
        bot.say(bot.db.preferences.get(trigger.sender.lower(), 'topic_mask'))
    else:
        bot.say("%s")

@commands('moderate')
def moderat(bot, trigger):
    if trigger.admin:
        channel = trigger.sender
        bot.write(["MODE", channel, "+m"])
    else:
        bot.say(u"Ho sento, pero no")
        return
    
@commands('unmoderate')
def dmoderat(bot, trigger):
    if trigger.admin:
        channel = trigger.sender
        bot.write(["MODE", channel + " -m"])
    else:
            bot.say(u"Tu no tienes derecho ha hacer eso :v")
