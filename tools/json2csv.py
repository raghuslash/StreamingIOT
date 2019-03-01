import json

def line2headers(jsonline):
    try:
        return list(json.loads(jsonline).keys())
    except Exception as e:
        print("Exception in method: headers",e)
        return []




def collect_headers(jsonfile):
    ALL_HEADERS=[]
    NLINES=0
    with open(jsonfile,'r') as f:
        while True:
            line=f.readline().strip()
            if not line: break
            NLINES+=1
            line_headers= line2headers(line)
            ALL_HEADERS = list(set(ALL_HEADERS+line_headers))
            #print(len(ALL_HEADERS))
        ALL_HEADERS.sort()
        #print(ALL_HEADERS)
        return ALL_HEADERS,NLINES


def line2csv(_jsonline,_headers):
    line=json.loads(_jsonline)
    vals=[]
    for h in _headers:
        if h in line:
            val=line[h]
        else:
            val=""
        vals.append(val)

    vals=map(lambda x: str(x),vals)
    csv=",".join(vals)
    return csv



def write_csv(ifile,ofile):

    import sys

    print("Collecting headers...")
    headers,nlines=collect_headers(filename)
    print(",".join(headers))

    #write csv headers
    with open(ofile,'a') as g:
        g.write(",".join(headers))
        g.write("\n")
    

    progress_bar_full_len=50
    print(" " + "-"*progress_bar_full_len)

    nlines_processed=0
    with open(ifile,'r') as f:
        while True:
            line=f.readline()
            if not line: break
            csv=line2csv(line,headers)
            with open(ofile,'a') as g:
                g.write(csv)
                g.write("\n")

            nlines_processed+=1
            progress_bar_len = int(progress_bar_full_len*nlines_processed/nlines) 
            print("\r[" + "#"*progress_bar_len + " "*(progress_bar_full_len - progress_bar_len) + "] " + str(int(100*nlines_processed/nlines)) + "%" ,end="")
            sys.stdout.flush()    
    
    print("\n " +  "-"* progress_bar_full_len)



if __name__=="__main__":
    import sys
    filename=sys.argv[1]
    import os
    outfile="xout.csv"
    if os.path.exists(outfile):
        print("OUTFILE '" + outfile + "' already exists. Exiting...")
        exit()
    write_csv(filename,outfile)


