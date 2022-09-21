# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.
from ast import Pass
from time import sleep, time
import datetime
import asyncio
from requests.auth import HTTPBasicAuth
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.async_telebot import AsyncTeleBot
import mysql.connector

import notifications
import session
import pix


import re 
################################################################
bot = AsyncTeleBot('5604807402:AAGjoXP_1GuJgTr9vmcvGANTpQdlj60E7HQ')

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
################################################################
id_grupo=""
id_nome_g=""
valor_plano=""
descricao=""

#--------------------------INICIO--------------------------#
def verify(mensagem):

    id= mensagem.chat.id
    print(mensagem)
    # veridica renovacao
    session.ntf_client()
    consulta_p= session.session_id(id)

# ALTERAR O NUMERO -1001650455571 PELO ID DO SEU GRUPO
    if id == -1001650455571:
        print("UPDATE CLIENT STATUS IN THE GROUP")
        # verifica inadimplente
        session.update_client()

    else:
        # verifica sessao ativa por tempo ou cria nova sessao
        start_session(id)
        consulta_a= session.session_id(id)
        # print("Aberta:"+ str(consulta_a[2]))
        if consulta_a[2] == "0":
            session.update_a(id,consulta_a[2])
            return True
        if consulta_a[2] == "1" and consulta_p[1]>17:
            return True
        return False

@bot.message_handler(commands=["mudaplano"])
async def renew_query(message):
    status = verify(message)
    id = message.chat.id
    if status==True:
        session.update_p(id,20)
        await bot.send_message(id, "Digite o ID do grupo que deseja alterar.")
    
def check_plano(mensagem):
    id= mensagem.chat.id

    consulta_p= session.session_id(id)
    #check email
    verifsess = session.query_session(id)
    print(verifsess)
    if verifsess==False:
        return False
    if consulta_p == None :
        return False 
    if consulta_p[1] == 21 :
        return True

    return False

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=check_plano)
async def echo_message(message):
    global id_grupo
    id = message.chat.id
    consulta_p = session.session_id(id)

    if (consulta_p[1]==21):
        session.update_p(id,consulta_p[1])
        id_grupo= message.text
        await bot.send_message(id, "Digite o ID_nome do plano.")

def check_plano2(mensagem):
    id= mensagem.chat.id

    consulta_p= session.session_id(id)
    #check email
    verifsess = session.query_session(id)
    print(verifsess)
    if verifsess==False:
        return False
    if consulta_p == None :
        return False 
    if consulta_p[1] == 22 :
        return True

    return False

@bot.message_handler(func=check_plano2)
async def echo_message(message):
    global id_nome_g
    id = message.chat.id
    consulta_p = session.session_id(id)

    if (consulta_p[1]==22):
        session.update_p(id,consulta_p[1])
        id_nome_g= message.text
        await bot.send_message(id, "Digite o novo valor.")

def check_plano3(mensagem):
    id= mensagem.chat.id

    consulta_p= session.session_id(id)
    #check email
    verifsess = session.query_session(id)
    print(verifsess)
    if verifsess==False:
        return False
    if consulta_p == None :
        return False 
    if consulta_p[1] == 23 :
        return True

    return False

@bot.message_handler(func=check_plano3)
async def echo_message(message):
    global valor_plano
    id = message.chat.id
    consulta_p = session.session_id(id)

    if (consulta_p[1]==23):
        session.update_p(id,consulta_p[1])
        valor_plano= message.text
        await bot.send_message(id, "Digite a nova descrição.")

def check_plano4(mensagem):
    id= mensagem.chat.id

    consulta_p= session.session_id(id)
    #check email
    verifsess = session.query_session(id)
    print(verifsess)
    if verifsess==False:
        return False
    if consulta_p == None :
        return False 
    if consulta_p[1] == 24 :
        return True

    return False

@bot.message_handler(func=check_plano4)
async def echo_message(message):
    global valor_plano
    global id_nome_g
    global descricao
    global id_grupo
    id = message.chat.id
    consulta_p = session.session_id(id)

    if (consulta_p[1]==24):
        session.update_p(id,0)
        descricao= message.text
        session.update_plano(valor_plano, descricao, id_grupo,id_nome_g)
        await bot.send_message(id, "Alterado com sucesso.")




#####################################
@bot.message_handler(commands=["comandos"])
async def renew_query(message):
    id = message.chat.id
    session.update_p(id,-1)
    await bot.send_message(id, """ 
/reset - reiniciar a sessão
/renovar - renovar plano
/mudaemail - altera email
/acesso - novo link de acesso ao grupo
""")

@bot.message_handler(commands=["reset"])
async def renew_query(message):
    id = message.chat.id
    session.update_p(id,-1)
    await bot.send_message(id, "Sessão reiniciada.")

@bot.message_handler(commands=["renovar"])
async def renew_query(message):
    id = message.chat.id
    grupo = session.query_client_id_g(id)
    await bot.send_message(id, "PLANOS", reply_markup=gen_markup(grupo))

@bot.message_handler(commands=["mudaemail"])
async def renew_query(message):
    id = message.chat.id
    session.update_a(id,"0")
    session.update_p(id,15)
    await bot.send_message(id, "Digite um novo email para alterar.")

@bot.message_handler(commands=["acesso"])
async def renew_query(message):
    id = message.chat.id
# ALTERAR O NUMERO -1001650455571 PELO ID DO SEU GRUPO
    invite = await bot.create_chat_invite_link(-1001650455571, member_limit=1, expire_date=int(time())+45) #Here, the link will auto-expire in 45 seconds
    InviteLink = invite.invite_link #Get the actual invite link from 'invite' class
            
    mrkplink = InlineKeyboardMarkup() #Created Inline Keyboard Markup
    mrkplink.add(InlineKeyboardButton("Entrar no grupo 🚀", url=InviteLink)) #Added Invite Link to Inline Keyboard

    await bot.send_message(id, "SHOWW! Agora só falta você entrar no grupo.", reply_markup=mrkplink)



@bot.message_handler(func=verify)
async def echo_message(message):
    id = message.chat.id
    print("--")

    consulta_p = session.session_id(id)
    if(consulta_p[1]==0):
        text = """ 
Olá, seja bem vindo(a)!
Antes de prosseguir, vamos apenas confirmar seus dados.
Qual seu nome?"""
        await bot.send_message(id, text)
        session.update_p(id,consulta_p[1])
        


#--------------------------name--------------------------#
def verify_name(mensagem):
    print("VERIFYING NAME...")
    print("---")

    name_client = mensagem.text
    id=mensagem.chat.id

    consulta_p= session.session_id(id)
    if consulta_p == None:
        return False 
    if consulta_p[1] == 1 :
        consulta_c = session.query_client(id)  
        if consulta_c == None:
            # customer does not exist
            session.update_p(id,consulta_p[1])
            session.create_user(id, name_client, 0)
            print("CLIENT CREATED")
            print("NAME: " + mensagem.text)
            return True
        else:
            # customer exists
            session.update_p(id,9)
            return True
    print("...")
    return False
    
# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=verify_name)
async def echo_message(message):
    print(message.chat)
    print("----")
        
    id = message.chat.id
    name = message.text
    consulta_p= session.session_id(id)
    if consulta_p[1] == 10:
        date_object = datetime.datetime.strptime('2000-05-12 10:30:00', "%Y-%m-%d %H:%M:%S")
        ##check if you already have a plan by expiration day
        consulta_venc = session.query_client(id)
        # CONVERT QUERY[3] STR TO DATA
        current_date = datetime.datetime.now()
        if consulta_venc[3]!=None:
            date_object = datetime.datetime.strptime(str(consulta_venc[3]), "%Y-%m-%d %H:%M:%S")
            print (date_object)
        #consulta vencimento > current date ok have a valid plan send link ELSE go to the second if
        #### if you already have a registration
        if (date_object > current_date and consulta_p[1]==10):
            session.update_p(id,consulta_p[1])
            await bot.send_message(id, "Verifiquei que você tem plano ativo. O que deseja fazer?", reply_markup=gen_markup_invite())
        if (date_object < current_date and consulta_p[1]==10):
            session.update_p(id,consulta_p[1])
            grupo = session.query_client_id_g(id)

            await bot.send_message(id, "Verifiquei que você já está conosco mas não tem plano ativo.")
            await bot.send_message(id, "PLANOS", reply_markup=gen_markup(grupo))
    if (consulta_p[1]==2):
        # 
            session.update_p(id,consulta_p[1])
            await bot.send_message(id, f"Legal {name}. Qual seu email?")

#--------------------------EMAIL--------------------------#
def check_email(mensagem):
    email_client = mensagem.text
    id= mensagem.chat.id
    print("-----")
    consulta_p= session.session_id(id)
    #check email
    checked= check(email_client)
    print ("VALID? ", checked)

    if consulta_p[1] == 16 and checked==1:
        session.update_e(id,email_client)
        print("Email: "+mensagem.text)
        notifications.ntf_att_email(id)
    
    verifsess = session.query_session(id)
    print(verifsess)
    if verifsess==False:
        return False

    if consulta_p == None :
        return False 
    if consulta_p[1] == 3 and checked==1:
        session.update_p(id,consulta_p[1])
        session.update_e(id,email_client)
        print("Email: "+mensagem.text)
        return True
    if consulta_p[1] == 3 and checked==0:
        notifications.ntf_email(id)
        return False
    


    return False

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=check_email)
async def echo_message(message):
    print("------")    
    id = message.chat.id
    
    consulta_p = session.session_id(id)

    if (consulta_p[1]==4):
        session.update_p(id,consulta_p[1])
        
        # await bot.send_message(id, "PLANOS", reply_markup=gen_markup())
        await bot.send_message(id, "Selecione o grupo que deseja participar:", reply_markup=grupos())


#--------------------------group--------------------------#
def check_grupo(mensagem):
    id= mensagem.chat.id
    print("-------")
    consulta_p= session.session_id(id)
    #check email
    verifsess = session.query_session(id)
    print(verifsess)
    if verifsess==False:
        return False
    if consulta_p == None :
        return False 
    if consulta_p[1] == 5 :
        session.update_p(id,consulta_p[1])
        return True

    return False

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=check_grupo)
async def echo_message(message):
    print("--------")
    id = message.chat.id
    
    consulta_p = session.session_id(id)

    if (consulta_p[1]==6):
        session.update_p(id,consulta_p[1])
        grupo = session.query_client_id_g(id)    
        await bot.send_message(id, "PLANOS", reply_markup=gen_markup(grupo))



################################################################
def start_session(id):
    print("---------")
    res_session_open = session.query_session(id)
    print("Open session? "+ str(res_session_open) +"  id:", id )

    if(res_session_open==False):
        print("--")

        session.create_session_id(id)
        print("SESSION STARTED")

        print("--")
        return "Active"

    print("--")
    print("ALREADY STARTED SESSION")
    

#VERIFY IF THE EMAIL IS VALID
def check(email):  

    if(re.search(regex,email)):  
        print("Valid Email")  
        return 1
    else:  
        print("Invalid Email")      
        return 0

###################################

# PLAN BUTTONS
def gen_markup(id_grupo):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    plano1 = session.query_plan_1(id_grupo)
    plano2 = session.query_plan_2(id_grupo)
    plano3 = session.query_plan_3(id_grupo)

    markup.add(
                InlineKeyboardButton(plano1[4], callback_data="monthly"),
               InlineKeyboardButton(plano2[4], callback_data="quarterly"),
               InlineKeyboardButton(plano3[4], callback_data="Yearly"))
    return markup


# USER BUTTON
def gen_markup_invite():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
            InlineKeyboardButton("Link para o grupo", callback_data="link"),
            InlineKeyboardButton("Renovar", callback_data="renew"))
    
    return markup

# PLAN BUTTONS
def grupos():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
                InlineKeyboardButton("GRUPO1", callback_data="GRUPO1"),
               InlineKeyboardButton("GRUPO2", callback_data="GRUPO2"),
               InlineKeyboardButton("GRUPO3", callback_data="GRUPO3"))
    return markup

# BUTTON CONFIRM PAYMENT
def gen_markup2():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("FIZ O PAGAMENTO", callback_data="pg_ok"))
    
    return markup


# CONDITIONS FOR BUTTONS
@bot.callback_query_handler(func=lambda call: True)
async def callback_inline(call):
    
    try:
        if call.message:
            id = call.message.chat.id
            
            if call.data == 'monthly':
                id_grupo = session.query_client_id_g(id) 
                plano1 = session.query_plan_1(id_grupo)
                print(plano1[2])
                # pix
                valor = plano1[2]
                token = pix.auth_gerencia() 
                copiaCola = pix.immediate_charge(token, id, valor)
                # immediate_charge
                await bot.send_message(id, 
"""Para efetuar o pagamento, utilize a opção 
"Pagar" -> "PIX Copia e Cola" no aplicativo do seu banco. 
(Não usar a opção chave aleatória)
Copie o código abaixo:\n""")
                await bot.send_message(id, copiaCola)
                await bot.send_message(id, "Assim que efetuar o pagamento clique no botão abaixo.", reply_markup=gen_markup2())
  
            if call.data == 'quarterly':
                # pix
                id_grupo = session.query_client_id_g(id) 
                plano2 = session.query_plan_2(id_grupo)
                valor = plano2[2]
                token = pix.auth_gerencia() 
                copiaCola = pix.immediate_charge(token, id, valor)
                #criar log de faturas /idcliente/txid fatura/valor/data

                await bot.send_message(id, 
"""Para efetuar o pagamento, utilize a opção 
"Pagar" -> "PIX Copia e Cola" no aplicativo do seu banco. 
(Não usar a opção chave aleatória)
Copie o código abaixo:\n""")
                await bot.send_message(id, copiaCola)
                await bot.send_message(id, "Assim que efetuar o pagamento clique no botão abaixo.", reply_markup=gen_markup2())

            if call.data == 'Yearly':
                # pix
                id_grupo = session.query_client_id_g(id) 
                plano3 = session.query_plan_3(id_grupo)
                valor = plano3[2]
                token = pix.auth_gerencia() 
                copiaCola = pix.immediate_charge(token, id, valor)

                await bot.send_message(id, 
"""Para efetuar o pagamento, utilize a opção 
"Pagar" -> "PIX Copia e Cola" no aplicativo do seu banco. 
(Não usar a opção chave aleatória)
Copie o código abaixo:\n""")
                await bot.send_message(id, copiaCola)
                await bot.send_message(id, "Assim que efetuar o pagamento clique no botão abaixo.", reply_markup=gen_markup2())

            if call.data == 'pg_ok':
#CONSULTATION RECEIPT
                token = pix.auth_gerencia() 
                status_fatura = pix.immediate_billing_query(token, id)
                if status_fatura==True:
                    notifications.unban(id)
                
# ALTERAR O NUMERO -1001650455571 PELO ID DO SEU GRUPO
                    invite = await bot.create_chat_invite_link(-1001650455571, member_limit=1, expire_date=int(time())+45) #Here, the link will auto-expire in 45 seconds
                    InviteLink = invite.invite_link #Get the actual invite link from 'invite' class
                
                    mrkplink = InlineKeyboardMarkup() #Created Inline Keyboard Markup
                    mrkplink.add(InlineKeyboardButton("Entrar no grupo 🚀", url=InviteLink)) #Added Invite Link to Inline Keyboard
                    
                    await bot.send_message(id, "Você pode usar o comando /comandos a qualquer momento!")
                    await bot.send_message(id, "SHOWW! Agora só falta você entrar no grupo.", reply_markup=mrkplink)
                    
                if status_fatura==False:
                    await bot.send_message(id, "Não identificamos seu pagamento...Assim que concluir clique no botão acima.")

# LINK TO THE GROUP
            if call.data == 'link':

# ALTERAR O NUMERO -1001650455571 PELO ID DO SEU GRUPO
                invite = await bot.create_chat_invite_link(-1001650455571, member_limit=1, expire_date=int(time())+45) #Here, the link will auto-expire in 45 seconds
                InviteLink = invite.invite_link #Get the actual invite link from 'invite' class
            
                mrkplink = InlineKeyboardMarkup() #Created Inline Keyboard Markup
                mrkplink.add(InlineKeyboardButton("Entrar no grupo 🚀", url=InviteLink)) #Added Invite Link to Inline Keyboard
            
                await bot.send_message(id, "SHOWW! Agora só falta você entrar no grupo.", reply_markup=mrkplink)

            if call.data == 'GRUPO1':
# ALTERAR O NUMERO -1001650455571 PELO ID DO SEU GRUPO
                # ATT GRUPO CLI
                session.update_g(id,-1001650455571)
                await bot.send_message(id, "SHOWW! Agora só escolher o plano.", reply_markup=gen_markup(-1001650455571))
                print('plano1')

            if call.data == 'GRUPO2':
# ALTERAR O NUMERO -1001650455571 PELO ID DO SEU GRUPO
                session.update_g(id,-1001650455571)
                await bot.send_message(id, "SHOWW! Agora só escolher o plano.", reply_markup=gen_markup(-1001650455571))
                print('plano2')
            if call.data == 'GRUPO3':
# ALTERAR O NUMERO -1001650455571 PELO ID DO SEU GRUPO
                session.update_g(id,-1001650455571)
                await bot.send_message(id, "SHOWW! Agora só escolher o plano.", reply_markup=gen_markup(-1001650455571))
                print('plano2')
# RENOVAÇÃO
            if call.data == 'renew':
                grupo = session.query_client_id_g(id)
                await bot.send_message(id, "PLANOS", reply_markup=gen_markup(grupo))
    except Exception as e:
        print(repr(e))






asyncio.run(bot.polling())