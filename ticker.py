import csv
import requests
import time
import os
import urllib

# https://github.com/femtotrader/pandas_datareaders_unofficial/commit/b3008b1eb9e2fd1cd86efd6561296fcb5adf0bd8 some copy and paste.

truefx  = requests.session()


symbols = ["EUR/USD"]
url = 'http://webrates.truefx.com/rates/connect.html'

params = {
    'f': 'csv',
    'c': symbols,
    'q': 'eurates',
    'u': 'jesusislord3', 
    'p': 'Anglocat777',
    's': 'y',
}

symbol_param = symbols[0] if len(symbols) == 1 else symbols.join(',')

login_url = str(url + '?u=' + params['u'] + '&p=' + params['p'] + '&q=' +params['q'] + '&c=' + symbol_param + '&f=' + params['f'] + '&s=' +params['s'])
login = truefx.get(login_url, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})  #.split(':')
print('login url is',login.url)
id = login.text
print('id is',id)
(username, password, qualifier, session_id) = id.split(':')
print('Session ID',session_id)
truefx.headers.clear()
while True:
    time.sleep(0.025) # official tick rate
    # url = 'http://webrates.truefx.com/rates/connect.html?id=' + id + "c=" + symbols
    ticker_params = {
         'id': str(session_id),
    } 

    # response = session.get(url, params=params) 
    
    # print('url is \n',url)    
    # results = truefx.get(url + '?id=' + login.text)
    
    with urllib.request.urlopen(url + '?id=' + login.text) as results:
        response = results.read().decode()
        poll = dict(zip(['currency-pair','millisecond-timestamp','bigbid,bidpips','high,low','pollopen'],response.split(',')))
        if response: # dont print blank reponses
            # print("url is",results.url,"status is",results.getcode())
            print(str(response))
        else:
            continue
    
    print('millesend is',poll['millisecond-timestamp'])
