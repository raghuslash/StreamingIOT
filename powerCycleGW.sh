#!/bin/bash

for GW in "gwb" "gwc" "gwd" "gwe" "gwh" "gwi" "gwa"

do	
	GWname="$GW.local"
	gwcmd=""
	ping -c 4 $GWname;
	if [ $? -ne 0 ]; then
		echo "$GW is not connected!"
		echo "Restarting smart plug..."
		if [ $GW == "gwa" ] ; then
			gwcmd="gwab"
		elif [ $GW == "gwb" ]; then
			 gwcmd="gwab"
		else
			gwcmd=$GW	
		fi
		echo "Switching off smart plug..."
		echo ""
		curl -X POST "https://maker.ifttt.com/trigger/${gwcmd}_off/with/key/c1b-dP0yd_4SXSkhjdkuhE"
		for i in {10..0}
		do	echo $i
			sleep 1
		done
		echo "Switching on smart plug..."
		echo ""
		curl -X POST "https://maker.ifttt.com/trigger/${gwcmd}_on/with/key/c1b-dP0yd_4SXSkhjdkuhE"
		
 
	fi


done


