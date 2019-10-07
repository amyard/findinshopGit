#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.

import telegram
from telegram import Emoji
from telegram.ext import Updater

import urllib
import urllib, json
import logging

import re, urlparse

def urlEncodeNonAscii(b):
    return re.sub('[\x80-\xFF]', lambda c: '%%%02x' % ord(c.group(0)), b)

def iriToUri(iri):
    parts= urlparse.urlparse(iri)
    return urlparse.urlunparse(
        part.encode('idna') if parti==1 else urlEncodeNonAscii(part.encode('utf-8'))
        for parti, part in enumerate(parts)
    )

# Enable logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi!')


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='Ублюдок, мать твою, а ну иди сюда, говно собачье! Что, решил ко мне лезть?! Ты, засранец вонючий, мать твою, а? Ну, иди сюда,﻿ попробуй меня трахнуть, я тебя сам трахну, ублюдок, онанист чертов, будь ты проклят! Иди, идиот, трахать тебя и всю твою семью, говно собачье, жлоб вонючий, дерьмо, сука, падла! Иди сюда, мерзавец, негодяй, гад, иди сюда, ты, говно, ЖОПА!')

def echo(bot, update):
    bot.sendMessage(update.message.chat_id, text=update.message.text)

def find(bot, update):
    query = update.message.text[6:]
    query = iriToUri(query)
    url = 'http://find.artel7.com/asearch/?term=%s' % query
    print url
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    if data:
        response = ''
        for x in data:
            response += '<a href="http://find.artel7.com/bid/transition/%s/">%s</a>' % (x[u'id'], '\n %s' % x[u'value:'])
        bot.sendMessage(update.message.chat_id, text=response, parse_mode=telegram.ParseMode.HTML)

    else:
        bot.sendMessage(update.message.chat_id, text="Oops "+Emoji.DISAPPOINTED_FACE)

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("191715524:AAEfqYeIeuuX6R0f2rjS82OcDNB-1KPDTIg")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.addTelegramCommandHandler("start", start)
    dp.addTelegramCommandHandler("help", help)
    dp.addTelegramCommandHandler("find", find)


    # on noncommand i.e message - echo the message on Telegram
#    dp.addTelegramMessageHandler(echo)

    # log all errors
    dp.addErrorHandler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
