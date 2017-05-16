rom MururiTrueFx import truefx
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook # used as a data starage format.
import math
# https://github.com/femtotrader/pandas_datareaders_unofficial/commit/b3008b1eb9e2fd1cd86efd6561296fcb5adf0bd8 some copy and paste.
import time
import threading

auth_response = truefx.login('jesusislord3','Anglocat777',['EUR/USD'])

print('auth response is',auth_response)

# plot axis
rates = []
timestamps = []
response = ''

#graph settings
tickrate = 0.025 # official tick rate
duration_to_plot = 3600 # in seconds
bootstrap = math.ceil(duration_to_plot / tickrate) # round up to give a rough estimated number of samples.

def boxplot(poll_one_pair:dict,time_in_seconds:int=3600,poll_rate:float=0.025): # results from truefx.poll_one_pair()
    pass

# from this example - http://stackoverflow.com/a/18793416

def data_listener():
    while True:
        time.sleep(tickrate)
        current_poll = truefx.poll_one_pair(auth_response)
        print('Tick')
        rates.append(float(current_poll['bigbid'])+(float(current_poll['bidpips'])/1000))
        timestamps.append(current_poll['millisecond-timestamp'])

        response = current_poll['response']
        # truncate plot axis
        del rates[bootstrap:]
        del timestamps[bootstrap:]

thread = threading.Thread(target=data_listener)
thread.daemon = True # do not be afraid christians! they dont exist :) fear  is of the devil anyways :D
thread.start()

time.sleep(1)
print('length of labels:',len(timestamps),'length of rates',len(rates))

# statts is populated after the listener starts
# stats = cbook.boxplot_stats(rates, labels=timestamps, bootstrap=bootstrap)
stats = cbook.boxplot_stats({'test1':1.2,'test2':1.4,'test5':1.7})

#plot graph
fs = 10  # fontsize





