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

    print ("%s" % (r.status_code) )
    #print (r.text)

with open(input_file,'r') as f:
    line = f.readline().strip()
    headers=[]

    for h in line.split(","):
        headers.append(h)

    print (headers)

    #exit(0)

with open(input_file,'r') as f:
    g = open("out",'w')

    reader = csv.DictReader( f, headers)
    count=0
    for row in reader:
        count+=1
        if count==1: continue
        jrow = json.dumps(row)
        #pool.apply_async(upload,(jrow,))
        #sys.stdout.write("[ ")
        #sys.stdout.write("*" * count)
        #sys.stdout.write(" ] ")
        sys.stdout.write(str(count))
        sys.stdout.write("\r")
        sys.stdout.flush()

        g.write('{ "index":{} }\n')
        g.write(jrow + "\n")

    print(count)


upload("out")
