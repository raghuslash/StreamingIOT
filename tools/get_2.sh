batch=$1
if [ -z "$1" ]; then
	batch=1
fi
python3 pyget.py $batch
/usr/local/bin/es2csv -u vinyas:9200 -i `cat index` -r -q @query.json -o data/out.csv
