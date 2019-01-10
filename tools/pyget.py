import datetime
import sys


try:
    past_interval = int(sys.argv[1])
except:
    print("Argument error: pass number of minutes (integer) of past data to be captured.")
    sys.exit(1)


date=datetime.datetime.now().strftime("%Y-%m-%d")

index = "helloworld-%s" % date

with open("index",'w') as g:
    g.write(index)

import json

query=json.load(open('template.query.json'))



now = datetime.datetime.now() # this is utc, donot use utcnow method
past = now - datetime.timedelta(minutes=past_interval)

now_ms = now.timestamp().__int__() * 1000
past_ms = past.timestamp().__int__() * 1000

query['query']['bool']['must'][1]['range']['timestamp']['gte'] = past_ms
query['query']['bool']['must'][1]['range']['timestamp']['lte'] = now_ms

with open('query.json','w') as g:
    json.dump(query,g)

print ("---> INDEX: %s" % index)
print ("---> PAST_INTERVAL (minutes): %s" % past_interval)
print ("---> NOW (ms): %s" % now_ms)
print ("---> PAST (ms): %s" %  past_ms)
