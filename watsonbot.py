from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
from watson_developer_cloud import ConversationV1
import json
import sqlite3

context = None
# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    print('Received /start command')
    update.message.reply_text('Hello!!!  I am doc_app_bot, I can help you get the appointment from your Doctor. If you are new to the bot app' 
                              'please press /help')

def help(bot, update):
    print('Received /help command')
    update.message.reply_text('Help!')


def message(bot, update):
    print('Received an update')
    global context
    d = {'name':'user'}
    conversation = ConversationV1(username='a6ebe755-b6a0-48ed-9f1c-350eb5af1051',  # TODO
                                  password='eBKmWayG1Lm0',  # TODO
                                  version='2018-02-16')

    # get response from watson
    response = conversation.message(
        workspace_id='2b6995b3-5f59-4cc7-ad14-bf5a515c9c30',  # TODO
        input={'text': update.message.text},
        context=context)
    #print(json.dumps(response, indent=2))
    context = response['context']
    #extract context variables
    for x in context:
        d[x]=context[x]
        print(x,d[x])
        if x =='confirm' and d[x] =='yes && slot_in_focus':
            update.message.reply_text('Let me check for the availability')
            conn = sqlite3.connect('schedule')
            c = conn.cursor()
            print(c)
            c.execute("SELECT * from tbl1 where time = ?",(d['time'],))
            flag = c.fetchall()
            print(flag)
            if not flag:
                c.execute("INSERT INTO tbl1 (name,day,time,mail)"
                                   "VALUES (?,?,?,?)", (d['name'],d['date'],d['time'],d['email']))
                update.message.reply_text('Appointment Set Successfully')
                conn.commit()
                conn.close() 
            else:
               update.message.reply_text('Cannot book an appointment at this time ,try some other time. to end this say thanks')
               conn.close()       
    # build response
    resp = ''
    for text in response['output']['text']:
        resp += text

    update.message.reply_text(resp)
    
def main():
    #connection with db
    conn = sqlite3.connect('schedule')
    # Create the Updater and pass it your bot's token.
    updater = Updater('631450108:AAHis_hEDLSAWpKy7UiZEoUcyKBpJR4O5DE')  # TODO

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, message))
    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
    conn.close()

if __name__ == '__main__':
    main()
