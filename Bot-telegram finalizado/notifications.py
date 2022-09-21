# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.
import telebot
# ----------------------------------------------------------------------------------------
import json
# ----------------------------------------------------------------------------------------
import requests
from requests.auth import HTTPBasicAuth


################################################################
bot = telebot.TeleBot('5604807402:AAGjoXP_1GuJgTr9vmcvGANTpQdlj60E7HQ')
################################################################

def notificacoes(message):
    print("NOTIFICATION SENT")
# ALTERAR PARA O ID DO NUMERO QUE SERA NOTIFICADO
    bot.send_message(5491668589, message)



def ban(id):
# ALTERAR O NUMERO -1001650455571 PELO ID DO SEU GRUPO
    bot.ban_chat_member(-1001650455571, id)
def unban(id):
    print("unban")
    bot.unban_chat_member(-1001650455571, id)

# NTF PLAN ACAB
def ntf_renovacao(id):
    bot.send_message(id, 
    """Seu plano está perto de acabar. 
Caso deseje renovar digite /renovar:""")

def ntf_email(id):
    bot.send_message(id, "Email inválido!")

def ntf_att_email(id):
    bot.send_message(id, "Email atualizado!")

    
    