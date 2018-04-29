#!/bin/sh
# wifi signal check script
# https://stackoverflow.com/questions/15797920/how-to-convert-wifi-signal-strength-from-quality-percent-to-rssi-dbm

ssid=$1
ERRORFILE=/tmp/$1
#VALUE_MAP_TO_ZERO=$2
#VALUE_MAP_TO_100=$3
VALUE_MAP_TO_ZERO=-80
VALUE_MAP_TO_100=-40
OUTPUT="$(sudo /sbin/iw dev wlan0 scan ap-force 2>$ERRORFILE | sed 's/^[^ \t]/\n&/'  | awk -v RS= '/SSID: '$ssid'/' | sed '/signal/!d;s/[^0-9/-]*//g;s/00$//')"
ERROR=$(/bin/cat $ERRORFILE)

if [ "$ERROR" = "" ]; then
	if [ "${OUTPUT}" != "" ]; then
	#	echo $OUTPUT
		
		VALUE_TO_CONVERT=${OUTPUT}
		
		if [ $VALUE_MAP_TO_ZERO -lt $VALUE_MAP_TO_100 ]; then
			if [ $VALUE_TO_CONVERT -le $VALUE_MAP_TO_ZERO ]; then
				PERCENTAGE=0
			elif [ $VALUE_TO_CONVERT -ge $VALUE_MAP_TO_100 ]; then
				PERCENTAGE=100
			else
				PERCENTAGE="$( expr \( $VALUE_TO_CONVERT - $VALUE_MAP_TO_ZERO \) \* 100 / \( $VALUE_MAP_TO_100 - $VALUE_MAP_TO_ZERO \) )"
			fi
		fi
	else
		PERCENTAGE=0
	fi
else
	echo "ERROR DETECTED (${ERROR})" # retry!
fi
echo "${PERCENTAGE}"
rm $ERRORFILE
