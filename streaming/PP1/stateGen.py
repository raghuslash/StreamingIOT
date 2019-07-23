#PP1 PCB Detection and Merging

#Import the libraries
import pandas as pd
import numpy as np
import scipy as sp

import os
import sys
import time

import csv
import datetime

import importlib

from matplotlib import pyplot as plt
from matplotlib import dates  as md 
from matplotlib.colors import LogNorm

#-------------------------------------------------
#Import routines
import routine_rawaccl_to_binryseq  
import routine_get_pcb_dur          
import routine_elim_spur_pcb        
import routine_get_pcb_level_data   
import routine_merging_algo         
import routine_merge_pxmty_algo  

#----------------------------------------------------
#Get the data from pp1 csv file
# pp1file = pd.read_csv('csv_folders/helloworld-2019-03-01/pickandplace1.csv')

###ADDITIONS FOR STREAMING STATES###########
if len(sys.argv) <  2:

        print("No filename passed. Place the CSV file in the same folder.")

        exit(2)

ppfile=sys.argv[1]

if not os.path.isfile(ppfile):

        print("File not found!")

        exit(1)

try:
    pp1file = pd.read_csv(ppfile)
    raw_pp_current=pd.read_csv(ppfile, usecols=['timestamp', 'data.A1', 'data.A2', 'data.A3'])
except:
        print("Invalid file!")
        exit(3)

###END OF ADDITIONS FOR STREAMING STATES###########

pp1file.columns = [c.replace('.', '_') for c in pp1file.columns]

#PP1 Proximity sensor data
pp1_pxstr_file = pp1file.query('deviceid == "pickandplace1_proximity_entry"').loc[:,['datatype','timestamp','deviceid','data_proximity']]
pp1_pxstr_file = pp1_pxstr_file.sort_values(by="timestamp")
pp1_pxstr_file = pp1_pxstr_file.reset_index()
pp1_pxstr_file = pp1_pxstr_file.iloc[:,1:len(pp1_pxstr_file.columns)]

#PP1 Vibration sensor data
pp1_vibr_file = pp1file.query('deviceid == "pickandplace1_vibration"').loc[:,['datatype','timestamp','deviceid','data_ax','data_ay','data_az']]
pp1_vibr_file = pp1_vibr_file.sort_values(by="timestamp")
pp1_vibr_file = pp1_vibr_file.reset_index()
pp1_vibr_file = pp1_vibr_file.iloc[:,1:len(pp1_vibr_file.columns)]
pp1_vibr_file = pp1_vibr_file.assign(net_accl = np.sqrt(pp1_vibr_file.data_ax**2 + pp1_vibr_file.data_ay**2 + pp1_vibr_file.data_az**2))

print('Size of pp1_pxstr_file =', pp1_pxstr_file.shape)
print('Size of pp1_vibr_file  =', pp1_vibr_file.shape)

#-------------------------------------------------------------------------
#Raw-acceleration to binary sequene conversion
filt_sig_pp1 = routine_rawaccl_to_binryseq.rawaccl_to_binryseq(pp1_vibr_file,1,'Y','Y',0.25,0.8)

#Detect PCBs and obtain PCB processing durations
pcb_data_pp1 = routine_get_pcb_dur.get_pcb_dur(filt_sig_pp1.binry_sig)

#Eliminate spuriois PCB detections
filt_sig_pp1['cor_binry_sig'] = routine_elim_spur_pcb.elim_spur_pcb(filt_sig_pp1.binry_sig,pcb_data_pp1,250)

#Recalculate PCB processing durations
pcb_data_pp1 = routine_get_pcb_dur.get_pcb_dur(filt_sig_pp1.cor_binry_sig)

#Obtain PCB level dataframe with weightages
pcb_level_pp1 = routine_get_pcb_level_data.get_pcb_level_data(filt_sig_pp1,pcb_data_pp1,50)

#-----------------------------------------------------------------------------------------------------------------------
#Merging process 
pcb_merge_pp1 = pcb_level_pp1
mrg_binry_pp1 = filt_sig_pp1.cor_binry_sig

THRESHOLD = 0.95
HIGH_END  = 1.50

iter_one = 0
iter_two = 0

PROC_ONE_END_FLAG = 0
while (PROC_ONE_END_FLAG == 0):
    
    iter_one = iter_one + 1
    print('PROC-ONE-ITERATION :', iter_one)
    
    pcb_merge_pp1,mrg_binry_pp1,no_of_merged_pcbs = routine_merge_pxmty_algo.merge_pxmty_algo    \
    (inp_df        = pcb_merge_pp1                                      \
    ,pxmty_df      = pp1_pxstr_file      \
    ,inp_binry_sig = mrg_binry_pp1                         \
    ,THRESHOLD     = THRESHOLD                                               \
    ,HIGH_END      = HIGH_END                                                \
    )
    
    if (no_of_merged_pcbs == 0):
        PROC_ONE_END_FLAG = 1
    #end-if
    
    print ('=============================================')
    
#end-while

PROC_TWO_END_FLAG = 0
while(PROC_TWO_END_FLAG == 0):
    
    iter_two = iter_two + 1
    print('PROC-TWO-ITERATION :', iter_two)
    
    pcb_merge_pp1,mrg_binry_pp1,no_of_merged_pcbs = routine_merging_algo.merging_algo  \
    (inp_df        = pcb_merge_pp1                                   \
    ,inp_binry_sig = mrg_binry_pp1                                   \
    ,THRESHOLD     = THRESHOLD                                            \
    ,HIGH_END      = HIGH_END                                             \
    ) 
    
    if(no_of_merged_pcbs == 0):
        PROC_TWO_END_FLAG = 1
    #end-if
    
    print ('=============================================')
    
#end-while

filt_sig_pp1['mrg_binry_sig'] = mrg_binry_pp1

#-----------------------------------------------------------------------------------------------------------
#Write processed info to csv file
filt_sig_pp1.to_csv('PP1_Processed_DataFrame.csv')
pcb_merge_pp1.to_csv('PP1_PCB_Merged_DataFrame.csv')
pcb_merge_pp1=pcb_merge_pp1[pcb_merge_pp1.weightage > 0.5]
pcb_merge_pp1.to_csv('PP1_PCB_Merged_Corrected_DataFrame.csv')
pp1_pxstr_file.to_csv('PP1_Proximity_Entry_DataFrame.csv')
#-----------------------------------------------------------------------------




###ADDITIONS FOR STREAMING STATES###########

raw_pp_current.dropna(axis=0, inplace=True)
raw_pp_current.sort_values(by=['timestamp'])
raw_pp_current.reset_index(inplace=True)
raw_pp_current['total_current']=raw_pp_current['data.A1']+raw_pp_current['data.A2']+raw_pp_current['data.A3']
raw_pp_current.index=raw_pp_current['timestamp']

working_times_df=pd.DataFrame()

working_times_df['timestamp']=pcb_merge_pp1['arvl_tmstmp']
working_times_df['working_time']=pcb_merge_pp1['proc_dur']
working_times_df['event']=1
try:
    working_times_df['energy'] = pcb_merge_pp1.apply(lambda x: raw_pp_current.loc[(raw_pp_current.timestamp <= x.dptr_tmstmp) & (x.arvl_tmstmp <= raw_pp_current.timestamp), ['total_current']].sum()*230/3600000, axis=1)
except:
    print("No working times.")


PP_temp_idle=filt_sig_pp1[['timestamp', 'cor_binry_sig']]
PP_temp_idle['cor_binry_sig']=PP_temp_idle['cor_binry_sig']*-1

PP_temp_idle['cor_binry_sig'].iloc[0]=(PP_temp_idle['cor_binry_sig'].iloc[1]+1)%2
PP_temp_idle['cor_binry_sig'].iloc[-1]=(PP_temp_idle['cor_binry_sig'].iloc[-2]+1)%2

idle_times_raw=sp.signal.find_peaks(PP_temp_idle.cor_binry_sig, width=1)
idle_times_raw_df=pd.DataFrame({"sample_number":idle_times_raw[0], "working_time":idle_times_raw[1]['widths']/72})

for x, row in idle_times_raw_df.iterrows():
    idle_times_raw_df.ix[x,'start_time']=PP_temp_idle.iloc[int(idle_times_raw[1]['left_ips'][x])].timestamp
    idle_times_raw_df.ix[x,'end_time']=PP_temp_idle.iloc[int(idle_times_raw[1]['right_ips'][x])].timestamp
    idle_times_raw_df.ix[x,'timestamp']=PP_temp_idle.iloc[int(idle_times_raw[0][x])].timestamp

idle_times_raw_df['event']=0

try:
    idle_times_raw_df['energy'] = idle_times_raw_df.apply(lambda x: raw_pp_current.loc[(raw_pp_current.timestamp <= x.end_time) & 
                                                            (x.start_time <= raw_pp_current.timestamp),
                                                            ['total_current']].sum()*230/3600000, axis=1)
except:
    print("No idle times.")



working_times_df=working_times_df[['event', 'working_time', 'energy','timestamp']]
idle_times_df=idle_times_raw_df[['event', 'working_time', 'energy', 'timestamp']]

PP_events=pd.DataFrame()

try:
    PP_events=PP_events.append(working_times_df)
except:
    print()
try:    
    PP_events=PP_events.append(idle_times_df)
except:
    print()

try:
    PP_events.index=PP_events.timestamp
    PP_events.drop('timestamp', axis=1, inplace=True)
    PP_events['device']='pickandplace1'
    print(PP_events)
except:
    print('No events found')
    sys.exit(1)

timestr = time.strftime("%H-%M")
print('PP1 working time mode: ', PP_events[PP_events.event==1].working_time.mode().mean())
parameters=open('/home/richard/Desktop/LiveParameters/PP1parameters.txt','a+')
parameters.write(timestr +'\tPP1 working time mode: ' + str(PP_events[PP_events.event==1].working_time.mode().mean())+'\n')
parameters.close()

if not os.path.exists('/mnt/UltraHD/streamingStates/merging/PP1'):

    os.makedirs('/mnt/UltraHD/streamingStates/merging/PP1')

# sns.distplot(PP_events.working_time)
# plt.title('PP1 Working Times Histogram')
#plt.savefig("/mnt/UltraHD/streamingStates/PP1/PP1boardstimes_hist.png") 

directory='/mnt/UltraHD/streamingStates/PP1'

timestr = time.strftime("%Y-%m-%d_%H-%M-%S")
print("Saving States with file name -", timestr+"_PP1.csv")
PP_events.to_csv('/mnt/UltraHD/streamingStates/PP1/'+ timestr+"_PP1.csv")
pcb_merge_pp1.to_csv('/mnt/UltraHD/streamingStates/merging/PP1/'+ timestr+"_merging_correction_PP1.csv")


# plt.plot(pp1_vibr_file.timestamp, pp1_vibr_file.net_accl)
# plt.savefig('VibData.png')


###END OF ADDITIONS FOR STREAMING STATES###########
