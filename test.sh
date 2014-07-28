#!/bin/sh
usage() {
	echo "Usage: $0 [-c] [-d hostname] [-m address] [-t]"
	exit 1
}

do_bleachbit() {
	echo "Cleaning system data.."
}

set_mac() {
	echo "Changing $1 mac address to $2.."
}

change_hostname() {
	echo "Changing hostname to $1.."
}

redirect_to_tor() {
	echo "Redirecting to tor.."
}

while getopts 'h:m:ct' OPTION; do 
	case "$OPTION" in
		c)	CLEAN="yes";;
		h)	HOSTNAME=$OPTARG;;
		m)	MAC=$OPTARG;;
		t)	TOR="yes";;
		?)	usage;;
	esac 
done

[ $# -eq 0 ] && echo "ITERATIVE MODE"

	[ -n "$CLEAN" ] && do_bleachbit

	[ -n "$MAC" ] && set_mac $IFACE $MAC

	[ -n "$HOSTNAME" ] && change_hostname $HOSTNAME

	[ -n "$TOR" ] && redirect_to_tor
