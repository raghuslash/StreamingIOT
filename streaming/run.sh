export DISPLAY=:0.0

batch_size=15
if [ ! -z $1 ];
then
batch_size=$1
fi
q_size=`expr $batch_size + 5`
echo "batch_size:$batch_size";
#exit;

lastbatch="nothing"
while [ 1 ]
do
	start=`date +%s`
        end=`date  +%s`
        duration=0
	
	cd /home/richard/Desktop/iiotstream/tools/data
	rm *

	cd ..
	sh get_2.sh $q_size
	index=`cat index | sed s/helloworld/streamingevents/`
	rfindex=`cat index | sed s/helloworld/streamingstates/`
	echo "INDEX - $index"
	mapindex=`cat index | sed s/helloworld/mapping/`
	echo "MAPPING INDEX - $mapindex"
    mergingindex=`cat index | sed s/helloworld/merging/`
    anoindex=`cat index | sed s/helloworld/anomalyevents/`
	echo "ANOMALY INDEX - $anoindex"
	#exit
	 
	cp dataSplitter.sh data/ 
	
	cd data
	sh dataSplitter.sh
	cd ..
	python3 CleanCSVs.py
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
        python3 anomalyGen.py /home/richard/Desktop/iiotstream/tools/data/loader.csv

	cd /home/richard/Desktop/iiotstream/streaming/MAPPING
        python3 mapldsp.py 
	
    cd /home/richard/Desktop/iiotstream/streaming/PP1
        python3 stateGen.py /home/richard/Desktop/iiotstream/tools/data/pickandplace1.csv

    cd /home/richard/Desktop/iiotstream/streaming/PP2
        python3 stateGen.py /home/richard/Desktop/iiotstream/tools/data/pickandplace2.csv
	
	
	
	
	
	
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
		python3 csv_upload.py "/mnt/UltraHD/streamingStates/RF/$rffname" $rfindex
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
	
	
	        #-------------PP1 states to Database---------------

        cd /mnt/UltraHD/streamingStates/PP1/

        pp1fname=$(ls -t | head -n1)
        pp1thisbatch=$pp1fname

        cd /home/richard/Desktop/iiotstream/streaming/CSV_UPLOAD
        if [ "$pp1thisbatch" = "$pp1lastbatch" ]; then
                echo Already exists.
        else
                echo Pushing Pick and Place 1 states to elasticsearch.
                python3 csv_upload.py "/mnt/UltraHD/streamingStates/PP1/$pp1fname" $index
                #pp1fname=$(ls -t | head -n1)
        fi
        pp1lastbatch=$pp1thisbatch

        cd /mnt/UltraHD/streamingStates/merging/PP1

        pp1mfname=$(ls -t | head -n1)
        pp1mthisbatch=$pp1mfname

        cd /home/richard/Desktop/iiotstream/streaming/CSV_UPLOAD
        if [ "$pp1mthisbatch" = "$pp1mlastbatch" ]; then
                echo Already exists.
        else
                echo Pushing Pick and Place 1 states to elasticsearch.
                python3 csv_upload.py "/mnt/UltraHD/streamingStates/merging/PP1/$pp1mfname" $mergingindex
                #pp1fname=$(ls -t | head -n1)
        fi
        pp1mlastbatch=$pp1mthisbatch

                #-------------PP22states to Database---------------

        cd /mnt/UltraHD/streamingStates/PP2/

        pp2fname=$(ls -t | head -n1)
        pp2thisbatch=$pp2fname

        cd /home/richard/Desktop/iiotstream/streaming/CSV_UPLOAD
        if [ "$pp2thisbatch" = "$pp2lastbatch" ]; then
                echo Already exists.
        else
                echo Pushing Pick and Place 2 states to elasticsearch.
                python3 csv_upload.py "/mnt/UltraHD/streamingStates/PP2/$pp2fname" $index
                #pp2fname=$(ls -t | head -n1)
        fi
        pp2lastbatch=$pp2thisbatch

        cd /mnt/UltraHD/streamingStates/merging/PP2
        pp2mfname=$(ls -t | head -n1)
        pp2mthisbatch=$pp2mfname

        cd /home/richard/Desktop/iiotstream/streaming/CSV_UPLOAD
        if [ "$pp2mthisbatch" = "$pp2mlastbatch" ]; then
                echo Already exists.
        else
                echo Pushing Pick and Place 2 states to elasticsearch.
                python3 csv_upload.py "/mnt/UltraHD/streamingStates/merging/PP2/$pp2mfname" $mergingindex
                #pp2fname=$(ls -t | head -n1)
        fi
        pp2mlastbatch=$pp2mthisbatch

    

	
	#-------------LD-SP MAPPING to Database---------------

	cd /mnt/UltraHD/mapping/LD-SP

        ldspfname=$(ls -t | head -n1)
        ldspthisbatch=$ldspfname

        cd /home/richard/Desktop/iiotstream/streaming/CSV_UPLOAD
        if [ "$ldspthisbatch" = "$ldsplastbatch" ]; then
                echo Already exists.
        else
                echo Pushing Board Mappings to elasticsearch.
                python3 csv_upload.py "/mnt/UltraHD/mapping/LD-SP/$ldspfname" $mapindex
                #ldspfname=$(ls -t | head -n1)
        fi
        ldsplastbatch=$ldspthisbatch
    
	#-------------LD Anomalous Events to Database---------------

	cd /mnt/UltraHD/streamingAno/LD

        ldanofname=$(ls -t | head -n1)
        ldanothisbatch=$ldanofname

        cd /home/richard/Desktop/iiotstream/streaming/CSV_UPLOAD
        if [ "$ldanothisbatch" = "$ldanolastbatch" ]; then
                echo Already exists.
        else
                echo Pushing Loader Anomalies to elasticsearch.
                python3 csv_upload.py "/mnt/UltraHD/streamingAno/LD/$ldanofname" $anoindex
                #ldspfname=$(ls -t | head -n1)
        fi
        ldanolastbatch=$ldanothisbatch
        
#----------------Wait for next Batch--------------------------
	#exit 1

	while [ $duration -lt $((batch_size*60)) ]
        do
                duration=$((end-start))
                end=`date  +%s`
        done
	
done

