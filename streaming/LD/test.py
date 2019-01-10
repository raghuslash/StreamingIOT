
# coding: utf-8

# In[1]:


import pandas as pd
import os
import sys


# In[2]:


import matplotlib.pyplot as plt


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
        
         raw=pd.read_csv(ldfile, usecols=['timestamp', 'data.ax', 'data.ay', 'data.az'])

except:

        print("Invalid file!")
        exit(2)

# In[4]:

raw.dropna(inplace=True)
raw["acc"]=( raw["data.ax"]**2 + raw["data.az"]**2 ) ** 0.5

# In[6]:


acc=raw[["timestamp", "acc"]]
acc.set_index('timestamp')
# acc.head()


# In[7]:



test=acc
test['acc']=pd.Series.to_frame(test.acc.rolling(75, center=True).std())


# In[11]:


import scipy.signal
import numpy as np


# In[12]:



board=scipy.signal.find_peaks(test.acc,height=(0.015), width=75)

# In[19]:




# In[20]:


boards=[]
differ=np.diff(board[0])
differ=differ.tolist()

# differ


# In[21]:


# binwidth=200
# plt.hist(differ, bins=np.arange(min(differ), max(differ) + binwidth, binwidth))
# print(np.percentile(differ, 30))


# In[22]:


test.insert(2,'state',0)
boards=[]
if len(board[0]) > 0:
	boards.append(board[0][0])
	for i, x in enumerate(board[0]):
    		try:
        		if differ[i]>5000:
           			#print(x)
            			boards.append(board[0][i+1])
            			test.at[x, 'state']=1
        		else:
            			test.at[x, 'state']=2
    		except:
        		continue

# In[ ]:


# In[ ]:


test.plot()
plt.margins(0)
plt.savefig("/mnt/UltraHD/streamingStates/LD/LDStates.png") 
plt.savefig("LDStates.png")
# In[ ]:


print(len(boards), 'boards found.')


# In[24]:

if not os.path.exists('/mnt/UltraHD/streamingStates/LD'):

    os.makedirs('/mnt/UltraHD/streamingStates/LD')



directory='/mnt/UltraHD/streamingStates/LD'


test.dropna(how='all', axis=1)
test.drop('acc', axis=1, inplace=True)
test.index = test["timestamp"]
test.drop("timestamp",axis=1, inplace=True)


test['device']='loader'
print(test)
import time

timestr = time.strftime("%Y-%m-%d_%H-%M-%S")
print("Saving States with file name -", timestr+"LD.csv")
test.to_csv('/mnt/UltraHD/streamingStates/LD/'+ timestr+"LD.csv")
#test.to_csv(timestr+"LD.csv")

