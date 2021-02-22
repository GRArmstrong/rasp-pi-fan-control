#!/bin/bash

# Make sure we're running as root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root (use sudo)"
   exit 1
fi

# Get current directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

cp -r "$DIR/fan-control" /opt

cp "$DIR/service/fan-control.service" /etc/systemd/system/fan-control.service

echo "Files should be in place, if you'll do the honours:"
echo "  \$ sudo systemctl enable fan-control --now"
