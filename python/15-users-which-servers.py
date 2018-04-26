#!/usr/bin/python

"""
Finds total jobs running on target host
First argument of this script is the name of the server
"""

import string
import classad
import htcondor

from collections import defaultdict

userhosts = defaultdict(int)

groups = []
users = []

from optparse import OptionParser

parser = OptionParser()
parser.add_option("-s", action="store_false", dest='servers', default=True, help="use all servers")

(options, args) = parser.parse_args()


coll = htcondor.Collector("htc.farm.particle.cz")

for submAd in coll.query(htcondor.AdTypes.Submitter, 'true', ['Name', 'RunningJobs']):
  user = string.split(string.split(submAd['Name'], "@")[0],".")[-1]
  users.append(user)

for submAd in coll.query(htcondor.AdTypes.Submitter, 'true', ['Name', 'RunningJobs', 'ScheddName']):
  user = string.split(string.split(submAd['Name'], "@")[0],".")[-1]
  servername = submAd['ScheddName']
  if user in users:
    userhosts[user] = servername
  
print "User's jobs are running on these servers:"
print "==========================================\n "
for users, servers in sorted(userhosts.iteritems()):
  print '{0:14} ==> {1:10s}'.format(users, servers)
