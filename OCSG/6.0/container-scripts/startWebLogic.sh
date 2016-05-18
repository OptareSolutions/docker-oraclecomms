#!/bin/sh

/u01/oracle/ocsg/wlserver/common/bin/wlst.sh -skipWLSModuleScanning /u01/oracle/ocsg-database-setup.py /u01/oracle/ocsg/user_projects/domains/ocsg-domain/

DOMAIN_HOME="/u01/oracle/ocsg/user_projects/domains/ocsg-domain"

${DOMAIN_HOME}/bin/startWebLogic.sh $*

