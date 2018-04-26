#!/usr/bin/python

"""
Finds total jobs running on target host
First argument of this script is the name of the server
"""

import string
import classad
import htcondor

from collections import defaultdict

ijobsusers = defaultdict(int)
rjobsusers = defaultdict(int)

users = []

from optparse import OptionParser

parser = OptionParser()
parser.add_option("-s", action="store_false", dest='servers', default=True, help="use all servers")

(options, args) = parser.parse_args()

coll = htcondor.Collector("htc.farm.particle.cz")

for submAd in coll.query(htcondor.AdTypes.Submitter, 'true', ['Name', 'RunningJobs']):
  user = string.split(string.split(submAd['Name'], "@")[0],".")[-1]
  users.append(user)

for submAd in coll.query(htcondor.AdTypes.Submitter, 'true', ['Name', 'RunningJobs', 'IdleJobs']):
  user = string.split(string.split(submAd['Name'], "@")[0],".")[-1]
  runningjobs = submAd['RunningJobs']
  idlejobs = submAd['IdleJobs']
  #print users, runningjobs, idlejobs
  if user in users:
    ijobsusers[user] += idlejobs
    rjobsusers[user] += runningjobs
  
print "Number of running jobs according to users: "
print "==========================================\n "
for users, jobs in sorted(rjobsusers.iteritems()):
  print '{0:14} ==> {1:10d}'.format(users, jobs)

print "\nNumber of idle jobs according to users: "
print "=========================================\n "
for users, jobs in sorted(ijobsusers.iteritems()):
  print '{0:14} ==> {1:10d}'.format(users, jobs)


