#!/usr/bin/python

"""
Finds total jobs running on target host
First argument of this script is the name of the server
"""

import classad
import htcondor

from optparse import OptionParser

parser = OptionParser()
parser.add_option("-s", action="store_false", dest='servers', default=True, help="use all servers")

(options, args) = parser.parse_args()

jobsavail = 0

coll = htcondor.Collector("htc.farm.particle.cz")

#for scheddAd in coll.query(htcondor.AdTypes.Schedd, 'true', ['Name', 'ScheddIpAddr', 'MyAddress']):
#  for jobAd in htcondor.Schedd(scheddAd).query('true', ['Name', 'MyAddress', 'State']):
#    print jobAd['Name']

for startAd in coll.query(htcondor.AdTypes.Startd, 'true', ['Name', 'MyAddress', 'State']):
  state = startAd['State']
  if state == 'Available' or state == 'Unclaimed':
    print startAd['Name']
    jobsavail += 1
    #print startAd['State']
print "Total available/unclaimed jobs: " + str(jobsavail)
