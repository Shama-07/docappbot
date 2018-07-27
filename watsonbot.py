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
    if context==None:
        update.message.reply_text('Hello!!!  I am doc_app_bot, I can help you get the appointment from your Doctor. If you are new to the bot' 
                                  'app please press /help')
    else:
        update.message.reply_text('Sorry Server is busy!!!! try after sometime')

def help(bot, update):
    print('Received /help command')
    update.message.reply_text('Type these commands\n\nAppointment - for a new appointment.\n\nCancel Appointment - for cancelling the booked appointment.\n\nlocation - to know the the location of the hospital.\n\nlist - for the list of doctors.\n\ntimimgs - to know the timimgs of the hospital.\n\nthanks - to make a new appointment after another.\n\ncancel - to cancel the appointment in the middle.\n\n /end - to end the conversation with bot')

def end(bot,update):
    print('Received /end command')
    global context
    context = None
    update.message.reply_text('Thank You!!!! To start a new converstion do /start')
    
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
            #extract context variables
            for x in context:
                d[x]=context[x]
                print(x,d[x])
            update.message.reply_text('Let me check for the availability')
            #establishing connection with db
            try:
                conn = sqlite3.connect('appointment.db',isolation_level= None)
                c = conn.cursor()
                print('conn done')
            except:
                print('connection prob')
            print(c)
            #code
            try:
                d1='SELECT * from tbl where day="%s" and time="%s" and doctor="%s"'%(d['date'],d['time'],d['doctor'])
                print(d1)
                c.execute('SELECT * from tbl where day="%s" and time="%s" and doctor="%s"'%(d['date'],d['time'],d['doctor']))
                print('Select done')
            except:
                print('Problem in Select')
            print(c)
            try:
                flag = c.fetchall()
                c.close()
                print('Flag worked')
            except:
                print('Prob in flag')
            conn.close();
            print(flag)
            #Inserting details into database
            if not flag:
                print("Submitting ")
                update.message.reply_text('Submitting your details')
                try:
                    conn = sqlite3.connect('appointment.db',isolation_level= None)
                    c = conn.cursor()
                    print(c);
                    c.execute("INSERT INTO tbl (name,day,time,doctor,mail)"
                                       "VALUES (?,?,?,?,?)",(d['person'],d['date'],d['time'],d['doctor'],d['email']))
                    print(c)
                    conn.commit()
                    c.close()
                    update.message.reply_text('Appointment Set Successfully. Thank You!!!! To continue say done')
                    conn.close()
                    msg = 'Thank You for booking an appointment with us.\n ........................................................\nYour Appointment is set with ' + d['doctor'] +'\n Date ' + d['date']+ '\nTimings ' + d['time'] + '\nWe request you to come half an hour early'
                    #Sending confirmation mails
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
                    update.message.reply_text('Sorry!! Couldnt set an appointment say okay to continue ')

            else:
               update.message.reply_text('Cannot book an appointment at this time ,try some other time. to end this say done')
        #canceling the previously booked appointment
        if x =='confirm1' and d[x] =='yes && slot_in_focus':
            for x in context:
                d[x]=context[x]
                print(x,d[x])
            update.message.reply_text('Let me check in the database')  
            update.message.reply_text('Cancelling the appointment.....')
            try:
                conn = sqlite3.connect('appointment.db',isolation_level=None)
                c = conn.cursor()
                print(c)
                c.execute("DELETE FROM tbl WHERE day = ? and time=? and doctor=?",(d['date'],d['time'],d['doctor']))
                conn.commit()
                print('done')
                update.message.reply_text('Appointment Cancelled.Thank You!!!! To continue say done')
                conn.close()
                msg = 'Thank You. Your appointment has been cancelled.\n ........................................................\nYour Appointment was set with ' + d['doctor'] +'\n Date ' + d['date']+ '\nTimings ' + d['time'] + '\n-SSSR Hospital'
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
                update.message.reply_text("Sorry!! couldn't cancel an appointment!!! To continue say done")
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
    dp.add_handler(CommandHandler("end", end))
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
