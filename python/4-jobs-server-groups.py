import string
import classad
import htcondor

from collections import defaultdict

coll = htcondor.Collector("htc.farm.particle.cz")

jobsgroups = defaultdict(int)

groups = []
jobnum = 0

for submAd in coll.query(htcondor.AdTypes.Submitter, 'true', ['Name', 'RunningJobs']):
  group = string.split(string.split(submAd['Name'],".")[0],"_")[1]
  groups.append(group)
  #print set(groups)

for scheddAd in coll.query(htcondor.AdTypes.Schedd, 'true', [ 'Name', 'MyAddress', 'ScheddIpAddr' ]): 
    servername = scheddAd['Name']
    print "\nServer %s" % (servername)
    print "==============================="

    schedd = htcondor.Schedd(scheddAd)
    query_iter = schedd.xquery()
    for job_ad in query_iter:
      accgroup = string.split(string.split(job_ad.get("AcctGroup"), ".")[0],"_")[1]
      if accgroup in groups:
	jobsgroups[accgroup] += 1

    for group, jobs in jobsgroups.iteritems():
      print "Number of running jobs for user group %s: %d" % (group, jobs)
