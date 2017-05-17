from MururiTrueFx import truefx
from MururiTrueFx.utils import actual_figure
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook # used as a data starage format.
import math
# https://github.com/femtotrader/pandas_datareaders_unofficial/commit/b3008b1eb9e2fd1cd86efd6561296fcb5adf0bd8 some copy and paste.
import time
import threading
from mpl_finance import mpl_finance

auth_response = truefx.login('jesusislord3','Anglocat777',['EUR/USD'])

print('auth response is',auth_response)

# plot axis
opens = []
closes = [] # bigbid and bidpips
highs = []
lows = []
timestamps = []
response = ''

#graph settings
tickrate = 0.025 # official tick rate
duration_to_plot = 3600 # in seconds
bootstrap = math.ceil(duration_to_plot / tickrate) # round up to give a rough estimated number of samples.



# from this example - http://stackoverflow.com/a/18793416

def data_listener():
    while True:
        time.sleep(tickrate)
        current_poll = truefx.poll_one_pair(auth_response)
        print('Tick')
        print('Current Poll is',current_poll['response'])
        opens.append(float(current_poll['pollopen']))
        closes.append(actual_figure(current_poll['bigbid'],current_poll['bidpips']))
        highs.append(float(current_poll['high']))
        lows.append(float(current_poll['low']))
        timestamps.append(current_poll['millisecond-timestamp'])

        # truncate plot axis
        """
        del opens[bootstrap:]
        del closes[bootstrap:]
        del highs[bootstrap:]
        del lows[bootstrap:]
        del timestamps[bootstrap:]
        """

thread = threading.Thread(target=data_listener)
thread.daemon = True # do not be afraid christians! they dont exist :) fear  is of the devil anyways :D
thread.start()

time.sleep(1)
print('length of labels:',len(timestamps),'length of rates',len(closes))

# statts is populated after the listener starts
# stats = cbook.boxplot_stats(rates, labels=timestamps, bootstrap=bootstrap)
# stats = cbook.boxplot_stats({'test1':1.2,'test2':1.4,'test5':1.7})

#plot graph
fs = 10  # fontsize

# demonstrate how to toggle the display of different elements:
fig, ax = plt.subplots()

mpl_finance.candlestick2_ochl(ax,opens,closes,highs,lows,)


#ax.autoscale_view() # layout correction
# plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right') # set the layout of the grid. tick  from right to left and bars should be verticle.

print(opens,closes,highs,lows)

plt.show()
"""
# redraw graph
while True:
    time.sleep(tickrate)
    print('Current Rates Are \n',response)
    plt.pause(tickrate)
    # update data
    # fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(6, 6), sharey=True)
    # redraw
    plt.draw()

"""



