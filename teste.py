# encoding: utf-8
import subprocess
import time
import random
import datetime
import telepot

occupant = [""]
address = [""]
telegram_id = [""]
flag = True
flagPonto = False
ask = False

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    
    if command == '/roll':
       bot.sendMessage(chat_id, random.randint(0,99))
    elif command == '/time':
       bot.sendMessage(chat_id, str(datetime.datetime.now()))
    if ask == True:
        if command == 'Sim' or command == 'sim' or command == '/start' or command == 'pode' or command == 'Pode':
            flagPonto = True
        else:
            bot.sendMessage(telegram_id[0], "Me avise quando então com /start")
    while flagPonto:
        print 'ponto'
        horaPonto = time.localtime().tm_hour
        minPonto = time.localtime().tm_min
        if horaPonto - horaAndre == 4 and minPonto - minAndre == 0:
            bot.sendMessage(telegram_id[0], "4 horas já")
        flagPonto = False
    
    print 'Got command: %s' % command
    print 'From: %s' % chat_id
    
bot = telepot.Bot('')
bot.message_loop(handle)
print 'I am listening ...'

while flag:
    print 'scan'
    global output
    output = subprocess.check_output("sudo arp-scan -l", shell=True)
    
    if address[0] in output:
        print 'mac'
        bot.sendMessage(telegram_id[0], "Jé vi que você chegou, posso marcar o horário?")
        horaAndre = time.localtime().tm_hour
        minAndre = time.localtime().tm_min
        flag = False
        ask = True

while 1:
    time.sleep(10)
