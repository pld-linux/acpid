#!/bin/sh
# /etc/acpid/actions/battery.sh
# based on work by Frank Dietrich <ablesoft@gmx.de>
#
# Detect AC connector plugged in or unplugged and take appropriate actions.

if [ $# != 1 ]; then
	exit 1
fi
set $*

# get the AC connector state from /proc filesystem.
STATE=`sed -n 's/^.*\(off\|on\)-line.*/\1/p' /proc/acpi/ac_adapter/AC/state`

case "$STATE" in
	on)
		# AC connector plugged in
		logger "acpid: AC connector plugged in."
		# deactivate standby (spindown) timeout for the drive
		#hdparm -q -S 0 /dev/hda
		# handle processor
		#echo 0 > /proc/acpi/processor/CPU0/throttling
		#echo 0 > /proc/acpi/processor/CPU0/performance
		;;
	off)
		# AC connector unplugged
		logger "acpid: AC connector unplugged."
		# activate standby (spindown) timeout for the drive
		# timeout 5 minutes (man hdparm, for more informations)
		#hdparm -q -S 60 /dev/hda 
		# handle processor
		#echo 4 > /proc/acpi/processor/CPU0/throttling
		#echo 3 > /proc/acpi/processor/CPU0/performance
		;;
	*)
		# AC connector in undetermined state
		logger "acpid: Could not determine new AC connector state."
		;;
esac
