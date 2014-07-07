#!/bin/bash
wbinfo -i svc_nagios &> /dev/null || { echo "CRITICAL! AD authentication check failed."; exit 2; }
echo "OK! AD authentication check was successfull."
exit 0
