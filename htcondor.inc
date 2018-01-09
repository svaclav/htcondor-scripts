#!/bin/bash

#
# Environment variables and helper functions for custom HTCondor scripts.
#

export LC_ALL=C

AWK="/bin/awk"
CONDOR_HISTORY="/usr/bin/condor_history"
CONDOR_STATUS="/usr/bin/condor_status"
CONDOR_CONFIG="/etc/condor/config.d/10_security.config"

function find-server-names() {
  echo -e "$(grep -oP 'condor\@\$\(UID_DOMAIN\)\/[a-z]+[0-9]*\.farm\.particle\.cz' ${CONDOR_CONFIG} | cut -d '/' -f 2)\n"
}

function check-args() {

if [ -z "$1" ]
then
  echo -e ""
  echo -e "Please set server name as a argument to this command.\n"
  echo -e "You can use these servers: \n"
  find-server-names
  exit
fi
}
