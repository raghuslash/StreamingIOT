import requests
import json
import csv
import sys

#from multiprocessing.dummy import Pool
#pool = Pool(100)

if len(sys.argv)<3:
    print ("Usage >")
    print ("python3 %s %s %s %s" % (sys.argv[0],"input_file.csv","output_es_index_name","eshost [http://localhost:9200/]") )
    sys.exit(1)

input_file=sys.argv[1]
output_es_index=sys.argv[2]
eshost= "http://localhost:9200" if len(sys.argv)<4 else sys.argv[3]




def upload(jsonline):
    data = open(jsonline).read()
    
    r = requests.post("{}/{}/{}/_bulk".format(eshost,output_es_index,"mydoctype"),
            headers={"Content-Type":"application/json"}, data=data)
    #print (r.text)
    #print ("%s" % (r.status_code) )
    #print (r.text)


### Using Pandas
import pandas as pd
from pprint import pprint

df=pd.read_csv(input_file)
tempfile='{}.out'.format(output_es_index)
with open(tempfile,'w') as g:
    for i in df.index:
        g.write('{ "index":{} }\n')
        g.write('{}\n'.format(df.loc[i].to_json()))
    
upload(tempfile)
