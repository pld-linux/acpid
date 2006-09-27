#!/bin/sh
# /etc/acpid/actions/battery.sh
# based on work by Frank Dietrich <ablesoft@gmx.de>
# £ukasz Pawelczyk <havner@pld-linux.org>
#
# Handle power related events and take appropriate actions.

if [ $# != 1 ]; then
	exit 1
fi
set $*

AC=/proc/acpi/ac_adapter/ADP1
BAT=/proc/acpi/battery/BAT1
STATE_FILE=/tmp/ac_bat_acpid.state

# get the AC connector state (plugged/unplugged) from /proc filesystem.
AC_STATE=`sed -n 's/^.*\(off\|on\)-line.*/\1/p' $AC/state`
AC_STATE_OLD=`cat "$STATE_FILE" | awk '{print $1};'`
# get the battery state from /proc filesystem
BAT_CAPACITY=`awk '/^remaining\ capacity:/ {print $3}' $BAT/state`
BAT_WARNING=`awk '/^alarm:/ {print $2}' $BAT/alarm`
BAT_CRITICAL=`awk '/^design\ capacity\ low:/ {print $4}' $BAT/info`
BAT_STATE_OLD=`cat "$STATE_FILE" | awk '{print $2};'`
if [ "$BAT_CAPACITY" -le "$((BAT_CRITICAL+200))" -a "$AC_STATE" = "off" ]; then
	BAT_STATE=critical
elif [ "$BAT_CAPACITY" -le "$((BAT_WARNING+200))" -a "$AC_STATE" = "off" ]; then
	BAT_STATE=warning
else
	BAT_STATE=normal
fi
echo "$AC_STATE $BAT_STATE" >  "$STATE_FILE"

if [ "$AC_STATE" != "$AC_STATE_OLD" ]; then
 case "$AC_STATE" in
  on)
	# AC connector plugged in
	logger "acpid: `basename $AC` connector plugged in. State: $AC_STATE."
	# deactivate standby (spindown) timeout for the drive
	#hdparm -q -S 0 /dev/hda
	# handle processor
	#echo 0 > /proc/acpi/processor/CPU0/throttling
	#echo 0 > /proc/acpi/processor/CPU0/performance
	;;
  off)
	# AC connector unplugged
	logger "acpid: `basename $AC` connector unplugged. State: $AC_STATE."
	# activate standby (spindown) timeout for the drive
	# timeout 5 minutes (man hdparm, for more informations)
	#hdparm -q -S 60 /dev/sda 
	# handle processor
	#echo 4 > /proc/acpi/processor/CPU0/throttling
	#echo 3 > /proc/acpi/processor/CPU0/performance
	;;
  *)
	# AC connector in undetermined state
	logger "acpid: Could not determine new `basename $AC` connector state: $AC_STATE."
	;;
 esac
fi

if [ "$BAT_STATE" != "$BAT_STATE_OLD" ]; then
 case "$BAT_STATE" in
  warning)
	# battery passed acpi alarm state and AC unplugged
	logger "acpid: Remaining `basename $BAT` battery capacity low. State: $BAT_STATE."
	# play alarm sound
	#play /path_to/alarm.wav
	# put computer to sleep
	#echo mem > /sys/power/state
	#hibernate
	;;
  critical)
	# some laptops generate acpi event when machine is about to turn off
	logger "acpid: Remaining `basename $BAT` battery capacity VERY low. State: $BAT_STATE."
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
	logger "acpid: Could not determine `basename $BAT` battery state: $BAT_STATE."
	;;
 esac
fi
