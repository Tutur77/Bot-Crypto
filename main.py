
import requests
import json
import time
import re
import hashlib
import hmac
import base64
import urllib







def timeServer(url):

        r =  requests.get(url)
        json_object = json.loads(r.text)
        return json_object["result"]["rfc1123"]


def listTickers():

       # help(KrakenAPI)
        r = requests.get("https://api.kraken.com/0/public/AssetPairs")
        json_object = json.loads(r.text)
        for d in json_object:
                print(json_object[d])

def getTicker(ticker = "BTCEUR"):
    return ticker



def saveMoyenneCSV():
    result = []
    times = timeServer("https://api.kraken.com/0/public/Time")
    moyenne = calculMoyenne()
    moyenne = str(moyenne)
    result.append(times)
    result.append(moyenne)

    strr = ' ; '.join(result)
    with open('Averages.txt', 'a') as file:
        file.write(strr + "\n")


def priceOneTicker():
        ticker = "BTCEUR"
        getTicker(ticker)
        r = requests.get("https://api.kraken.com/0/public/Ticker?pair="+ticker)
        json_object = json.loads(r.text)
        x = json_object['result']
        for i in x:
                return x[i]['c'][0]


def savePriceCSV(count):
        res = priceOneTicker()
        times = timeServer("https://api.kraken.com/0/public/Time")
        result = []
        result.append(getTicker())
        result.append(times)
        result.append(res)

        str = ' ; '.join(result)
        with open('Tickers.txt', 'a') as file:
            file.write(str + "\n")

        count = count + 1
        #time.sleep(1)
        #saveMoyenneCSV()
        #savePriceCSV(count)



def calculMoyenne():
    file = open('Tickers.txt', 'r')
    Lines = file.readlines()
    res = []
    moyenne=0
    count=0

    for line in Lines:
        count = count +1
        res = line.split(";")
        result = float(res[-1])
        moyenne = moyenne + result
    moyenne = moyenne/count
    return moyenne

Kraken_secret_key = ''

Kraken_headers ={'API-Key': ''}



def kraken_api(kraken_headers,query,URI_path,URL_path):

    count = 0
    if query == 'balance':
        Kraken_nonce = str(int(time.time() * 1000))
        Kraken_POST_data = {

            'nonce': Kraken_nonce
        }

        url_encoded_post_data = urllib.parse.urlencode(Kraken_POST_data)

        encoded = (str(Kraken_POST_data['nonce']) + url_encoded_post_data).encode()

        message = URI_path.encode() + hashlib.sha256(encoded).digest()

        Kraken_signature = hmac.new(base64.b64decode(Kraken_secret_key), message,
                                    hashlib.sha512)

        Kraken_signature_digest = base64.b64encode(Kraken_signature.digest())

        Kraken_headers['API-Sign'] = Kraken_signature_digest.decode()

        response = requests.post(URL_path, data=Kraken_POST_data, headers=
        Kraken_headers)

        result = response.json()

        print(result)


    elif query == 'pending_order':
        Kraken_nonce = str(int(time.time() * 1000))
        Kraken_POST_data = {

            'nonce': Kraken_nonce
        }

        url_encoded_post_data = urllib.parse.urlencode(Kraken_POST_data)

        encoded = (str(Kraken_POST_data['nonce']) + url_encoded_post_data).encode()

        message = URI_path.encode() + hashlib.sha256(encoded).digest()

        Kraken_signature = hmac.new(base64.b64decode(Kraken_secret_key), message,
                                    hashlib.sha512)

        Kraken_signature_digest = base64.b64encode(Kraken_signature.digest())

        Kraken_headers['API-Sign'] = Kraken_signature_digest.decode()

        response = requests.post(URL_path, data=Kraken_POST_data, headers=
        Kraken_headers)

        result = response.json()
        res = []
        result = response.json()
        x = result['result']['open']
        for i in x:
            if (result['result']['open'][i]['status'] == 'pending'):
                count = count + 1
                print("{} {}".format(result['result'], "\n"))
                res.append(result['result'])
        count = str(count)
        print("Il y a " + count + " ordres en attente")

        return res



    if query == 'query_order' or count != 0:
        Kraken_nonce = str(int(time.time() * 1000))
        Kraken_POST_data = {
            'pair': 'BTCEUR',
            'type': 'sell',
            'ordertype': 'market',
            'volume': '0.001',
            'nonce': Kraken_nonce
        }

        url_encoded_post_data = urllib.parse.urlencode(Kraken_POST_data)

        encoded = (str(Kraken_POST_data['nonce']) + url_encoded_post_data).encode()

        message = URI_path.encode() + hashlib.sha256(encoded).digest()

        Kraken_signature = hmac.new(base64.b64decode(Kraken_secret_key), message,
                                    hashlib.sha512)

        Kraken_signature_digest = base64.b64encode(Kraken_signature.digest())

        Kraken_headers['API-Sign'] = Kraken_signature_digest.decode()

        response = requests.post(URL_path, data=Kraken_POST_data, headers=
        Kraken_headers)

        result = response.json()

        print(result)

def Ledger():

    result = []
    closed_result = []
    order = kraken_api(Kraken_headers,'pending_order','/0/private/OpenOrders','https://api.kraken.com/0/private/OpenOrders')
    closed_order = closedQuery(Kraken_headers,'/0/private/ClosedOrders','https://api.kraken.com/0/private/ClosedOrders')
    result.append(order)
    closed_result.append(closed_order)
    print(closed_result)

    with open('Ledger.txt', 'w') as file:
        file.write("Ordres en attentes" + "\n")
        file.write(str(result) + "\n")
        file.write("Ordres fermees" + "\n")
        file.write(str(closed_result) + "\n")




def closedQuery(kraken_headers,URI_path,URL_path):


    Kraken_nonce = str(int(time.time() * 1000))
    Kraken_POST_data = {
        'nonce': Kraken_nonce
    }

    url_encoded_post_data = urllib.parse.urlencode(Kraken_POST_data)

    encoded = (str(Kraken_POST_data['nonce']) + url_encoded_post_data).encode()

    message = URI_path.encode() + hashlib.sha256(encoded).digest()

    Kraken_signature = hmac.new(base64.b64decode(Kraken_secret_key), message,
                                hashlib.sha512)

    Kraken_signature_digest = base64.b64encode(Kraken_signature.digest())

    Kraken_headers['API-Sign'] = Kraken_signature_digest.decode()

    response = requests.post(URL_path, data=Kraken_POST_data, headers=
    Kraken_headers)

    result = response.json()

    print(result)


def BOT():
    while True:

        print(timeServer("https://api.kraken.com/0/public/Time"))
        listTickers() # Liste tous les Tickers
        print(priceOneTicker()) # Le prix d'un ticker désigné
        savePriceCSV(0) # Sauvegarde la moyenne dans le fichier Averages.txt
        print(calculMoyenne()) # Calcul la moyenne du fichier Tickers.txt (Qui ai sensé s'exécuter pendant 5 minutes



        kraken_api(Kraken_headers,'balance','/0/private/Balance','https://api.kraken.com/0/private/Balance') # Request balance
        kraken_api(Kraken_headers,'pending_order','/0/private/OpenOrders','https://api.kraken.com/0/private/OpenOrders') # Check Pending order
        kraken_api(Kraken_headers,'query_order','/0/private/AddOrder','https://api.kraken.com/0/private/AddOrder') # New Order
        Ledger() # Ordres en attentes et ordres fermées dans le fichier
        #closedQuery(Kraken_headers,'/0/private/ClosedOrders','https://api.kraken.com/0/private/ClosedOrders')



BOT()