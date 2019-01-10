thisDir=$(dirname $(realpath "$0"))
if [ ! -e /mnt/UltraHD/UltraHD ]; then

        echo "Trying to mount UltraHD..."
        mount /dev/sdb1 /mnt/UltraHD
        if [ $? -ne 0 ]; then
                echo "Unable to mount UltraHD. Exiting..." 
                sleep 1
		cd /mnt/UltraHD/RAW
		echo "Failed for index - $LASTINDEX. Hard disk not mounted." > errorLog.txt
		
		echo "Error log can be found at /mnt/UltraHD/RAW/errorLog.txt"
		exit 1
	fi
	
fi

LASTINDEX=$1
if [ -z "$1" ]; then
	LASTINDEX=$(date -d "-1 day" +"helloworld-%Y-%m-%d")
	echo "Yesterday's index is $LASTINDEX"
fi
echo "Going to query index - $LASTINDEX"
echo "Changing directory to /mnt/UltraHD/RAW..."
cd /mnt/UltraHD/RAW
sh dump.sh $LASTINDEX
echo $?
#if [ $? -e 0 ]; then
	echo ""
	echo "Finished downloading CSV of index - $LASTINDEX"
	echo ""
	echo "Changing directory to $thisDir"
	cd "$thisDir"
	echo ""
	echo "Calling fragmentation script..."
	sh fragmentation.sh $LASTINDEX
#else
#	echo "Error in getting CSV..."
#	echo "Please check if IP is updated in hosts file."
#	echo "Error log can be found at /mnt/UltraHD/RAW/errorLog.txt"
#
#	echo "Failed for index - $LASTINDEX. Network error" > errorLog.txt
#	exit 2
#fi

