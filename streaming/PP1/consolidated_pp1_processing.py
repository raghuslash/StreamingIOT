#PP1 PCB Detection and Merging

#Import the libraries
import pandas as pd
import numpy as np
import scipy as sp

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
pp1file = pd.read_csv('csv_folders/helloworld-2019-03-01/pickandplace1.csv')
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
filt_sig_pp1 = routine_rawaccl_to_binryseq.rawaccl_to_binryseq(pp1_vibr_file,1,'Y','Y',0.6,1.1)

#Detect PCBs and obtain PCB processing durations
pcb_data_pp1 = routine_get_pcb_dur.get_pcb_dur(filt_sig_pp1.binry_sig)

#Eliminate spuriois PCB detections
filt_sig_pp1['cor_binry_sig'] = routine_elim_spur_pcb.elim_spur_pcb(filt_sig_pp1.binry_sig,pcb_data_pp1,500)

#Recalculate PCB processing durations
pcb_data_pp1 = routine_get_pcb_dur.get_pcb_dur(filt_sig_pp1.cor_binry_sig)

#Obtain PCB level dataframe with weightages
pcb_level_pp1 = routine_get_pcb_level_data.get_pcb_level_data(filt_sig_pp1,pcb_data_pp1,50)

#-----------------------------------------------------------------------------------------------------------------------
#Merging process 
pcb_merge_pp1 = pcb_level_pp1
mrg_binry_pp1 = filt_sig_pp1.cor_binry_sig

THRESHOLD = 0.95
HIGH_END  = 1.20

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

pp1_pxstr_file.to_csv('PP1_Proximity_Entry_DataFrame.csv')
#-----------------------------------------------------------------------------