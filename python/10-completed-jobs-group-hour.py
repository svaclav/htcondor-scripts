#!/usr/bin/python

"""
Finds total jobs running on target host
First argument of this script is the name of the server
"""

import string
import classad
import htcondor

from collections import defaultdict

jobsgroups = defaultdict(int)

groups = []

from optparse import OptionParser

parser = OptionParser()
parser.add_option("-s", action="store_false", dest='servers', default=True, help="use all servers")

(options, args) = parser.parse_args()

coll = htcondor.Collector("htc.farm.particle.cz")

for submAd in coll.query(htcondor.AdTypes.Submitter, 'true', ['Name', 'RunningJobs']):
  group = string.split(string.split(submAd['Name'],".")[0],"_")[1]
  groups.append(group)

for scheddAd in coll.query(htcondor.AdTypes.Schedd, 'true', [ 'Name', 'MyAddress', 'ScheddIpAddr' ]): 
  schedd = htcondor.Schedd(scheddAd)
  for jobAd in schedd.history('true', ['AcctGroup', 'CompletionDate', 'JobStatus'], 200):
    accgroup = string.split(string.split(jobAd['AcctGroup'], ".")[0],"_")[1]
    if jobAd['JobStatus'] == 4:
      jobsgroups[accgroup] += 1

print "Number of completed jobs according to groups: "
print "=============================================\n "
for group, jobs in jobsgroups.iteritems():
  #print "Number of completed jobs according to group %s: %d" % (group, jobs)
  print '{0:10} ==> {1:10d}'.format(group, jobs)
