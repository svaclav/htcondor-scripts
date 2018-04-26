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

coll = htcondor.Collector("htc.farm.particle.cz")

for scheddAd in coll.query(htcondor.AdTypes.Schedd, 'true', ['Name', 'ScheddIpAddr', 'MyAddress', 'TotalRunningJobs']):

  servername = scheddAd['Name']

  schedd = htcondor.Schedd(scheddAd)
  query_iter = schedd.xquery()
  print "Walltime for jobs running on %s: " % (servername)
  for job_ad in query_iter:
    if job_ad['CumulativeSlotTime'] != 0:
      print job_ad['Cmd'], job_ad['CumulativeSlotTime'], job_ad['RemoteUserCpu']

  totaljobs = scheddAd['TotalRunningJobs']
  if options.servers:
    print "Total jobs running on " + servername + ": " + str(totaljobs)
