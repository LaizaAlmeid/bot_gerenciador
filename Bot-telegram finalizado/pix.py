import json
from pydoc import cli
import re
from traceback import print_tb
# ----------------------------------------------------------------------------------------
import requests
import json
from requests.auth import HTTPBasicAuth

import datetime

import rstr

import session

import notifications

my_key_pix="a93bf0be-71ee-473c-a3e2-99bc8f6b0530"

copiacolaPix=""


def immediate_charge(token, id , valor):
    txid=(rstr.xeger(r'^[a-zA-Z0-9]{26,35}$'))

    print('SOLICITANDO COBRANCA')
    res = session.query_id(id)
    print (valor)
    url = f'https://api-pix.gerencianet.com.br/v2/cob/{txid}'

    payload = json.dumps({
    'calendario': {
        'expiracao': 3600
    },
    'devedor': {
        'cpf': '12345678909',
        'nome': f'{res[1]}'
    },
    'valor': {
        'original': f'{valor}'
    },
    'chave': f'{my_key_pix}',
    'solicitacaoPagador': 'Informe o número ou identificador do pedido.'
    })
    
    head = {
    'Authorization': f'Bearer {token}' ,
    'x-client-cert-pem': 'certificado.pem',
    'Content-Type': 'application/json'
    }
    response = requests.request("PUT", url, data=payload, headers=head, cert=('certificado.pem'))
    print(response.text)
    print(type(response.json()))
    loc_id = response.json()['loc']['id']
    txid_res = response.json()['txid']
    
    session.create_invoice(id,loc_id,txid_res,valor)
    
# ---------------------------------------------------
    print('SOLICITANDO QRCODE')
    url2 = f'https://api-pix.gerencianet.com.br/v2/loc/{loc_id}/qrcode'
    
    payload={}
    headers = {
    'Authorization': f'Bearer {token}',
    'x-client-cert-pem': 'certificado.pem', }
    response = requests.request("GET", url2, headers=headers,cert=('certificado.pem'))

    copiacolaPix=response.json()['qrcode']
    imgQrPix=response.json()['imagemQrcode']
    print("NUMERO DA LOC E COPIA COLA",loc_id," ",copiacolaPix)
    return copiacolaPix

# -----------------------------------------------------------------------------------------
def immediate_billing_query(token, id):
    
    session.query_session(id)
    cliente= session.query_id(id)
    grupo_cli= cliente[7]
    txid = session.query_invoice(id)
    print(txid)
    print(token)
    url = f'https://api-pix.gerencianet.com.br/v2/cob/{txid}'
    
    head = {
    'Authorization': f'Bearer {token}' ,
    'x-client-cert-pem': 'certificado.pem',
    'Content-Type': 'application/json'
    }

    response = requests.request("GET", url,  headers=head, cert=('certificado.pem'))
    print(response.text)
    print(type(response.json()))
    txid_res = response.json()['txid']
    status_res = response.json()['status']
    ##########
    valor = response.json()['pix'][0]['valor']

    if txid_res== txid and status_res=="CONCLUIDA":  
        datahr_pagamento = response.json()['pix'][0]['horario']

        trans_date= datetime.datetime.strptime(datahr_pagamento,'%Y-%m-%dT%H:%M:%S.%fZ')
        data = (trans_date + datetime.timedelta(days=0))
        plano1 = session.query_plan_1(grupo_cli)
        plano2 = session.query_plan_2(grupo_cli)
        plano3 = session.query_plan_3(grupo_cli)
        if valor== plano1[2]:
            data = (trans_date + datetime.timedelta(days=30))
            print("+30dias")
        if valor== plano2[2]:
            data = (trans_date + datetime.timedelta(days=90))
            print("+90dias")
        if valor== plano3[2]:
            data = (trans_date + datetime.timedelta(days=365))
            print("+365")
        print("Vencimento para:")
        print(data)
        session.update_due_date(id,data)
        # NOTIFICA
        session.update_invoice(id,txid_res, datahr_pagamento,status_res)
        notifications.notificacoes(f"Pagamento efetuado pelo cliente: {cliente[1]}")
        return True
        
    if txid_res== txid and status_res!="CONCLUIDA": 
        datahr_pagamento = ""
        session.update_invoice(id,txid_res, datahr_pagamento,status_res)
        return False
# ---------------------------------------------------


def auth_gerencia():
    print('SOLICITANDO TOKEN')

    auth = HTTPBasicAuth('Client_Id_2c055a41861f9c9190c20b67c1745cc520bb6d62', 'Client_Secret_ab45bfb7f4e6676b074f0e5d2f869db9b6e740fc')


    url = "https://api-pix.gerencianet.com.br/oauth/token"

    payload = json.dumps({
    "grant_type": "client_credentials"
    })
    headers = {
    'x-client-cert-pem': 'certificado.pem',
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, data=payload, headers=headers, auth=auth, cert=('certificado.pem'))
    print(type(response.json()))
    print(response.json()['access_token'])
    token =response.json()['access_token']

    return token
