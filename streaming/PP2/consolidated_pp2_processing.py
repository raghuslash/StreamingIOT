#PP2 PCB Detection and Merging

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

#-----------------------------------------------------------
#Get the data from pp2 csv file
pp2file = pd.read_csv('csv_folders/helloworld-2019-03-01/pickandplace2.csv')
pp2file.columns = [c.replace('.', '_') for c in pp2file.columns]

#PP2 Proximity sensor data
pp2_pxend_file = pp2file.query('deviceid == "pickandplace2_proximity_exit"').loc[:,['datatype','timestamp','deviceid','data_proximity']]
pp2_pxend_file = pp2_pxend_file.sort_values(by="timestamp")
pp2_pxend_file = pp2_pxend_file.reset_index()
pp2_pxend_file = pp2_pxend_file.iloc[:,1:len(pp2_pxend_file.columns)]

#PP2 Vibration sensor data
pp2_vibr_file = pp2file.query('deviceid == "pickandplace2_vibration"').loc[:,['datatype','timestamp','deviceid','data_ax','data_ay','data_az']]
pp2_vibr_file = pp2_vibr_file.sort_values(by="timestamp")
pp2_vibr_file = pp2_vibr_file.reset_index()
pp2_vibr_file = pp2_vibr_file.iloc[:,1:len(pp2_vibr_file.columns)]
pp2_vibr_file = pp2_vibr_file.assign(net_accl = np.sqrt(pp2_vibr_file.data_ax**2 + pp2_vibr_file.data_ay**2 + pp2_vibr_file.data_az**2))

print('Size of pp2_pxend_file =', pp2_pxend_file.shape)
print('Size of pp2_vibr_file  =', pp2_vibr_file.shape)

#-------------------------------------------------------------------------------------------------------------------------------------
#Convert raw acceleration to binary sequence
filt_sig_pp2 = routine_rawaccl_to_binryseq.rawaccl_to_binryseq(pp2_vibr_file,1,'Y','Y',0.2,1.1)

#-------------------------------------------------------------------------
#Raw-acceleration to binary sequene conversion
filt_sig_pp1 = routine_rawaccl_to_binryseq.rawaccl_to_binryseq(pp1_vibr_file,1,'Y','Y',0.6,1.1)

#Detect PCBs and obtain PCB processing durations
pcb_data_pp2 = routine_get_pcb_dur.get_pcb_dur(filt_sig_pp2.binry_sig)

#Eliminate spuriois PCB detections
filt_sig_pp2['cor_binry_sig'] = routine_elim_spur_pcb.elim_spur_pcb(filt_sig_pp2.binry_sig,pcb_data_pp2,500)

#Recalculate PCB processing durations
pcb_data_pp2 = routine_get_pcb_dur.get_pcb_dur(filt_sig_pp2.cor_binry_sig)

#Obtain PCB level dataframe with weightages
pcb_level_pp2 = routine_get_pcb_level_data.get_pcb_level_data(filt_sig_pp2,pcb_data_pp2,50)

#-----------------------------------------------------------------------------------------------------------------------
#Merging process for PP2 (Single step)
 
pcb_merge_pp2 = pcb_level_pp2
mrg_binry_pp2 = filt_sig_pp2.cor_binry_sig

PROC_TWO_END_FLAG = 0
while(PROC_TWO_END_FLAG == 0):
    
    iter_two = iter_two + 1
    print('PROC-TWO-ITERATION :', iter_two)
    
    pcb_merge_pp2,mrg_binry_pp2,no_of_merged_pcbs = routine_merging_algo.merging_algo  \
    (inp_df        = pcb_merge_pp2                                   \
    ,inp_binry_sig = mrg_binry_pp2                                   \
    ,THRESHOLD     = THRESHOLD                                            \
    ,HIGH_END      = HIGH_END                                             \
    ) 
    
    if(no_of_merged_pcbs == 0):
        PROC_TWO_END_FLAG = 1
    #end-if
    
    print ('=============================================')
    
#end-while 

filt_sig_pp2['mrg_binry_sig'] = mrg_binry_pp2

#-----------------------------------------------------------------------------------------------------------
#Write processed info to csv file
filt_sig_pp2.to_csv('PP2_Processed_DataFrame.csv')
pcb_merge_pp2.to_csv('PP2_PCB_Merged_DataFrame.csv')
pp2_pxend_file.to_csv('PP2_Proximity_Exit_DataFrame.csv')
#-----------------------------------------------------------------------------
