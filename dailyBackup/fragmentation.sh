index=$1

if [ -z "$1" ]

then 

	echo "No index name supplied... exiting"

	exit 1

else 

	echo "Supplied index ---> $index"

fi 

sleep 2



echo ""

echo "Checking if Index exists -- $index"

rawFile="/mnt/UltraHD/RAW/data/$index"

ls $rawFile

if [ $? -ne 0 ]

then

	echo "The supplied file with index name - $index doesn't exist"

	exit 1

else

	echo "Found index - $index"

fi

sleep 2

echo ""

echo "Changing dir to /mnt/UltraHD/RAW_SEGREGATED/"

cd /mnt/UltraHD/RAW_SEGREGATED/

sleep 2

echo ""

echo "Creating dir named $index"

mkdir $index

if [ $? -ne 0 ]

then

	echo ""

	echo "Folder exists already... EXITING"

	exit 1

else

	echo "Successfully created folder $index"

fi

sleep 2

echo ""

echo "Changing dir to $index"

cd $index

sleep 2


echo ""

echo "Current Directory ---> `pwd`"


for device in "loader" "screenprinter" "pickandplace1" "pickandplace2" "reflowoven" "bakingoven1" "bakingoven2"

do

	echo ""

	head -1 $rawFile > temp

	echo "Grepping.... $device"

	awk "/$device/" $rawFile >> temp

	echo "Sorting... $device"

	sort -t, -nk2 temp -o "$device.csv"

	rm temp

done


