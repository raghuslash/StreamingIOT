
# coding: utf-8

# In[1]:


import pandas as pd
import os
import sys
import time
import matplotlib.pyplot as plt
import scipy.signal
import numpy as np
import seaborn as sns

# In[2]:


# In[3]:


#plt.rcParams["figure.figsize"]=[15,5]

# In[4]:

if len(sys.argv) <  2:

        print("No filename passed. Place the CSV file in the same folder.")

        exit(2)

spfile=sys.argv[1]

if not os.path.isfile(spfile):

        print("File not found!")

        exit(1)

try:
    raw_sp = pd.read_csv(spfile, usecols =['timestamp', 'data.A1'])

except:

        print("Invalid file!")
        exit(3)

raw_sp.sort_values(by=['timestamp'])
raw_sp.reset_index(inplace=True)
raw_sp['timestamp'] =  pd.to_datetime(raw_sp['timestamp'])
# In[5]:

test_sp=raw_sp
sptimethresh=6

# In[6]:

test_sp=test_sp[['data.A1','timestamp']]

# In[7]:


test_sp['sum']=pd.Series.to_frame(test_sp['data.A1'].rolling(6, center=True).sum())
test_sp['sum_forcleaning']=pd.Series.to_frame(test_sp['data.A1'].rolling(12, center=True).sum())
# In[8]:


# plt.plot(test_sp['timestamp'], test_sp['sum'])
# plt.plot(test_sp['timestamp'], test_sp['data.A1']*10)

# In[9]:
test_sp['idle']=2
printing_delays_raw=scipy.signal.find_peaks(test_sp['sum'], height=(12.25, 15), distance=sptimethresh, width=1)
printing_delays_raw_df=pd.DataFrame({"sample_number":printing_delays_raw[0], "working_time":printing_delays_raw[1]['widths']})
cleaning_delays_raw=scipy.signal.find_peaks(test_sp['sum_forcleaning'], height=60, distance=sptimethresh, width=1)
cleaning_delays_raw_df=pd.DataFrame({"sample_number":cleaning_delays_raw[0], "working_time":cleaning_delays_raw[1]['widths']})

# In[10]:
for index, i in enumerate(printing_delays_raw[0]):
    test_sp.ix[int(printing_delays_raw[1]['left_ips'][index]) : int(printing_delays_raw[1]['right_ips'][index]), 'idle']=0

for index, i in enumerate(cleaning_delays_raw[0]):
    test_sp.ix[int(cleaning_delays_raw[1]['left_ips'][index]) : int(cleaning_delays_raw[1]['right_ips'][index]), 'idle']=0
       


idle_delays_raw=scipy.signal.find_peaks(test_sp['idle'], height=.5, width=1)
idle_delays_raw_df=pd.DataFrame({"sample_number":idle_delays_raw[0], "working_time":idle_delays_raw[1]['widths']})

SP_events=pd.DataFrame({"timestamp":test_sp.iloc[printing_delays_raw_df.sample_number].timestamp, "event":1, "working_time":printing_delays_raw_df.working_time.tolist()})

#remove shot noisy detections
SP_events=SP_events[SP_events['working_time']>=4]


cleanings=pd.DataFrame({"timestamp":test_sp.iloc[cleaning_delays_raw_df.sample_number].timestamp, "event":2, "working_time":cleaning_delays_raw_df.working_time.tolist()})
SP_events.reset_index(inplace=True)
cleanings.reset_index(inplace=True)

idles=pd.DataFrame({"timestamp":test_sp.iloc[idle_delays_raw_df.sample_number].timestamp, "event":0, "working_time":idle_delays_raw_df.working_time.tolist()})
idles.reset_index(inplace=True)

for x, row in SP_events.iterrows():
    SP_events.ix[x,'energy']=test_sp.ix[int(printing_delays_raw[1]['left_ips'][x]):int(printing_delays_raw[1]['right_ips'][x]), 'data.A1'].sum()*230/3600000

# In[11]:

for x, row in cleanings.iterrows():
    cleanings.ix[x,'energy']=test_sp.ix[int(cleaning_delays_raw[1]['left_ips'][x]):int(cleaning_delays_raw[1]['right_ips'][x]), 'data.A1'].sum()*230/3600000



for x, row in idles.iterrows():
    idles.ix[x,'energy']=test_sp.ix[int(idle_delays_raw[1]['left_ips'][x]):int(idle_delays_raw[1]['right_ips'][x]), 'data.A1'].sum()*230/3600000


# In[12]:

SP_events.index=SP_events.timestamp.apply(lambda x: x.isoformat())
SP_events.drop('timestamp', axis=1, inplace=True)
SP_events.drop('index', axis=1, inplace=True)

cleanings.index=cleanings.timestamp.apply(lambda x: x.isoformat())
cleanings.drop('timestamp', axis=1, inplace=True)
cleanings.drop('index', axis=1, inplace=True)


idles.index=idles.timestamp.apply(lambda x: x.isoformat())
idles.drop('timestamp', axis=1, inplace=True)
idles.drop('index', axis=1, inplace=True)



SP_events=SP_events.append(cleanings)
SP_events=SP_events.append(idles)


# In[15]:

# In[16]:
SP_events['device']='screenprinter'
print(SP_events)

timestr = time.strftime("%H-%M")
print('Printing time Mode: ', SP_events.working_time[SP_events['event']==1].mode().mean())
print('Cleaning time Mode: ', SP_events.working_time[SP_events['event']==2].mode().mean())
parameters=open('/home/richard/Desktop/LiveParameters/SPparameters.txt','a+')
parameters.write(timestr +'\tSP printing time mode: ' + str(SP_events.working_time[SP_events['event']==1].mode().mean())+'\n')
parameters.write(timestr +'\tSP cleaning time mode: ' + str(SP_events.working_time[SP_events['event']==2].mode().mean())+'\n')
parameters.close()


if not os.path.exists('/mnt/UltraHD/streamingStates/SP'):

    os.makedirs('/mnt/UltraHD/streamingStates/SP')


# sns.distplot(SP_events.working_time[SP_events['event']==1])
# plt.title('SP Printing Times Histogram')
# plt.savefig("/mnt/UltraHD/streamingStates/SP/SPprinting_hist.png") 
# sns.distplot(SP_events.working_time[SP_events['event']==2])
# plt.title('SP Cleaning Times Histogram')
# plt.savefig("/mnt/UltraHD/streamingStates/SP/SPcleaning_hist.png") 

directory='/mnt/UltraHD/streamingStates/SP'

timestr = time.strftime("%Y-%m-%d_%H-%M-%S")

print("Saving States with file name -", timestr+"_SP.csv")
SP_events.to_csv('/mnt/UltraHD/streamingStates/SP/'+ timestr+"_SP.csv")

#test.to_csv(timestr+"SP.csv")


