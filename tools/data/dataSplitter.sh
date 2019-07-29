#for device in "loader" "screenprinter_vaf" "pickandplace1" "pickandplace2" "reflowoven_vaf" "bakingoven1" "bakingoven2"

fname=$1
if [ -z $1 ] ; then 
	fname="out.csv"
fi
fline=$(head -1 $fname)
for device in "loader" "screenprinter_plus_vaf" "reflowoven_vaf" "pickandplace1" "pickandplace2"

do	
        echo "Grepping.... $device"
        grep $device $fname > temp
	echo "Sorting... $device"
        sort -t, -nk2 temp -o "$device.csv"
        rm temp
	sed -i "1i $fline" "$device.csv"
done


