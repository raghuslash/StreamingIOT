#for device in "loader" "screenprinter_vaf" "pickandplace1" "pickandplace2" "reflowoven_vaf" "bakingoven1" "bakingoven2"


fline=$(head -1 out.csv)
for device in "loader" "screenprinter_plus_vaf" "reflowoven_vaf"

do	
        echo "Grepping.... $device"
        grep $device out.csv > temp
	echo "Sorting... $device"
        sort -t, -nk2 temp -o "$device.csv"
        rm temp
	sed -i "1i $fline" "$device.csv"
done


