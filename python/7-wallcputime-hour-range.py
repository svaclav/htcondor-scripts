#!/usr/bin/python

"""
Computes walltime and cputime for needed server in the timedelta period

Usage:
./7-wallcputime-hour-range.py -m condor.farm.particle.cz -s "12/04/2017 01:00:00" -u "12/06/2017 09:50:12"

"""

import time
import datetime 

import sys
import classad
import htcondor

from optparse import OptionParser

parser = OptionParser()
parser.add_option("-m", "--host", dest="host",
                  help="which computing server to use")
parser.add_option("-s", "--since", dest="stime",
                  help="completed jobs after this date")
parser.add_option("-u", "--until", dest="utime", 
                  help="completed jobs before this date")

(options, args) = parser.parse_args()

coll = htcondor.Collector("htc.farm.particle.cz")

def date2Unix(date):
    unixTime = time.mktime(datetime.datetime.strptime(date, "%m/%d/%Y %H:%M:%S").timetuple())
    return unixTime

for scheddAd in coll.query(htcondor.AdTypes.Schedd, 'true', ['Name', 'ScheddIpAddr', 'MyAddress']):
  servername = scheddAd['Name']
  for jobAd in htcondor.Schedd(scheddAd).query('true', ['JobStatus', 'Owner', 'RemoteWallClockTime', 'User', 'JobStartDate', 'CompletionDate']):
    jobstartdate    = jobAd['JobStartDate']
    completiondate  = jobAd['CompletionDate']
    jobstatus	    = jobAd['JobStatus']
    #walltime	    = jobAd['RemoteWallClockTime']
    #print walltime
    #walltimetotal   = 0

    if options.stime and options.utime:
      startdateuser = date2Unix(options.stime)
      enddateuser   = date2Unix(options.utime)
      if jobstatus == 4 and jobstartdate >= startdateuser and enddateuser <= completiondate:
	  walltimetotal += walltime
  print "Total walltime for server " + str(servername) + ": " + str(walltimetotal)
