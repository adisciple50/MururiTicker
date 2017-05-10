import urllib

# url = 'http://webrates.truefx.com/rates/connect.html' - in case of endpoint change please refactor - or "find and replace".

truefx = urllib.request()

def login(username:str,password:str,symbols:list,qualifier='eurates',pollformat='csv',snapshot=True,url='http://webrates.truefx.com/rates/connect.html'):
    # make snapshot pythonic
    if snapshot:
        snapshot = 'y'
    else:
        snapshot = 'n'

    symbol_param = symbols[0] if len(symbols) == 1 else symbols.join(',')

    login_url = str(
        url + '?u=' + username + '&p=' + password + '&q=' + qualifier + '&c=' + symbol_param + '&f=' + pollformat + '&s=' + snapshot)

    with truefx.urlopen(login_url) as response:
        return response.read().decode()



def poll(auth_response:str,url='http://webrates.truefx.com/rates/connect.html'):
    with urllib.request.urlopen(url + '?id=' + login.text) as results:
        response = results.read().decode()
        poll_response = dict(zip(['currency-pair', 'millisecond-timestamp', 'bigbid,bidpips', 'high,low', 'pollopen'],
                        response.split(','))).update({'response':response})
        if response:  # dont print blank reponses
            return poll_response
        else:
            False

