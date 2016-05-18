#!/bin/sh

export DISPLAY=:0

/usr/bin/Xvfb :0 -screen 0 1024x860x24 >> /tmp/Xvfb.out 2>&1 &

twm >> /tmp/Xvfb.out 2>&1 &

x11vnc --nopw &

sleep 5

cd /u01/oracle/ocsg-pte/ocsg_pte/
/u01/oracle/ocsg-pte/ocsg_pte/run.sh

