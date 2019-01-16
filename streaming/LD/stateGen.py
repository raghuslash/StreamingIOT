
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


# In[2]:


# import matplotlib.pyplot as plt


# In[3]:


# plt.rcParams["figure.figsize"]=[15,5]
if len(sys.argv) <  2:

        print("No filename passed. Place the CSV file in the same folder.")

        exit(2)

ldfile=sys.argv[1]

if not os.path.isfile(ldfile):

        print("File not found!")

#         exit(1)

try:
        
         raw_ld=pd.read_csv(ldfile, usecols=['timestamp', 'data.ax', 'data.az'])

except:

        print("Invalid file!")
        exit(2)

# In[4]:


raw_ld.sort_values(by=['timestamp'], inplace=True)
raw_ld.reset_index(inplace=True)
raw_ld.dropna(axis=0, inplace=True)

# In[6]:


raw_ld["acc"] = ( raw_ld["data.ax"]**2 + raw_ld["data.az"]**2 ) ** 0.5
acc=raw_ld[["timestamp", "acc"]]
acc.set_index('timestamp')
test_ld=acc
test_ld['acc']=pd.Series.to_frame(test_ld.acc.rolling(100, center=True).std())
test_ld['timestamp'] =  pd.to_datetime(test_ld['timestamp'])

# In[7]:


timethresh=12

# In[11]:



import scipy.signal
import numpy as np


# In[12]:



#board=scipy.signal.find_peaks(test.acc,height=(0.016), width=3)
board=scipy.signal.find_peaks(test_ld.acc, height=(0.01), distance=timethresh*72, width=1)
differ=np.diff(board[0])
differ=differ.tolist()


# In[21]:

loading_delays_rawdf=pd.DataFrame({"sample_number":board[0], "working_time":board[1]['widths']/72})
LD_events=pd.DataFrame({"timestamp":test_ld.iloc[loading_delays_rawdf.sample_number].timestamp, "event":1, "working_time":(loading_delays_rawdf.working_time).tolist()})

# In[22]:

LD_events.index=LD_events.timestamp
LD_events.drop('timestamp', axis=1, inplace=True)
LD_events['energy']=float('nan')

LD_events['device']='loader'
print(LD_events)

# In[ ]:

timestr = time.strftime("%H-%M")
print('LD loading time mode: ', LD_events.working_time.mode().mean())
parameters=open('/home/richard/Desktop/LiveParameters/LDparameters.txt','a+')
parameters.write(timestr +'\tLD loading time mode: ' + str(LD_events.working_time.mode().mean())+'\n')
parameters.close()
# In[24]:

if not os.path.exists('/mnt/UltraHD/streamingStates/LD'):

    os.makedirs('/mnt/UltraHD/streamingStates/LD')

# sns.distplot(LD_events.working_time)
# plt.title('Loader Loading Times Histogram')
#plt.savefig("/mnt/UltraHD/streamingStates/LD/LDboards_hist.png") 

directory='/mnt/UltraHD/streamingStates/LD'


timestr = time.strftime("%Y-%m-%d_%H-%M-%S")
print("Saving States with file name -", timestr+"_LD.csv")
LD_events.to_csv('/mnt/UltraHD/streamingStates/LD/'+ timestr+"_LD.csv")

