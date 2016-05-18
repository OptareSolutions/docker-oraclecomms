#!/usr/bin/python

#=======================================================================================
# This script updates the database with administration user info for OCMA and OCSG.
# Usage:
#      java weblogic.WLST <WLST_script> <path to domain>
#
# Where:
#      <WLST_script> specifies the full path to the WLST script.
#      <path to domain> specifies the full path to an existing OCMA domain.
#=======================================================================================

import sys, os

from java.lang import String
from java.lang import System
from java.io import Console
from java.io import File
from java.lang import Class
from java.net import URLClassLoader
from java.net import URL

from com.oracle.cie.domain.security import SecurityHelper
from com.oracle.cie.domain import DomainInfoHelper;
from com.oracle.cie.domain.xml.security import UserType,SecurityInfo

CONFIG_JAR = "com.bea.cie.config-wlng_5.2.0.0.jar"
OCSG_UTIL_CLASS = "com.bea.wlcp.wlng.security.providers.authentication.account.util.OCSGDatabaseConfigUtil";
OCSG_DATASOURCE ="wlng.datasource"
OCSG_UTIL_JAR = "wlngSecurityProviders.jar";

datasourceNames = [OCSG_DATASOURCE]

#=============================================================================
# Main
#=============================================================================
def main():
  print("Setting up environment")
  # load the product properties
  props = System.getProperty("prod.props.file")
  loadProperties(props)

  #read the domain name
  if len(sys.argv) > 1 and sys.argv[1] != None :
    print("Reading domain: "+sys.argv[1])
    readDomain(sys.argv[1])
  else:
    print("No domain path specified")
    usage()

  dsMap = readDomainInfo(sys.argv[1])
  closeDomain()

  print("Setting up the database")
  setupDatabase(dsMap)
  exit()

#=============================================================================
# readPwd
#=============================================================================
def readPwd(user):

  cons = System.console()
  prompt = array(["Please enter password for user '"+user+"': "],String)
  if cons != None:
    pw = cons.readPassword("%s", prompt)
    if pw != None:
      s = String(pw)
      java.util.Arrays.fill(pw, ' ');
      return s
  else:
    # We assume there will be no more than a total of 5 arguments passed to this script.
    # Change if more arguments are added. Check is just a barf protection.
    if len(sys.argv) >= 4:
      for i in xrange(2,4):
        p = sys.argv[i].split('=')
        if p[0] == user:
          return p[1]
  return ''

#=============================================================================
# getClassloader
#=============================================================================
def getClassloader():
  jarPath = os.path.join(OCSG_HOME, "modules", CONFIG_JAR)
  classLoader = URLClassLoader(jarray.array([File(jarPath).toURI().toURL()], URL))
  return classLoader

#=============================================================================
# getAppPath
#=============================================================================
def getAppPath():
  appPath = os.path.join(OCSG_HOME, "applications")
  files = os.listdir(appPath)
  earName = [f for f in files if f.startswith(ADMIN_EAR_NAME)][0]
  appPath = os.path.join(appPath,earName)
  return appPath

#=============================================================================
# setupDatabase
#=============================================================================
def setupDatabase(dsMap):
  setupDatabaseOcsg(dsMap)
  print("Database successfully setup")

#=============================================================================
# setupDatabase for OCSG
#=============================================================================
def setupDatabaseOcsg(dsMap):
  try:
    jarPath = os.path.join(WL_HOME, "server", "lib", "mbeantypes", OCSG_UTIL_JAR)
    cl = URLClassLoader(jarray.array([File(jarPath).toURI().toURL()], URL))
    clz = cl.loadClass(OCSG_UTIL_CLASS)
    m = clz.getMethod("main",jarray.array([Class.forName("[Ljava.lang.String;")],Class))
    m.invoke(None, jarray.array([dsMap[OCSG_DATASOURCE]],Object))
  except Exception, ex:
      print "Unable to populate database", ex
      sys.exit(1)

#=============================================================================
# readDomainInfo
#=============================================================================
def readDomainInfo(dp):
  print("Reading database info from domain")
  dsMap = {}
  # get the SO user info.
  #si = SecurityHelper.parseSecurityFromDir(dp + File.separator + DomainInfoHelper.INFO_DIRECTORY)
  #admin = SecurityHelper.getAdminUser(si.getUserArray())
  soUser = "oracle"
  soUserPass = "welcome1"
  for dsName in datasourceNames:
    # get the db connection and user info
    cd('/JDBCSystemResource/'+dsName+'/JdbcResource/'+dsName+'/JDBCDriverParams/NO_NAME_0')
    dbUrl = get('URL')
    dbDriver = get('DriverName')
    cd('Properties/NO_NAME_0/Property/user')
    dbUser = get('Value')
    #dbPasswd = readPwd(dbUser)
    dbPasswd = "ocsg"
    cd('/')
    args = jarray.array([dbDriver, dbUrl, dbUser, dbPasswd, soUser, soUserPass], String)
    dsMap[dsName] = args
  del dbPasswd
  del soUserPass
  return dsMap

#=============================================================================
# usage
#=============================================================================
def usage():
	print("This script updates the database with administration user info for OCMA.")
	print("Usage:")
	print("   java weblogic.WLST <WLST_script> <path to domain>")
	print("Where:")
	print("   <WLST_script> specifies the full path to the WLST script.")
	print("   <path to domain> specifies the full path to an existing OCMA domain.")
	exit()


# Invoke main
if __name__== "main":
	main()
