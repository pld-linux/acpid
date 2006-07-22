#!/bin/sh
# /etc/acpid/actions/button.sh
#
# Detect buttons pressed and take appropriate actions.

if [ $# != 1 ]; then
	exit 1
fi
set $*

case "$1" in
	button/power)
		logger "acpid: $1 action is not defined."
		# halt computer
		#halt
		# put computer to sleep (not all machines have sleep button)
		#echo mem > /sys/power/state
		#hibernate
		;;
	button/sleep)
		logger "acpid: $1 action is not defined"
		# put computer to sleep
		#echo mem > /sys/power/state
		#hibernate
		;;
	button/lid)
		logger "acpid: $1 action is not defined"
		# put computer to sleep
		#echo mem > /sys/power/state

		# if you want to specify separate commands for lid open/close uncomment this section:

		#NUMBER=`printf "%d" "0x$4"`
		#EVEN=`dc -e "1 k $NUMBER 2 / p" | grep "\.0"`
		#if [ ! "$EVEN" ]; then
		#	logger "acpid: lid close action is not defined"
		#else
		#	logger "acpid: lid open action is not defined"
		#fi
		;;
	*)
		logger "acpid: $1 action is not defined"
		;;
esac
