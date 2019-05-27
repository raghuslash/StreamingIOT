import pandas as pd
import os
import glob
import sys
newest = max(glob.iglob('/mnt/UltraHD/streamingStates/LD/*.csv'), key=os.path.getctime)
tempdf=pd.read_csv(newest)
ld_boards=tempdf[tempdf['event'] == 1]

newest = max(glob.iglob('/mnt/UltraHD/streamingStates/SP/*.csv'), key=os.path.getctime)
tempdf=pd.read_csv(newest)
sp_boards=tempdf[tempdf['event'] == 1]


pattern="%Y-%m-%dT%H:%M:%S.%f"
sp_boards['timestamp'] =  pd.to_datetime(sp_boards['timestamp'], format=pattern)
ld_boards['timestamp'] =  pd.to_datetime(ld_boards['timestamp'], format=pattern)


#print(sp_boards)
#print(ld_boards)


matching_list=[]
spmatch=0
posdiff=0
for ldindex, ldrow in ld_boards.iterrows():
#     print (index, row["timestamp"], row["state"])
    ldts=ldrow['timestamp']
#     print(ldts)
    bestdiff=-1
    for spindex, sprow in sp_boards.iterrows():
        spts=sprow['timestamp']
        posdiff=abs(spts-ldts)
        if bestdiff==-1:
            bestdiff=posdiff
        elif posdiff<bestdiff:
            bestdiff=posdiff
            spmatch=sprow['timestamp']
        elif posdiff>bestdiff:
#             print(bestdiff.seconds)
            if (bestdiff.seconds >19):
                spmatch='NaN'
            break
        if spts<ldts:
            spmatch='NaN'
    try:
        spmatch=spmatch.strftime(pattern)
    except:
        continue
    matchrow={"BoardID":ldts.strftime('%s'), "LD_Time": ldts.strftime(pattern), "SP_Time": spmatch}
    matching_list.append(matchrow)
board_mapping=pd.DataFrame(matching_list)

#board_mapping['BoardID'] =  pd.to_datetime(sp_boards['BoardID'], format=pattern)
#board_mapping['LD_Time'] =  pd.to_datetime(ld_boards['LD_Time'], format=pattern)
#board_mapping['SP_Time'] =  pd.to_datetime(sp_boards['SP_Time'], format=pattern)

print (board_mapping)
sys.exit(2)


board_mapping.index = board_mapping["BoardID"]
board_mapping.drop("BoardID",axis=1, inplace=True)


if not os.path.exists('/mnt/UltraHD/mapping/LD-SP'):
    os.makedirs('/mnt/UltraHD/mapping/LD-SP')
import time
timestr = time.strftime("%Y-%m-%d_%H-%M-%S")
board_mapping.to_csv('/mnt/UltraHD/mapping/LD-SP/'+timestr+'LD-SP.csv')

