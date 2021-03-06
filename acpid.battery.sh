#!/bin/sh
# /etc/acpid/actions/battery.sh
# based on work by Frank Dietrich <ablesoft@gmx.de>
# �ukasz Pawelczyk <havner@pld-linux.org>
#
# Handle power related events and take appropriate actions.

if [ $# != 1 ]; then
	exit 1
fi
set $*

AC=/proc/acpi/ac_adapter/AC
BAT=/proc/acpi/battery/$2

# get the AC connector state (plugged/unplugged) from /proc filesystem.
AC_STATE=`sed -n 's/^.*\(off\|on\)-line.*/\1/p' $AC/state`

# get the battery state from /proc filesystem
BAT_CAPACITY=`awk '/^remaining\ capacity:/ {print $3}' $BAT/state`
BAT_WARNING=`awk '/^alarm:/ {print $2}' $BAT/alarm`
BAT_CRITICAL=`awk '/^design\ capacity\ low:/ {print $4}' $BAT/info`
if [ "$BAT_CAPACITY" -le "$((BAT_CRITICAL+200))" -a "$AC_STATE" = "off" ]; then
	BAT_STATE=critical
elif [ "$BAT_CAPACITY" -le "$((BAT_WARNING+200))" -a "$AC_STATE" = "off" ]; then
	BAT_STATE=warning
else
	BAT_STATE=normal
fi

case "$AC_STATE" in
  on)
	# AC connector plugged in
	logger "acpid: `basename $AC` connector plugged in."
	# deactivate standby (spindown) timeout for the drive
	#hdparm -q -S 0 /dev/hda
	# handle processor - this feature is deprecated for Kernel > 2.6.11.
	#echo 0 > /proc/acpi/processor/CPU0/throttling
	#echo 0 > /proc/acpi/processor/CPU0/performance
	;;
  off)
	# AC connector unplugged
	logger "acpid: `basename $AC` connector unplugged."
	# activate standby (spindown) timeout for the drive
	# timeout 5 minutes (man hdparm, for more informations)
	#hdparm -q -S 60 /dev/hda 
	# handle processor - this feature is deprecated for Kernel > 2.6.11.
	#echo 4 > /proc/acpi/processor/CPU0/throttling
	#echo 3 > /proc/acpi/processor/CPU0/performance
	;;
  *)
	# AC connector in undetermined state
	logger "acpid: Could not determine new `basename $AC` connector state."
	;;
esac

case "$BAT_STATE" in
  warning)
	# battery passed acpi alarm state and AC unplugged
	logger "acpid: Remaining `basename $BAT` battery capacity low."
	# play alarm sound
	#play /path_to/alarm.wav
	# put computer to sleep
	#echo mem > /sys/power/state
	#hibernate
	;;
  critical)
	# some laptops generate acpi event when machine is about to turn off
	logger "acpid: Remaining `basename $BAT` battery capacity VERY low."
	# play alarm sound
	#play /path_to/alarm.wav
	# put computer to sleep
	#echo mem > /sys/power/state
	#hibernate
	;;
  normal)
	# either battery is charged or AC plugged
	;;
  *)
	# battery in undetermined state
	logger "acpid: Could not determine `basename $BAT` battery state."
	;;
esac
