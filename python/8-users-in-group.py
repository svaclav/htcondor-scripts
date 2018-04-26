#!/usr/bin/python

"""
Finds total jobs running on target host
First argument of this script is the name of the server
"""

import string
import classad
import htcondor

from collections import defaultdict

usergroups = defaultdict(int)

groups = []

from optparse import OptionParser

parser = OptionParser()
parser.add_option("-s", action="store_false", dest='servers', default=True, help="use all servers")

(options, args) = parser.parse_args()


coll = htcondor.Collector("htc.farm.particle.cz")

for submAd in coll.query(htcondor.AdTypes.Submitter, 'true', ['Name', 'RunningJobs']):
  group = string.split(string.split(submAd['Name'],".")[0],"_")[1]
  groups.append(group)

for submAd in coll.query(htcondor.AdTypes.Submitter, 'true', ['Name', 'RunningJobs']):
  group = string.split(string.split(submAd['Name'],".")[0],"_")[1]
  user = string.split(string.split(submAd['Name'], "@")[0],".")[-1]
  #print submAd['Name']
  if group in groups:
    usergroups[group] += 1
    
print "Number of users in groups: "
print "==========================\n "
for group, user in usergroups.iteritems():
  #print "Number of users in group %s: %d" % (group, user)
  print '{0:10} ==> {1:10d}'.format(group, user)
