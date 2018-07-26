from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
from watson_developer_cloud import ConversationV1
import json
import sqlite3
import smtplib

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
    inp = response['input']
    #extract context variables
    for x in context:
        d[x]=context[x]
        print(x,d[x])
        if x =='confirm' and d[x] =='yes && slot_in_focus':
            update.message.reply_text('Let me check for the availability')
            conn = sqlite3.connect('appointment.db',isolation_level= None)
            c = conn.cursor()
            print(c)
            c.execute("SELECT * from tbl where day=? and time=? and doctor=?",(d['date'],d['time'],d['doctor']))
            print(c)
            flag = c.fetchall()
            conn.close();
            print(flag)
            if not flag:
                print("Submitting ")
                update.message.reply_text('Submitting your details')
                try:
                    conn = sqlite3.connect('appointment.db',isolation_level= None)
                    c = conn.cursor()
                    print(c);
                    c.execute("INSERT INTO tbl (name,day,time,doctor,mail)"
                                       "VALUES (?,?,?,?,?)",(d['person'],d['date'],d['time'],d['doctor'],d['email']))
                    conn.commit()
                    update.message.reply_text('Appointment Set Successfully. Thank You')
                    conn.close()
                    msg = 'Thank You for booking an appointment with us.\n ........................................................\nYour Appointment is set with ' + d['doctor'] +'\n DATE ' + d['date']+ '\nTimings ' + d['time'] + '\nWe request you to come half an hour early'
                    try:
                        ml = smtplib.SMTP('smtp.gmail.com',587)
                        ml.ehlo()
                        ml.starttls()
                        ml.login('docappbot@gmail.com','abcdef_1')
                        ml.sendmail('docappbot@gmail.com',d['email'],msg)
                        ml.close()
                        update.message.reply_text("Confirmation Mail Has Been Sent")
                    except:
                        print("couldn't send")
                except:
                    update.message.reply_text('Sorry!! Couldnt set an appointment say thanks and continue ')

            else:
               update.message.reply_text('Cannot book an appointment at this time ,try some other time. to end this say thanks')
               conn.close() 
        if x =='confirm1' and d[x] =='yes && slot_in_focus':
            update.message.reply_text('Let me check in the database')  
            update.message.reply_text('Cancelling the appointment.....')
            try:
                conn = sqlite3.connect('appointment.db',isolation_level=None)
                c = conn.cursor()
                print(c)
                c.execute("DELETE FROM tbl WHERE day = ? and time=? and doctor=?",(d['date'],d['time'],d['doctor']))
                conn.commit()
                print('done')
                update.message.reply_text('Appointment Cancelled.Thank You')
                conn.close()
     
            except:
                update.message.reply_text("Sorry!! couldn't cancel an appointment")
    # build response
    resp = ''
    for text in response['output']['text']:
        resp += text
        resp += "\n"
    update.message.reply_text(resp)
    
def main():
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
