# coding=utf8
"""
admin.py - Willie Admin Module
Copyright 2010-2011, Sean B. Palmer (inamidst.com) and Michael Yanovich
(yanovich.net)
Copyright © 2012, Elad Alfassa, <elad@fedoraproject.org>
Copyright 2013, Ari Koivula <ari@koivu.la>

Licensed under the Eiffel Forum License 2.

http://willie.dftba.net
"""
from __future__ import unicode_literals

import willie.module


def configure(config):
    """
    | [admin] | example | purpose |
    | -------- | ------- | ------- |
    | hold_ground | False | Auto re-join on kick |
    """
    config.add_option('admin', 'hold_ground', "Auto re-join on kick")


@willie.module.commands('join')
@willie.module.priority('low')
@willie.module.example('-join #ejemplo o -join #ejemplo contraseña')
def join(bot, trigger):
    """Entra al canal especificado el bot. Solo puede ser ejecutado por un administrador del bot en mensaje privado."""
    # Can only be done in privmsg by an admin
    if not trigger.is_privmsg:
        return

    if trigger.admin:
        channel, key = trigger.group(3), trigger.group(4)
        if not channel:
            return
        elif not key:
            bot.join(channel)
        else:
            bot.join(channel, key)


@willie.module.commands('part')
@willie.module.priority('low')
@willie.module.example('-part #ejemplo')
def part(bot, trigger):
    """Sale del canal especificado. Solo puede ser ejecutado por un administrador del bot en mensaje privado."""
    # Can only be done in privmsg by an admin
    if not trigger.is_privmsg:
        return
    if not trigger.admin:
        return

    channel, _sep, part_msg = trigger.group(2).partition(' ')
    if part_msg:
        bot.part(channel, part_msg)
    else:
        bot.part(channel)


@willie.module.commands('quit')
@willie.module.priority('low')
def quit(bot, trigger):
    """Sale del servidor actual. Solo puede ser ejecutado por el propietario del bot en mensaje privado."""
    # Can only be done in privmsg by the owner
    if not trigger.is_privmsg:
        return
    if not trigger.owner:
        return

    quit_message = trigger.group(2)
    if not quit_message:
        quit_message = '[Shutdown] Solicitado por %s' % trigger.nick

    bot.quit(quit_message)


@willie.module.commands('msg')
@willie.module.priority('low')
@willie.module.example('-msg ##UnivSpace Buenos días')
def msg(bot, trigger):
    """
    Envía un mensaje al canal o usuario especificado. Solo puede ser ejecutado por un administrador del bot en mensaje privado.
    """
    if not trigger.is_privmsg:
        return
    if not trigger.admin:
        return
    if trigger.group(2) is None:
        return

    channel, _sep, message = trigger.group(2).partition(' ')
    message = message.strip()
    if not channel or not message:
        return

    bot.msg(channel, message)


@willie.module.commands('me')
@willie.module.priority('low')
def me(bot, trigger):
    """
    Envía una acción al canal especificado. Solo puede ser ejecutado por un administrador del bot en mensaje privado.
    """
    if not trigger.is_privmsg:
        return
    if not trigger.admin:
        return
    if trigger.group(2) is None:
        return

    channel, _sep, action = trigger.group(2).partition(' ')
    action = action.strip()
    if not channel or not action:
        return

    msg = '\x01ACTION %s\x01' % action
    bot.msg(channel, msg)


@willie.module.event('INVITE')
@willie.module.rule('.*')
@willie.module.priority('low')
def invite_join(bot, trigger):
    """
    Entra a un canal cuando el bot sea invitado. Solo puede ser ejecutado por un administrador del bot.
    """
    if not trigger.admin:
        return
    bot.join(trigger.args[1])


@willie.module.event('KICK')
@willie.module.rule(r'.*')
@willie.module.priority('low')
def hold_ground(bot, trigger):
    """
    This function monitors all kicks across all channels willie is in. If it
    detects that it is the one kicked it'll automatically join that channel.

    WARNING: This may not be needed and could cause problems if willie becomes
    annoying. Please use this with caution.
    """
    if bot.config.has_section('admin') and bot.config.admin.hold_ground:
        channel = trigger.sender
        if trigger.args[1] == bot.nick:
            bot.join(channel)


@willie.module.commands('mode')
@willie.module.priority('low')
def mode(bot, trigger):
    """Establece un modo de usuario al Bot. Solo puede ser ejecutado por un administrador del bot en mensaje privado."""
    if not trigger.is_privmsg:
        return
    if not trigger.admin:
        return
    mode = trigger.group(3)
    bot.write(('MODE ', bot.nick + ' ' + mode))


@willie.module.commands('set')
@willie.module.example('-set core.owner Me')
def set_config(bot, trigger):
    """Muestra y modifica parámetros del bot.
       Solo puede ser ejecutado por un administrador del bot en mensaje privado.

    Argumentos:
        arg1 - sección y opción en el formato "section.option"
        arg2 - valor

    Si no se especifica una sección se toma "core" por defecto.
    Si no se le asigna un valor, se elimina la opción.
    """
    if not trigger.is_privmsg:
        bot.reply("Solo puede ser ejecutado en un mensaje privado..")
        return
    if not trigger.admin:
        bot.reply("Tu no puedes hacer eso xD.")
        return

    # Get section and option from first argument.
    arg1 = trigger.group(3).split('.')
    if len(arg1) == 1:
        section, option = "core", arg1[0]
    elif len(arg1) == 2:
        section, option = arg1
    else:
        bot.reply("Uso: -set section.option value")
        return

    # Display current value if no value is given.
    value = trigger.group(4)
    if not value:
        if not bot.config.has_option(section, option):
            bot.reply("La opción %s.%s no existe." % (section, option))
            return
        # Except if the option looks like a password. Censor those to stop them
        # from being put on log files.
        if option.endswith("password") or option.endswith("pass"):
            value = "(contraseña censurada)"
        else:
            value = getattr(getattr(bot.config, section), option)
        bot.reply("%s.%s = %s" % (section, option, value))
        return

    # Otherwise, set the value to one given as argument 2.
    setattr(getattr(bot.config, section), option, value)


@willie.module.commands('save')
@willie.module.example('-save')
def save_config(bot, trigger):
    """Guarda el estado de la configuración de DreamBot en el archivo de configuración."""
    if not trigger.is_privmsg:
        return
    if not trigger.admin:
        return
    bot.config.save()
