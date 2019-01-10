export DISPLAY=:0.0

batch_size=15
if [ ! -z $1 ];
then
batch_size=$1
fi

echo "batch_size:$batch_size";
#exit;

lastbatch="nothing"
#while [ 1 ]
#do
	start=`date +%s`
        end=`date  +%s`
        duration=0
	
	cd /home/richard/Desktop/iiotstream/tools/data
	cp ../dataSplitter.sh .
	rm *.csv
	cd ..
	sh get.sh $batch_size
	index=`cat index | sed s/helloworld/streamingstates/`
	echo "INDEX - $index"
	#exit
	 
	
	cd data
	sh dataSplitter.sh
	mkdir -p "/mnt/UltraHD/RAW/`date '+%Y-%m-%dT%H-%M-%S'`"
	cd /mnt/UltraHD/RAW/
	foldername=$(ls -t | head -n1)
	cd /home/richard/Desktop/iiotstream/tools/data

	cp *.csv "/mnt/UltraHD/RAW/$foldername/"

	cd /home/richard/Desktop/iiotstream/streaming/RF
	python3 stateGen.py /home/richard/Desktop/iiotstream/tools/data/reflowoven_vaf.csv
        
	cd /home/richard/Desktop/iiotstream/streaming/SP
        python3 stateGen.py /home/richard/Desktop/iiotstream/tools/data/screenprinter_plus_vaf.csv

        cd /home/richard/Desktop/iiotstream/streaming/LD
        python3 stateGen.py /home/richard/Desktop/iiotstream/tools/data/loader.csv
	

	
	
	
	
	
	
	#--------------Reflow states to Databse----------

	cd /mnt/UltraHD/streamingStates/RF
	rffname=$(ls -t | head -n1)
	
	#--------------Save Index-----------------
	
	rfthisbatch=$rffname
	
	cd /home/richard/Desktop/iiotstream/streaming/CSV_UPLOAD
	if [ "$rfthisbatch" = "$rflastbatch" ]; then
        	echo Already exists.
	else
        	echo Pushing Reflow Oven states to elasticsearch.
		python3 csv_upload.py "/mnt/UltraHD/streamingStates/RF/$rffname" $index
		#rffname=$(ls -t | head -n1)
	fi
	rflastbatch=$rfthisbatch
	
	
	
	#------------SP states to Database---------------

	cd /mnt/UltraHD/streamingStates/SP

        spfname=$(ls -t | head -n1)
        spthisbatch=$spfname

        cd /home/richard/Desktop/iiotstream/streaming/CSV_UPLOAD
        if [ "$spthisbatch" = "$splastbatch" ]; then
                echo Already exists.
        else
                echo Pushing Screenprinter states to elasticsearch.
                python3 csv_upload.py "/mnt/UltraHD/streamingStates/SP/$spfname" $index
        
                #spfname=$(ls -t | head -n1)
	fi
        splastbatch=$spthisbatch

	
	
	
	
	#-------------LD states to Database---------------

	cd /mnt/UltraHD/streamingStates/LD

        ldfname=$(ls -t | head -n1)
        ldthisbatch=$ldfname

        cd /home/richard/Desktop/iiotstream/streaming/CSV_UPLOAD
        if [ "$ldthisbatch" = "$ldlastbatch" ]; then
                echo Already exists.
        else
                echo Pushing Loader states to elasticsearch.
                python3 csv_upload.py "/mnt/UltraHD/streamingStates/LD/$ldfname" $index
                #ldfname=$(ls -t | head -n1)
        fi
        ldlastbatch=$ldthisbatch
    

	
#----------------Wait for next Batch--------------------------
	#exit 1

	#while [ $duration -lt $((batch_size*60)) ]
        #do
        #        duration=$((end-start))
        #        end=`date  +%s`
        #done
	
#done

