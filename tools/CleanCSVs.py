#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import datetime
import json
import pathlib
pd.__version__


# In[2]:


# In[3]:


#Clean Screenprinter CSV
try:
    sp=pd.read_csv("data/screenprinter_plus_vaf.csv")

    sp.timestamp=pd.to_datetime(sp.timestamp)
    sp_start=sp.ix[0, 'timestamp']
    sp_end=sp.iloc[-1]
    sp_end=sp_end.timestamp

    last_tail=pathlib.Path("sp_last_time.txt")
    if last_tail.exists():
        f = open("sp_last_time.txt","r")
        last=f.read()
        try:
            last=datetime.datetime.strptime(last, '%Y-%m-%d %H:%M:%S.%f')
            if last<sp_end and last>sp_start:
                sp_start=last
    #             sp_end=sp_start + datetime.timedelta(minutes=15)
        except:
            sp_end=sp_start + datetime.timedelta(minutes=15)
    else:
        sp_end=sp_start + datetime.timedelta(minutes=15)

    f = open("sp_last_time.txt","w")
    f.write(sp_end.strftime("%Y-%m-%d %H:%M:%S.%f"))

    sp_new=sp.loc[(sp.timestamp >= sp_start) & (sp.timestamp <= sp_end)]
    sp_new.index=sp_new.timestamp
    sp_new.drop('timestamp', axis=1, inplace=True)
    sp_new.to_csv("data/screenprinter.csv")
except:
    print("Screenprinter splicing failed")

# In[4]:

# In[5]:


#Clean Loader CSV
try:
    ld=pd.read_csv("data/loader.csv")

    ld.timestamp=pd.to_datetime(ld.timestamp)
    ld_start=ld.ix[0, 'timestamp']
    ld_end=ld.iloc[-1]
    ld_end=ld_end.timestamp

    last_tail=pathlib.Path("ld_last_time.txt")
    if last_tail.exists():
        f = open("ld_last_time.txt","r")
        last=f.read()
        try:
            last=datetime.datetime.strptime(last, '%Y-%m-%d %H:%M:%S.%f')
            if last<ld_end and last>ld_start:
                ld_start=last
                ld_end=ld_start + datetime.timedelta(minutes=15)
        except:
            ld_end=ld_start + datetime.timedelta(minutes=15)
    else:
        ld_end=ld_start + datetime.timedelta(minutes=15)

    f = open("ld_last_time.txt","w")
    f.write(ld_end.strftime("%Y-%m-%d %H:%M:%S.%f"))    
    ld_new=ld.loc[(ld.timestamp >= ld_start) & (ld.timestamp <= ld_end)]
    ld_new.index=ld_new.timestamp
    ld_new.drop('timestamp', axis=1, inplace=True)
    ld_new.to_csv("data/loader.csv")
except:
    print("Loader splicing failed")

# In[ ]:


# sp_new=pd.read_csv("data/screenprinter_new.csv")


# In[33]:


#Clean PP1 CSV
try:
    pp1=pd.read_csv("data/pickandplace1.csv")

    pp1.timestamp=pd.to_datetime(pp1.timestamp)
    pp1_start=pp1.ix[0, 'timestamp']
    pp1_end=pp1.iloc[-1]
    pp1_end=pp1_end.timestamp

    last_tail=pathlib.Path("pp1_last_time.txt")
    if last_tail.exists():
        f = open("pp1_last_time.txt","r")
        last=f.read()
        try:
            last=datetime.datetime.strptime(last, '%Y-%m-%d %H:%M:%S.%f')
            if last<pp1_end and last>pp1_start:
                pp1_start=last
    #             pp1_end=pp1_start + datetime.timedelta(minutes=15)
                try:
                	gpp1=pp1.groupby(['data.proximity'], as_index=False).last()
                	pp1_end=gpp1[gpp1['data.proximity']==0]['timestamp'].iloc[0] - datetime.timedelta(seconds=5)
                except:
                	print("Proximity data not helpful. Sending entire csv..")
        except:
    #         pp1_end=pp1_start + datetime.timedelta(minutes=15)
            try:
            	gpp1=pp1.groupby(['data.proximity'], as_index=False).last()
            	pp1_end=gpp1[gpp1['data.proximity']==0]['timestamp'].iloc[0] - datetime.timedelta(seconds=5)
            except:
            	print("Proximity data not helpful. Sending entire csv..")
    else:
        try:
        	gpp1=pp1.groupby(['data.proximity'], as_index=False).last()
        	pp1_end=gpp1[gpp1['data.proximity']==0]['timestamp'].iloc[0] - datetime.timedelta(seconds=5)
        except:
        	print("Proximity data not helpful. Sending entire csv..")

    f = open("pp1_last_time.txt","w")
    f.write(pp1_end.strftime("%Y-%m-%d %H:%M:%S.%f"))

    pp1_new=pp1.loc[(pp1.timestamp >= pp1_start) & (pp1.timestamp <= pp1_end)]
    pp1_new.index=pp1_new.timestamp
    pp1_new.drop('timestamp', axis=1, inplace=True)
    pp1_new.to_csv("data/pickandplace1.csv")
except:
    print("Pickandplace1 splicing failed")


# In[34]:

# In[6]:


#Clean PP2 CSV
try:
    pp2=pd.read_csv("data/pickandplace2.csv")
    pp2.timestamp=pd.to_datetime(pp2.timestamp)
    pp2_start=pp2.ix[0, 'timestamp']
    pp2_end=pp2.iloc[-1]
    pp2_end=pp2_end.timestamp

    last_tail=pathlib.Path("pp2_last_time.txt")
    if last_tail.exists():
        f = open("pp2_last_time.txt","r")
        last=f.read()
        try:
            last=datetime.datetime.strptime(last, '%Y-%m-%d %H:%M:%S.%f')
            if last<pp2_end and last>pp2_start:
                pp2_start=last
    #             pp2_end=pp2_start + datetime.timedelta(minutes=15)
                try:
                	gpp2=pp2.groupby(['data.proximity'], as_index=False).last()
                	pp2_end=gpp2[gpp2['data.proximity']==1]['timestamp'].iloc[0] + datetime.timedelta(seconds=5)
                except:
                	print("Proximity data not helpful. Sending entire csv..")
        except:
    #         pp2_end=pp2_start + datetime.timedelta(minutes=15)
            try:
            	gpp2=pp2.groupby(['data.proximity'], as_index=False).last()
            	pp2_end=gpp2[gpp2['data.proximity']==1]['timestamp'].iloc[0] + datetime.timedelta(seconds=5)
            except:
            	print("Proximity data not helpful. Sending entire csv..")
    else:
    #     sp_end=sp_start + datetime.timedelta(minutes=15)
        try:
        	gpp2=pp2.groupby(['data.proximity'], as_index=False).last()
        	pp2_end=gpp2[gpp2['data.proximity']==1]['timestamp'].iloc[0] + datetime.timedelta(seconds=5)
        except:
        	print("Proximity data not helpful. Sending entire csv..")

    f = open("pp2_last_time.txt","w")
    f.write(pp2_end.strftime("%Y-%m-%d %H:%M:%S.%f"))
    pp2_new=pp2.loc[(pp2.timestamp >= pp2_start) & (pp2.timestamp <= pp2_end)]
    pp2_new.index=pp2_new.timestamp
    pp2_new.drop('timestamp', axis=1, inplace=True)
    pp2_new.to_csv("data/pickandplace2.csv")

except:
    print("Pickandplace2 splicing failed")

# In[8]:

# In[ ]:




