from dateutil import parser
import datetime
with open('index.txt', 'r') as ifile:
  d = ifile.read()
d=parser.parse(d)
d=(d + datetime.timedelta(minutes=5*60+30)).strftime("streamingstates-%Y-%m-%d")

ifile = open('index.txt', 'w')
ifile.write(d)

