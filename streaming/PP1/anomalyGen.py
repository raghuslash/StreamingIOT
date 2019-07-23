#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy
import scipy.signal
import seaborn
import datetime
import pandas_helper_calc
import os
import sys
import time
import csv

# In[2]:
pp1_raw=pd.read_csv("PP1_Processed_DataFrame.csv", usecols=['timestamp','quant_sig'])
pp1_raw.dropna(axis=0, inplace=True)
pp1_raw.timestamp=pd.to_datetime(pp1_raw.timestamp)
# pp1_raw['acc']=(pp1_raw["data.ax"]**2+pp1_raw["data.az"]**2)**0.5
# pp1_raw.timestamp=pp1_raw.timestamp + datetime.timedelta(hours=5, minutes=30)


# In[3]:


pp1_raw.rename({"quant_sig":"acc"}, axis=1, inplace=True)


# In[4]:


pp1_processed=pd.read_csv("PP1_Processed_DataFrame.csv", usecols=['timestamp', 'mrg_binry_sig'])
pp1_processed.dropna(axis=0, inplace=True)
pp1_processed.timestamp=pd.to_datetime(pp1_processed.timestamp)
# pp1_processed.timestamp=pp1_processed.timestamp + datetime.timedelta(hours=5, minutes=30)


# In[5]:


pp1_raw.sort_values('timestamp', axis=0, inplace=True)
pp1_processed.sort_values('timestamp', axis=0, inplace=True)


# In[6]:


# print(pp1_raw.shape[0], pp1_processed.shape[0])


# In[7]:


# get_ipython().run_line_magic('matplotlib', '')


# In[8]:


#plt.plot(pp1_raw.timestamp, pp1_raw.acc)
#plt.plot(pp1_processed.timestamp, pp1_processed.mrg_binry_sig)


# In[9]:


# pp1_raw=pp1_raw[(pp1_raw['timestamp'] >= pp1_processed['timestamp'][0]) & (pp1_raw['timestamp'] <= pp1_processed.iloc[-1].timestamp)]


# In[10]:


# pp1_raw.reset_index(inplace=True)
# pp1_raw.drop('index', axis=1, inplace=True)


# In[11]:


# print(pp1_raw.shape[0], pp1_processed.shape[0])


# In[12]:


downtimes=pp1_raw.copy()
downtimes['mrg_binry_sig']=pp1_processed['mrg_binry_sig']


# In[13]:


downtimes['inv_binry_sig']=0
downtimes.loc[downtimes['mrg_binry_sig']!=1,['inv_binry_sig']]=1


# In[14]:


idle_dur=scipy.signal.find_peaks(downtimes['inv_binry_sig'], height=(0.5), width=1)
idle_dur_df=pd.DataFrame({"timestamp":downtimes.iloc[idle_dur[0]].timestamp, "duration":idle_dur[1]['widths']/75 , "left_ips":idle_dur[1]['left_ips'], "right_ips":idle_dur[1]['right_ips']})


# In[15]:


between_boards_df=idle_dur_df[idle_dur_df['duration']<15]


# In[16]:


for x, row in between_boards_df.iterrows():
    downtimes.loc[int(row.left_ips):int(row.right_ips), ['acc']]=0


# In[17]:


for x, row in idle_dur_df.iterrows():
    downtimes.loc[int(row.left_ips):int(row.left_ips)+75, ['acc']]=0
    downtimes.loc[int(row.right_ips)-75:int(row.right_ips), ['acc']]=0


# In[18]:


# downtimes.loc[378]['acc']


# In[19]:


downtimes.loc[downtimes['mrg_binry_sig']==1,['acc']]=0


# In[20]:


# downtimes


# In[21]:


# import dill
# dill.dump_session('anomaly_cp1.dat')


# In[22]:


# import dill
# dill.load_session('anomaly_cp1.dat')


# In[23]:


# get_ipython().run_line_magic('matplotlib', '')


# In[24]:


# plt.plot(downtimes.timestamp, downtimes.acc)


# In[25]:


# plt.plot(pp1_raw.timestamp, pp1_raw.acc+0.5)


# In[26]:


# plt.plot(pp1_processed.timestamp, pp1_processed.mrg_binry_sig)


# In[27]:


# downtimes.index=downtimes.timestamp
# downtimes.drop('timestamp', axis=1, inplace=True)


# In[28]:


# downtimes.index


# In[29]:


#Use for PP1
downtimes['sum']=pd.Series.to_frame(downtimes['acc'].rolling(75*2, center=True).std())
# downtimes['sum']=pd.Series.to_frame(downtimes['acc'].rolling(75*0, center=True).sum())
downtimes['sum']=(downtimes['sum']-downtimes['sum'].mean())/downtimes['sum'].mean()
refills=scipy.signal.find_peaks(downtimes['sum'], height=(24,60), width=1, distance=5*75)
restarts=scipy.signal.find_peaks(downtimes['sum'], height=(70), width=1, distance=20*75)
refills_df=pd.DataFrame({"timestamp":downtimes.iloc[refills[0]].timestamp, 'anomalous_event':1, 'device':'pickandplace1'})
restarts_df=pd.DataFrame({"timestamp":downtimes.iloc[restarts[0]].timestamp, 'anomalous_event':2, 'device':'pickandplace1'})



# In[30]:


PP1_ano_events=pd.concat([refills_df, restarts_df])
PP1_ano_events.index=PP1_ano_events.timestamp.apply(lambda x: x.isoformat())
PP1_ano_events.drop('timestamp', axis=1, inplace=True)
# In[ ]:


if not os.path.exists('/mnt/UltraHD/streamingAno/PP1'):

    os.makedirs('/mnt/UltraHD/streamingAno/PP1')

# sns.distplot(LD_events.working_time)
# plt.title('Loader Loading Times Histogram')
#plt.savefig("/mnt/UltraHD/streamingStates/LD/LDboards_hist.png") 

directory='/mnt/UltraHD/streamingAno/PP1'


timestr = time.strftime("%Y-%m-%d_%H-%M-%S")
print("Saving Anomalous events with file name -", timestr+"_PP1.csv")
PP1_ano_events.to_csv('/mnt/UltraHD/streamingAno/PP1/'+ timestr+"_PP1.csv")
#Use for PP2
# downtimes['sum']=pd.Series.to_frame(downtimes['acc'].rolling(75*3, center=True).std())
# downtimes['sum']=pd.Series.to_frame(downtimes['acc'].rolling(75*70, center=True).std())
# downtimes['sum']=pd.Series.to_frame(downtimes['acc'].rolling(30, center=True).sum())
# downtimes['sum']=(downtimes['sum']-downtimes['sum'].mean())/downtimes['sum'].mean()
# downtimes['sum']=pd.Series.to_frame(downtimes['sum'].rolling(30,center=True).mean())
# refills=scipy.signal.find_peaks(downtimes['sum'], height=(20,30), width=1, distance=5*75)
# restarts=scipy.signal.find_peaks(downtimes['sum'], height=(40), width=1, distance=20*75)
# refills_df=pd.DataFrame({"timestamp":downtimes.iloc[refills[0]].timestamp, 'a_event':1})
# restarts_df=pd.DataFrame({"timestamp":downtimes.iloc[restarts[0]].timestamp, 'a_event':2})


# In[31]:


# plt.plot(downtimes.timestamp, downtimes['sum'])
# plt.plot(pp1_raw.timestamp, pp1_raw.acc*40, 'orange')
# plt.plot(downtimes.timestamp, downtimes.acc, 'blue')
# plt.stem(refills_df.timestamp, refills_df.a_event*20, 'red')
# plt.stem(restarts_df.timestamp, restarts_df.a_event*20, 'green')
# plt.plot(downtimes.timestamp, downtimes.mrg_binry_sig, 'green')
# plt.plot(downtimes.timestamp, downtimes.inv_binry_sig)


# In[ ]:





# In[ ]:




