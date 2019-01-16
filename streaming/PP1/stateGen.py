import pandas as pd
import os
import sys
import time
import matplotlib.pyplot as plt
import scipy.signal
import numpy as np
import seaborn as sns


# plt.rcParams["figure.figsize"]=[15,5]

if len(sys.argv) <  2:

        print("No filename passed. Place the CSV file in the same folder.")

        exit(2)

ppfile=sys.argv[1]

if not os.path.isfile(ppfile):

        print("File not found!")

        exit(1)

try:
    raw_pp = pd.read_csv(ppfile, usecols=['timestamp', 'data.ax', 'data.az'])
    raw_pp_current=pd.read_csv(ppfile, usecols=['timestamp', 'data.A1', 'data.A2', 'data.A3'])
except:

        print("Invalid file!")
        exit(3)


raw_pp.dropna(axis=0, inplace=True)
raw_pp.sort_values(by=['timestamp'], inplace=True)
raw_pp.reset_index(inplace=True)
#raw_pp['timestamp'] =  pd.to_datetime(raw_pp['timestamp'])

raw_pp_current.dropna(axis=0, inplace=True)
raw_pp_current.sort_values(by=['timestamp'])
raw_pp_current.reset_index(inplace=True)
raw_pp_current['total_current']=raw_pp_current['data.A1']+raw_pp_current['data.A2']+raw_pp_current['data.A3']
raw_pp_current.index=raw_pp_current['timestamp']



#Load LD data and plot
raw_pp["acc"] = ( raw_pp["data.ax"]**2 + raw_pp["data.az"]**2) ** 0.5
acc=raw_pp[["timestamp", "acc"]]
test_pp=acc
# test_pp['acc_rolling_sum']=pd.Series.to_frame(test_pp.acc.rolling(100*10, center=True).sum())
test_pp['acc_rolling_std']=pd.Series.to_frame(test_pp.acc.rolling(100*2, center=True).std())

test_pp['detections']=pd.Series.to_frame(test_pp.acc_rolling_std.rolling(100, center=True).sum())

# plt.plot(test_pp['timestamp'], test_pp['acc']*100)
# plt.plot(test_pp['timestamp'], test_pp['detections'])


test_pp['boards']=0
test_pp['boards'][test_pp['detections']>=2]=1


# plt.plot(test_pp["timestamp"],test_pp["boards"])

working_times_raw=scipy.signal.find_peaks(test_pp.boards, distance=40*72, width=1)
working_times_raw_df=pd.DataFrame({"sample_number":working_times_raw[0], "working_time":working_times_raw[1]['widths']/72})


for x, row in working_times_raw_df.iterrows():
    working_times_raw_df.ix[x,'start_time']=test_pp.iloc[int(working_times_raw[1]['left_ips'][x])].timestamp
    working_times_raw_df.ix[x,'end_time']=test_pp.iloc[int(working_times_raw[1]['right_ips'][x])].timestamp
    working_times_raw_df.ix[x,'timestamp']=test_pp.iloc[int(working_times_raw[0][x])].timestamp

working_times_df=working_times_raw_df[working_times_raw_df.working_time>30]
working_times_df['event']=1
working_times_df['energy'] = working_times_df.apply(lambda x: raw_pp_current.loc[(raw_pp_current.timestamp <= x.end_time) &
                                                            (x.start_time <= raw_pp_current.timestamp),
                                                            ['total_current']].sum()*230, axis=1)


working_times_df.index=working_times_df.timestamp
working_times_df.drop('timestamp', axis=1, inplace=True)
working_times_df.drop('sample_number', axis=1, inplace=True)

# plt.plot(test_pp["timestamp"],test_pp["boards"])
# plt.plot(raw_pp_current.timestamp, raw_pp_current['total_current'])

PP_events=working_times_df[['event', 'working_time', 'energy']]

PP_events['device']='pickandplace1'
print(PP_events)

# In[ ]:

timestr = time.strftime("%H-%M")
print('PP1 working time mode: ', PP_events.working_time.mode().mean())
parameters=open('/home/richard/Desktop/LiveParameters/PP1parameters.txt','a+')
parameters.write(timestr +'\tPP1 working time mode: ' + str(PP_events.working_time.mode().mean())+'\n')
parameters.close()
# In[24]:

if not os.path.exists('/mnt/UltraHD/streamingStates/PP1'):

    os.makedirs('/mnt/UltraHD/streamingStates/PP1')

# sns.distplot(PP_events.working_time)
# plt.title('PP1 Working Times Histogram')
#plt.savefig("/mnt/UltraHD/streamingStates/PP1/PP1boardstimes_hist.png") 

directory='/mnt/UltraHD/streamingStates/PP1'


timestr = time.strftime("%Y-%m-%d_%H-%M-%S")
print("Saving States with file name -", timestr+"_PP1.csv")
PP_events.to_csv('/mnt/UltraHD/streamingStates/PP1/'+ timestr+"_PP1.csv")

