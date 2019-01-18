import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.dates as mdates
import os
import sys
import time
import scipy.signal





if len(sys.argv) <  2:

	print("No filename passed. Place the CSV file in the same folder.")

	exit(2)

rffile=sys.argv[1]

if not os.path.isfile(rffile):

	print("File not found!")

	exit(1)

try:

	rf_raw=pd.read_csv(rffile, usecols =['timestamp', 'data.A1', 'data.A2', 'data.A3'])

except:

	print("Invalid file!")


rf_raw.dropna(inplace=True, axis=0)
rf_raw.sort_values(by=['timestamp'], inplace=True)
rf_raw.reset_index(inplace=True)

rf_raw.index=rf_raw.timestamp

rf_raw['total_current']=rf_raw['data.A1']+rf_raw['data.A2']+rf_raw['data.A3']
rf_raw['rolling_mean_p1']=pd.Series.to_frame(rf_raw['data.A1'].rolling(10, center=True).mean())
rf_raw['state']=0


rf_raw['state'][rf_raw['rolling_mean_p1']<=1.5]=0
rf_raw['state'][rf_raw['rolling_mean_p1']>= 35]=2
rf_raw['state'][(rf_raw['rolling_mean_p1']>1.5) & (rf_raw['rolling_mean_p1']<=35)]=1

rf_raw.ix[0, 'state']=(rf_raw.ix[0, 'state']+1)%3
rf_raw.ix[-1, 'state']=(rf_raw.ix[0, 'state']+1)%3

heating_times=scipy.signal.find_peaks(rf_raw.state, height=1.5, width=1)
heating_times_df=pd.DataFrame({"sample_number":heating_times[0], "working_time":heating_times[1]['widths']})

idle_temp=rf_raw[['state']]*-1
idle_times=scipy.signal.find_peaks(idle_temp.state, height=-.5, width=1)
idle_times_df=pd.DataFrame({"sample_number":idle_times[0], "working_time":idle_times[1]['widths']})

maintain_temp=rf_raw[['state']]
maintain_temp['state'][rf_raw.state==2]=0
maintain_times=scipy.signal.find_peaks(maintain_temp.state, height=.5, width=1)
maintain_times_df=pd.DataFrame({"sample_number":maintain_times[0], "working_time":maintain_times[1]['widths']})

for x, row in heating_times_df.iterrows():
    heating_times_df.ix[x,'start_time']=rf_raw.iloc[int(heating_times[1]['left_ips'][x])].timestamp
    heating_times_df.ix[x,'end_time']=rf_raw.iloc[int(heating_times[1]['right_ips'][x])].timestamp
    heating_times_df.ix[x,'timestamp']=rf_raw.iloc[int(heating_times[0][x])].timestamp
    heating_times_df.ix[x,'state']=rf_raw.iloc[int(heating_times[0][x])].state
    
for x, row in maintain_times_df.iterrows():
    maintain_times_df.ix[x,'start_time']=rf_raw.iloc[int(maintain_times[1]['left_ips'][x])].timestamp
    maintain_times_df.ix[x,'end_time']=rf_raw.iloc[int(maintain_times[1]['right_ips'][x])].timestamp
    maintain_times_df.ix[x,'timestamp']=rf_raw.iloc[int(maintain_times[0][x])].timestamp
    maintain_times_df.ix[x,'state']=rf_raw.iloc[int(maintain_times[0][x])].state
    
for x, row in idle_times_df.iterrows():
    idle_times_df.ix[x,'start_time']=rf_raw.iloc[int(idle_times[1]['left_ips'][x])].timestamp
    idle_times_df.ix[x,'end_time']=rf_raw.iloc[int(idle_times[1]['right_ips'][x])].timestamp
    idle_times_df.ix[x,'timestamp']=rf_raw.iloc[int(idle_times[0][x])].timestamp
    idle_times_df.ix[x,'state']=rf_raw.iloc[int(idle_times[0][x])].state


heating_times_df['energy'] = heating_times_df.apply(lambda x: rf_raw.loc[(rf_raw.timestamp <= x.end_time) & 
                                                            (x.start_time <= rf_raw.timestamp),
                                                            ['total_current']].sum()*230/3600000, axis=1)
maintain_times_df['energy'] = maintain_times_df.apply(lambda x: rf_raw.loc[(rf_raw.timestamp <= x.end_time) & 
                                                            (x.start_time <= rf_raw.timestamp),
                                                            ['total_current']].sum()*230/3600000, axis=1)
idle_times_df['energy'] = idle_times_df.apply(lambda x: rf_raw.loc[(rf_raw.timestamp <= x.end_time) & 
                                                            (x.start_time <= rf_raw.timestamp),
                                                            ['total_current']].sum()*230/3600000, axis=1)


RF_states=heating_times_df[['timestamp', 'state', 'working_time', 'energy']]
RF_states=RF_states.append(maintain_times_df[['timestamp', 'state', 'working_time', 'energy']])
RF_states=RF_states.append(idle_times_df[['timestamp', 'state', 'working_time', 'energy']])




RF_states.index=RF_states.timestamp
RF_states.drop('timestamp', axis=1, inplace=True)
RF_states['device']='reflowoven'
print(RF_states)



if not os.path.exists('/mnt/UltraHD/streamingStates/RF'):

    os.makedirs('/mnt/UltraHD/streamingStates/RF')



directory='/mnt/UltraHD/streamingStates/RF'



import time

timestr = time.strftime("%Y-%m-%d_%H-%M-%S")

print("Saving States with file name - ", timestr+'_RF.csv')

RF_states.to_csv('/mnt/UltraHD/streamingStates/RF/'+ timestr+"_RF.csv")



