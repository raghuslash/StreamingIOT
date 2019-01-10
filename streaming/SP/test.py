
# coding: utf-8

# In[1]:


import pandas as pd
import os
import sys
import time


# In[2]:


import matplotlib.pyplot as plt


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
        
        test = pd.read_csv(spfile, usecols =['timestamp', 'data.A1'])

except:

        print("Invalid file!")
        exit(3)
#only one phase for sp

test.dropna(inplace=True)
# In[5]:

#test=raw.head(60*mins)
#test.index=test['timestamp']
#test.to_csv('sp_head.csv', index=False)



# In[6]:


#test=pd.read_csv('sp_head.csv')
#test.plot()
#plt.margins(0)


# In[7]:


import scipy.signal
import numpy as np


# In[8]:


test=test[['data.A1','timestamp']]
events=scipy.signal.find_peaks(test['data.A1'], height=(2.75), width=1)
# test['data.A1']


# In[9]:


#plt.scatter(events[0], events[1]['peak_heights'], color='r', marker='o')
#plt.stem(events[0], events[1]['peak_heights'])
#plt.xlim(xmin = 0)

# In[10]:


test.insert(2,'state',0)
sampleno=0
if len(events[0])>0:
	for x in events[0]:
		if test.ix[x, 'data.A1'] < 5:
			test.at[x, 'state'] = 1
		elif test.ix[x, 'data.A1'] > 9:
			test.at[x, 'state'] = 2


# In[11]:


test.plot()
plt.xlim(xmin = 0)

plt.title('Screenprinter  States')
#plt.show()
plt.savefig('/mnt/UltraHD/streamingStates/SP/SPStates.png')
plt.savefig('SPStates.png')
# In[12]:


test['state'].value_counts()
print(len(test.query('state == 1')), 'boards found.')


# In[15]:


test.drop('data.A1', axis=1, inplace=True)
test.index = test["timestamp"]
test.drop("timestamp",axis=1, inplace=True)

test['device']='screenprinter'
print(test)

# In[16]:

if not os.path.exists('/mnt/UltraHD/streamingStates/SP'):

    os.makedirs('/mnt/UltraHD/streamingStates/SP')



directory='/mnt/UltraHD/streamingStates/SP'


import time

timestr = time.strftime("%Y-%m-%d_%H-%M-%S")

print("Saving States with file name -", timestr+"SP.csv")

test.to_csv('/mnt/UltraHD/streamingStates/SP/'+ timestr+"SP.csv")

#test.to_csv(timestr+"SP.csv")


