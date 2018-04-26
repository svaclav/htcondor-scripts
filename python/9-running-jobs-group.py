#!/usr/bin/python

"""
Finds total jobs running on target host
First argument of this script is the name of the server
"""

import string
import classad
import htcondor

from collections import defaultdict

ijobsgroups = defaultdict(int)
rjobsgroups = defaultdict(int)

groups = []

from optparse import OptionParser

parser = OptionParser()
parser.add_option("-s", action="store_false", dest='servers', default=True, help="use all servers")

(options, args) = parser.parse_args()

coll = htcondor.Collector("htc.farm.particle.cz")

for submAd in coll.query(htcondor.AdTypes.Submitter, 'true', ['Name', 'RunningJobs']):
  group = string.split(string.split(submAd['Name'],".")[0],"_")[1]
  groups.append(group)

for submAd in coll.query(htcondor.AdTypes.Submitter, 'true', ['Name', 'RunningJobs', 'IdleJobs']):
  group = string.split(string.split(submAd['Name'],".")[0],"_")[1]
  runningjobs = submAd['RunningJobs']
  idlejobs = submAd['IdleJobs']
  #print group, runningjobs, idlejobs
  if group in groups:
    ijobsgroups[group] += idlejobs
    rjobsgroups[group] += runningjobs
  
print "Number of running jobs according to groups: "
print "==========================\n "
for group, jobs in rjobsgroups.iteritems():
  print '{0:10} ==> {1:10d}'.format(group, jobs)

print "\nNumber of idle jobs according to groups: "
print "==========================\n "
for group, jobs in ijobsgroups.iteritems():
  print '{0:10} ==> {1:10d}'.format(group, jobs)


