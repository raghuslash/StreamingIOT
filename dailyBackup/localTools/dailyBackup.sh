#/bin/bash/
if [ -f /mnt/extHD/src ] && [ -f /mnt/CAREFUL/dest ]; then
	rsync -arv --ignore-existing --progress /mnt/extHD/VINYAS_DATA/ /mnt/CAREFUL/VINYAS_DATA/
	if [ $? -ne 0 ]; then
		echo Daily Backup failed at `date` >> ~/Desktop/backup_error_log.txt
	fi
else
	 
	echo "Daily Backup failed at `date`. Disks not mounted properly."  >> ~/Desktop/backup_error_log.txt
fi


