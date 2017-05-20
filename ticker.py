from MururiTrueFx import truefx
from MururiTrueFx.utils import actual_figure

import math
# https://github.com/femtotrader/pandas_datareaders_unofficial/commit/b3008b1eb9e2fd1cd86efd6561296fcb5adf0bd8 some copy and paste.
import time
import threading

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

def data_listener(stop_interupt_signal:threading.Event):
    while (not stop_interupt_signal.is_set()):
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

thread_stopper = threading.Event()
thread = threading.Thread(target=data_listener,args=(thread_stopper,))
thread.daemon = True # do not be afraid christians! they dont exist :) fear  is of the devil anyways :D
thread.start()


time.sleep(1)
thread_stopper.set()
print('length of labels:',len(timestamps),'length of rates',len(closes))

time.sleep(5)
print(opens,closes,highs,lows,timestamps)
###  BEGIN GRAPH PLOTTING
import numpy as np
from bokeh.plotting import figure, output_file, show

def to_np_dt64(x):
    return np.datetime_as_string(np.datetime64(x,'ms'))

nptimestamps = list(map(to_np_dt64,timestamps))

print('nptimestamps\n',nptimestamps)

aapl = np.array(closes)
aapl_dates = np.array(nptimestamps, dtype=np.datetime64)

print('aapl_dates',aapl_dates)

## EXAMPLE

window_size = 30
window = np.ones(window_size)/float(window_size)
aapl_avg = np.convolve(aapl, window, 'same')

# output to static HTML file
output_file("stocks.html", title="stocks.py example")

# create a new plot with a a datetime axis type
p = figure(width=800, height=350, x_axis_type="datetime")

# add renderers
p.circle(aapl_dates, aapl, size=4, color='darkgrey', alpha=0.2, legend='close')
p.line(aapl_dates, aapl_avg, color='navy', legend='avg')

# NEW: customize by setting attributes
p.title.text = "AAPL One-Month Average"
p.legend.location = "top_left"
p.grid.grid_line_alpha=0
p.xaxis.axis_label = 'Date'
p.yaxis.axis_label = 'Price'
p.ygrid.band_fill_color="olive"
p.ygrid.band_fill_alpha = 0.1

# show the results
show(p)

## End Example