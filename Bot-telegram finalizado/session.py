
import json
from pymysql import connect
import math
import datetime

import notifications

conexao = connect(
    host='50.116.86.63',
    user='grup1047_veribot',
    password='#inFA0701',
    database='grup1047_veribot',
)
cursor = conexao.cursor()
 
def ntf_client():
    print("CONSULTANDO CLIENTEe...") 
    conexao.ping(reconnect=True)      
    
    command ="SELECT * FROM Clientes"
    cursor.execute(command)
    result = cursor.fetchall() 
    count = len(result)
    print("Result:",count)

    for res in result:
        date_object = datetime.datetime.strptime('2000-05-12 10:30:00', "%Y-%m-%d %H:%M:%S")
        # CONVERT
        current_date = datetime.datetime.now()
        if res[3]!=None:
            date_object = datetime.datetime.strptime(str(res[3]), "%Y-%m-%d %H:%M:%S")
            print (date_object)
        if (date_object > current_date ):
            dias= ((date_object- current_date).days)
            print(math.floor(dias))
            print(res[8])
            if math.floor(dias)==2:
                if res[8]==0:
                    command = 'UPDATE Clientes SET notificado = %s WHERE id_conv_telegram = %s'
                    cursor.execute(command,('1',res[6]))
                    conexao.commit() 
                    notifications.ntf_renovacao(res[6])
                


###########################
###########################

 # CONTULTA CLIENTE PELO ID
###############################
def query_id(id):
    print("Query client") 
    conexao.ping(reconnect=True)      

    print("ID query",id)
    comando ="SELECT * FROM Clientes WHERE id_conv_telegram =(%s) LIMIT 2"
    ## search for last!!!!!!!!
    cursor.execute(comando,(id,))
    resultado = cursor.fetchall()
    
    for res in resultado:
        return res


# CONSULTA A ULTIMA SESSAO
# CONSULT THE SESSION BY IDCONSULT THE SESSION BY ID
###############################
def session_id(id):
    print("--")
    print("CONSULTING SESSION...") 
    ## check connection with the bank
    conexao.ping(reconnect=True)      
    
    print("ID_client: ",id)
    command ="SELECT * FROM SessoesAbertas WHERE id_cliente =(%s) ORDER BY data_criacao DESC limit 1"
    cursor.execute(command,(id,))
    result = cursor.fetchall()
    count = len(result)
    print(result)
    print("Result:",count)

    for res in result:
        return res

# CONSULTA O CLIENTE PELO ID
###############################
def query_client(id):
    print("CONSULTING CLIENT...")
    conexao.ping(reconnect=True)      
    
    print("ID: ",id)
    command ="SELECT * FROM Clientes WHERE id_conv_telegram =(%s)"
    cursor.execute(command,(id,))
    result = cursor.fetchall() 
    count = len(result)
    print("Result:",count)

    for res in result:
        return res

# CONSULTA SESSAO ABERTA E SE JÁ PASSOU DO TEMPO
# CONSULT IF THERE IS A SESSION
###############################
def query_session(id):
    conexao.ping(reconnect=True)      
    
    print("ID QUERY",id)

    command ="SELECT * FROM SessoesAbertas WHERE id_cliente =(%s) ORDER BY data_criacao DESC limit 1"
    cursor.execute(command,(id,))
    result = cursor.fetchall() 
    count = len(result)
    print("Sessões abertas do usuario:",count)
    
    time_out = datetime.datetime.now()
    
    for res in result:
        # Verifica se a ultima sessão foi a mais de 15 minutos
        date_object = datetime.datetime.strptime(str(res[4]), "%Y-%m-%d %H:%M:%S")
        print(date_object)
        print(time_out)
        minutos= ((time_out- date_object).seconds) / 60
        print("%.2f" %minutos)
        print("Id_cliente:" , res[0])
        
        if res[0]==None or minutos>7:
            return False
        return True

    return False


###############################
def query_invoice(id):
    conexao.ping(reconnect=True)      

    print("--")
    print("Query invoice") 

    date_current= datetime.datetime.now()
    date_previous= (datetime.datetime.now() - datetime.timedelta(days=1))
    print('DateTime end:', date_current)
    print('DateTime start:', date_previous)
    
    print("ID QUERY",id)
    command ="SELECT * FROM Faturas WHERE id_cliente =(%s) and date(data_criacao) >= %s and date(data_criacao) <= %s ORDER BY data_criacao DESC limit 1"
    cursor.execute(command,(id,date_previous.date(),date_current.date(),))
    result = cursor.fetchall() 
    
    for res in result:
        return res[3]




# CONSULTA O PLANO PELO ID
###############################
def query_plan_1(id_grupo):
    print("CONSULTING PLAN1...")
    conexao.ping(reconnect=True)      
    
    print("ID: ",id_grupo)
    command ="SELECT * FROM Planos WHERE id_grupo =(%s) and nome_id=(%s)"
    cursor.execute(command,(id_grupo,"plano1",))
    result = cursor.fetchall() 
    count = len(result)
    print("Result:",count)

    for res in result:
        return res

def query_plan_2(id_grupo):
    print("CONSULTING PLAN2...")
    conexao.ping(reconnect=True)      
    
    print("ID: ",id_grupo)
    command ="SELECT * FROM Planos WHERE id_grupo =(%s) and nome_id=(%s)"
    cursor.execute(command,(id_grupo,"plano2",))
    result = cursor.fetchall() 
    count = len(result)
    print("Result:",count)

    for res in result:
        return res

def query_plan_3(id_grupo):
    print("CONSULTING PLAN3...")
    conexao.ping(reconnect=True)      
    
    print("ID: ",id_grupo)
    command ="SELECT * FROM Planos WHERE id_grupo =(%s) and nome_id=(%s)"
    cursor.execute(command,(id_grupo,"plano3",))
    result = cursor.fetchall() 
    count = len(result)
    print("Result:",count)

    for res in result:
        return res

def query_client_id_g(id):
    print("CONSULTING PLAN id...")
    conexao.ping(reconnect=True)      
    
    print("ID: ",id)
    command ="SELECT * FROM Clientes WHERE id_conv_telegram =(%s)"
    cursor.execute(command,(id,))
    result = cursor.fetchall() 


    for res in result:
        return res[7]





###########################
###########################


# UPDATE
###############################
def update_client():
    print("CONSULTING CLIENT...") 
    conexao.ping(reconnect=True)      
    
    command ="SELECT * FROM Clientes"
    cursor.execute(command)
    result = cursor.fetchall() 
    count = len(result)
    print("Result:",count)

    for res in result:
        date_object = datetime.datetime.strptime('2000-05-12 10:30:00', "%Y-%m-%d %H:%M:%S")
        # CONVERT QUERY[3] STR TO DATA
        current_date = datetime.datetime.now()
        if res[3]!=None:
            date_object = datetime.datetime.strptime(str(res[3]), "%Y-%m-%d %H:%M:%S")
            print (date_object)
        if (date_object < current_date ):
            notifications.ban(res[6])
            command = 'UPDATE Clientes SET ativo = %s WHERE id_conv_telegram = %s'
            cursor.execute(command,('0',res[6]))
            conexao.commit() 

# UPDATE
###############################
def update_e(id,email):
    conexao.ping(reconnect=True)      
    
    command = 'UPDATE Clientes SET email = %s WHERE id_conv_telegram = %s'
    cursor.execute(command,(email,id,))
    conexao.commit() 


# UPDATE
###############################
def update_due_date(id,data):
    conexao.ping(reconnect=True)      
    
    command = 'UPDATE Clientes SET dia_venc = %s, ativo = %s , notificado = %s WHERE id_conv_telegram = %s'
    cursor.execute(command,(data,'1','0',id,))
    conexao.commit() # edita o banco de dados

# UPDATE
###############################
def update_p(id,passo):
    print("UPDATE STEP...")
    conexao.ping(reconnect=True)      

    passo_u=int(passo)+1
    command = 'UPDATE SessoesAbertas SET passo = %s WHERE id_cliente = %s ORDER BY data_criacao DESC limit 1'
    cursor.execute(command,(passo_u,id,))
    conexao.commit() 

# UPDATE
###############################
def update_a(id,aberta):
    print("--")
    print("UPDATE ASSET...")
    conexao.ping(reconnect=True)      

    aberta_u=int(aberta)+1
    command = 'UPDATE SessoesAbertas SET aberta = "%s" WHERE id_cliente = %s ORDER BY data_criacao DESC limit 1'
    cursor.execute(command,(aberta_u,id,))
    conexao.commit() 


# UPDATE
###############################
def update_invoice(id, txid,hr_pagamento,status_res):
    conexao.ping(reconnect=True)      

    command = 'UPDATE Faturas SET status = %s , data_pagamento = REPLACE (REPLACE (%s, "T", " "), ".000Z", "") WHERE id_cliente = %s and txid= %s'
    cursor.execute(command,(status_res, hr_pagamento, id, txid,))
    conexao.commit() 

# UPDATE
###############################
def update_g(id,grupo):
    conexao.ping(reconnect=True)      
    
    command = 'UPDATE Clientes SET grupo = %s WHERE id_conv_telegram = %s'
    cursor.execute(command,(grupo,id,))
    conexao.commit() 

# UPDATE
###############################
def update_plano(valor, descricao, id_grupo,nome_id):
    conexao.ping(reconnect=True)      
    
    command = 'UPDATE Planos SET valor = %s , descricao = %s WHERE id_grupo = %s and nome_id = %s '
    cursor.execute(command,(valor,descricao,id_grupo,nome_id,))
    conexao.commit() 


###############################
###############################

# CREATE ok
def create_user(id, nome, ativo):
    print("CREATING USER...")
    conexao.ping(reconnect=True)      

    command = 'INSERT INTO Clientes (id_conv_telegram , nome, ativo, notificado) VALUES (%s,%s,%s,%s)'
    cursor.execute(command,(id,nome,ativo,0))
    conexao.commit() 


#CREATE ok
def create_session_id(id):
    conexao.ping(reconnect=True)      

# ALTERAR O NUMERO -1001650455571 PELO ID DO SEU GRUPO
    if(id!="-100165045"):
        command = 'INSERT INTO SessoesAbertas (id_cliente , passo, aberta, data_criacao) VALUES (%s,%s,%s,%s)'
        cursor.execute(command,(id,0,0,datetime.datetime.now(),))
        conexao.commit() 

# CREATE ok
def create_invoice(id, loc_id, txid,valor):
    conexao.ping(reconnect=True)      
    
    #before creating, update open invoices with this id and pending status to canceled
    command = 'INSERT INTO Faturas (id_cliente , loc_id, txid, valor, status, data_criacao) VALUES (%s,%s,%s,%s,%s,%s)'
    cursor.execute(command,(id,loc_id,txid, valor,'Pendente', datetime.datetime.now(),))
    conexao.commit() 

