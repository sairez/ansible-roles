#!/usr/bin/python
# This script searches log files for attempted failed logins.
# -MH

import os
import sys

# Make sure we have all our user variables.
if len(sys.argv) < 2:
    print "USAGE: ./check_failed_logins.py [LOG FILE]"
    print "Example: ./check_failed_logins.py /var/log/messages"
    sys.exit(1)

file=sys.argv[1]
datfile="/tmp/check_failed_logins.dat"
count=0
users=[]
# Check if our dat file exists.  If not, create it.
try:
   fdat=open(datfile,"r")
except IOError:
   fdat=open(datfile,"w+")
else:
   fdat=open(datfile,"r")
linenum=fdat.read();
fdat.close()
# If there is no line number, set it to zero and we'll start
# back from the beggining.  
if str(len(linenum)) == "0":
	linenum = 0
# Search our file from the previous position.
searchfile = open(file, "r")
pointer = searchfile.seek(int(linenum), 0);
for line in searchfile:
    if "denied access" in line: 
	getline = line.split(" ")
        user=getline[7]
        user=user.rstrip('\r\n')
        user=user.rstrip('\n')
	#print "An attempted failed login was found for "+user
	count += 1
	users.append(user)
	#print line
position = searchfile.tell();
#print position
# Record our recent line number and close the file.
fdat=open(datfile,"r+")
fdat.write(str(position));
fdat.close()
searchfile.close()
def f7(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]
users.sort()
badusers=f7(users)
# Print out our results.
if count > 3:
	print "Number of failed login attempts ("+str(count)+") exceeds quota. The following user(s) have invalid logins: "
	print ', '.join(map(str, badusers))
	sys.exit(2)
else:
	print "Number of failed login attempts ("+str(count)+") is within a permissable range."
	sys.exit(0)
