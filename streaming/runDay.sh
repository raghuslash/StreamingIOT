
	cd /home/richard/Desktop/iiotstream/tools
	sh dump.sh $1
	cd data
	echo $1 > index
	index=`cat index | sed s/helloworld/streamingevents/`
	rfindex=`cat index | sed s/helloworld/streamingstates/`
	echo "INDEX - $index"
	mapindex=`cat index | sed s/helloworld/mapping/`
	echo "MAPPING INDEX - $mapindex"
        mergingindex=`cat index | sed s/helloworld/merging/`
	#exit
	 
	
	sh dataSplitter.sh $1
	mkdir -p "/mnt/UltraHD/RAW/`date '+%Y-%m-%dT%H-%M-%S'`"
	cd /mnt/UltraHD/RAW/
	foldername=$(ls -t | head -n1)
	cd /home/richard/Desktop/iiotstream/tools/data

	#cp *.csv "/mnt/UltraHD/RAW/$foldername/"

	cd /home/richard/Desktop/iiotstream/streaming/RF
	python3 stateGen.py /home/richard/Desktop/iiotstream/tools/data/reflowoven_vaf.csv
        
	cd /home/richard/Desktop/iiotstream/streaming/SP
        python3 stateGen.py /home/richard/Desktop/iiotstream/tools/data/screenprinter_plus_vaf.csv

        cd /home/richard/Desktop/iiotstream/streaming/LD
        python3 stateGen.py /home/richard/Desktop/iiotstream/tools/data/loader.csv
        
	#cd /home/richard/Desktop/iiotstream/streaming/MAPPING
        #python3 mapldsp.py 
	
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

        cd /mnt/UltraHD/streamingStates/merging/PP1/

        pp1fname=$(ls -t | head -n1)
        pp1thisbatch=$pp1fname

        cd /home/richard/Desktop/iiotstream/streaming/CSV_UPLOAD
        if [ "$pp1thisbatch" = "$pp1lastbatch" ]; then
                echo Already exists.
        else
                echo Pushing Pick and Place 1 states to elasticsearch.
                python3 csv_upload.py "/mnt/UltraHD/streamingStates/merging/PP1/$pp1fname" $mergingindex
                #pp1fname=$(ls -t | head -n1)
        fi
        pp1lastbatch=$pp1thisbatch

                #-------------PP1 states to Database---------------

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

                cd /mnt/UltraHD/streamingStates/merging/PP2/

        pp2fname=$(ls -t | head -n1)
        pp2thisbatch=$pp2fname

        cd /home/richard/Desktop/iiotstream/streaming/CSV_UPLOAD
        if [ "$pp2thisbatch" = "$pp2lastbatch" ]; then
                echo Already exists.
        else
                echo Pushing Pick and Place 2 states to elasticsearch.
                python3 csv_upload.py "/mnt/UltraHD/streamingStates/merging/PP2/$pp2fname" $mergingindex
                #pp2fname=$(ls -t | head -n1)
        fi
        pp2lastbatch=$pp2thisbatch

    

	
#	#-------------LD-SP MAPPING to Database---------------
#
#	cd /mnt/UltraHD/mapping/LD-SP
#
#        ldspfname=$(ls -t | head -n1)
#        ldspthisbatch=$ldspfname
#
#        cd /home/richard/Desktop/iiotstream/streaming/CSV_UPLOAD
#        if [ "$ldspthisbatch" = "$ldsplastbatch" ]; then
#                echo Already exists.
#        else
#                echo Pushing Board Mappings to elasticsearch.
#                python3 csv_upload.py "/mnt/UltraHD/mapping/LD-SP/$ldspfname" $mapindex
#                #ldspfname=$(ls -t | head -n1)
#        fi
#        ldsplastbatch=$ldspthisbatch
