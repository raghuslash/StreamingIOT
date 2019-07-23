#!/usr/bin/env python
# coding: utf-8

# In[1]:

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import scipy.signal
import numpy as np
import seaborn as sns
import time
import datetime
if len(sys.argv) <  2:

        print("No filename passed. Place the CSV file in the same folder.")

        exit(2)

ldfile=sys.argv[1]

if not os.path.isfile(ldfile):

        print("File not found!")

#         exit(1)

try:
        
         loader_raw=pd.read_csv(ldfile, usecols=['timestamp', 'data.ax', 'data.az'])

except:

        print("Invalid file!")
        exit(2)

# In[2]:


# loader_raw=pd.read_csv("data/05-03/loader.csv", usecols=['timestamp','data.ax','data.az'])
loader_raw.dropna(axis=0, inplace=True)
loader_raw.timestamp=pd.to_datetime(loader_raw.timestamp)


# In[3]:


loader_raw.acc=(loader_raw["data.ax"]**2+loader_raw["data.az"]**2)**0.5
loader_raw.timestamp=loader_raw.timestamp + datetime.timedelta(hours=5, minutes=30)


# In[4]:


#get_ipython().run_line_magic('matplotlib', '')


# In[5]:


# plt.plot(loader_raw.timestamp, loader_raw.acc, 'red')


# In[6]:


loader_raw.acc_std=pd.Series.to_frame(loader_raw.acc.rolling(150, center=True).std())


# In[7]:


loader_raw['acc_std_sum']=loader_raw.acc_std.rolling(1350,  win_type='triang', center=True).sum()


# In[8]:


loader_raw['acc_std_sum']=loader_raw.acc_std_sum.rolling(1350, center=True).mean()


# In[9]:


# plt.plot(loader_raw.timestamp, loader_raw.acc)
# plt.plot(loader_raw.timestamp_ist, loader_raw.acc_mean_again)
# plt.plot(loader_raw.timestamp, loader_raw.acc_std_sum)


# In[10]:


ldr_refill=scipy.signal.find_peaks(loader_raw['acc_std_sum'], height=(7,13), width=3)


# In[11]:


ldr_stack=scipy.signal.find_peaks(loader_raw['acc_std_sum'], height=(13), width=3)


# In[12]:


ldr_refill_df=pd.DataFrame({"sample_number":ldr_refill[0], "event":1})


# In[13]:


ldr_stack_df=pd.DataFrame({"sample_number":ldr_stack[0], "event":2})


# In[21]:


ldr_refill_events=pd.DataFrame({"timestamp":loader_raw.iloc[ldr_refill_df.sample_number].timestamp, "anomalous_event":1, "device":"loader"})


# In[22]:


ldr_stack_events=pd.DataFrame({"timestamp":loader_raw.iloc[ldr_stack_df.sample_number].timestamp, "anomalous_event":2, "device":"loader"})


# In[23]:


# plt.plot(loader_raw.timestamp, loader_raw.acc, 'r')
# plt.stem(ldr_refill_events.timestamp, ldr_refill_events.event*0.5)
# plt.stem(ldr_stack_events.timestamp, ldr_stack_events.event*0.5)


# In[24]:


LD_ano_events=pd.concat([ldr_refill_events, ldr_stack_events])
LD_ano_events.index=LD_ano_events.timestamp
LD_ano_events.drop('timestamp', axis=1, inplace=True)

# In[ ]:


if not os.path.exists('/mnt/UltraHD/streamingAno/LD'):

    os.makedirs('/mnt/UltraHD/streamingAno/LD')

# sns.distplot(LD_events.working_time)
# plt.title('Loader Loading Times Histogram')
#plt.savefig("/mnt/UltraHD/streamingStates/LD/LDboards_hist.png") 

directory='/mnt/UltraHD/streamingAno/LD'


timestr = time.strftime("%Y-%m-%d_%H-%M-%S")
print("Saving Anomalous events with file name -", timestr+"_LD.csv")
LD_ano_events.to_csv('/mnt/UltraHD/streamingAno/LD/'+ timestr+"_LD.csv")

