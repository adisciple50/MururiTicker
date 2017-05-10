from .MururiTrueFx import truefx
# https://github.com/femtotrader/pandas_datareaders_unofficial/commit/b3008b1eb9e2fd1cd86efd6561296fcb5adf0bd8 some copy and paste.


while True:
    time.sleep(0.025) # official tick rate
    # url = 'http://webrates.truefx.com/rates/connect.html?id=' + id + "c=" + symbols
    
    with urllib.request.urlopen(url + '?id=' + login.text) as results:
        response = results.read().decode()
        poll = dict(zip(['currency-pair','millisecond-timestamp','bigbid,bidpips','high,low','pollopen'],response.split(',')))
        if response: # dont print blank reponses
            # print("url is",results.url,"status is",results.getcode())
            print(str(response))
        else:
            continue
    
    print('millesend is',poll['millisecond-timestamp'])
