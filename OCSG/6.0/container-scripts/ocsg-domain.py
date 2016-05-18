#=======================================================================================
# This is an example of WLST offline configuration script to create a co-located OCSG domain
#
# Usage:
#      java weblogic.WLST <WLST_script>
#
# Where:
#      <WLST_script> specifies the full path to the WLST script.
#=======================================================================================

#=======================================================================================
# Configuration (INPUT) Parameters
#=======================================================================================

# listen address input parameters
# example: hostname can be DNSName or IPAddress

AdminServerListenAddress = ""
AdminServerListenPort    =  7001

# Administrator configuration
adminName = "weblogic"
adminPassword = "welcome1"

# wlng.datasource configuration parameters

XADriver    = "com.mysql.jdbc.Driver"
XAURL       = "jdbc:mysql://mysqldb/ocsg"
XAUser      = "ocsg"
XAPassword  = "ocsg"

# wlng.localTX.datasource configuration parameters

nonXADriver   = "com.mysql.jdbc.Driver"
nonXAURL      = "jdbc:mysql://mysqldb/ocsg"
nonXAUser     = "ocsg"
nonXAPassword = "ocsg"

# optional path to JDK home
jdkHome = ""

#=======================================================================================
# Open a domain template.
#=======================================================================================

readTemplate('/u01/oracle/ocsg/wlserver/common/templates/wls/ocsg-domain.jar')

#=======================================================================================
# Configure the Administration Server and SSL port.
#=======================================================================================

print "Configuring the Administration Server"

cd('Servers/AdminServer')
set('ListenAddress', AdminServerListenAddress)
set('ListenPort', AdminServerListenPort)

#=======================================================================================
# Define the name of the domain as "ocsg-domain"
#=======================================================================================

cd('/')
set('Name','ocsg-domain')

#=======================================================================================
# Define the username and password for admin user. You must define the password before you
# can write the domain.
#=======================================================================================

cd('/')
cd('Security/ocsg-domain/User/weblogic')
cmo.setName(adminName)
cmo.setPassword(adminPassword)

#=======================================================================================
# Set Options:
# - CreateStartMenu:    Enable creation of Start Menu shortcut.
# - ServerStartMode:    Set mode to development.
# - OverwriteDomain:    Overwrites domain, when saving, if one exists.
#=======================================================================================

#setOption('CreateStartMenu', 'false')
setOption('ServerStartMode', 'dev')
setOption('OverwriteDomain', 'true')
if jdkHome != "":
    setOption('JavaHome', jdkHome)

#=======================================================================================
# Write the domain and close the domain template.
#=======================================================================================

print "Writing Domain"
writeDomain('/u01/oracle/ocsg/user_projects/domains/ocsg-domain')
closeTemplate()

#=======================================================================================
# Reopen the domain.
#=======================================================================================

print "Reading Domain"
readDomain('/u01/oracle/ocsg/user_projects/domains/ocsg-domain')

#=======================================================================================
# Configure wlng.datasource
#=======================================================================================
cd('/JDBCSystemResource/wlng.datasource/JdbcResource/wlng.datasource/JDBCDriverParams/NO_NAME_0')
set('DriverName', XADriver)
set('URL', XAURL)
set('PasswordEncrypted', XAPassword)
cd('Properties/NO_NAME_0/Property/user')
cmo.setValue(XAUser)

testTable =''
testConnection = 'false'

import re
isMySQL = re.search('mysql', XADriver, re.I) != None
isOracle = re.search('oracle', XADriver, re.I) != None

if isMySQL:
	testTable = 'SQL SELECT 1'
	testConnection = 'true'
if isOracle :
	testTable = 'SQL SELECT 1 FROM DUAL'
	testConnection = 'true'

cd('/JDBCSystemResource/wlng.datasource/JdbcResource/wlng.datasource/JDBCConnectionPoolParams/NO_NAME_0')
set('testTableName',testTable)
set('testConnectionsOnReserve', testConnection)

#=======================================================================================
# Configure wlng.localTX.datasource
#=======================================================================================

cd('/JDBCSystemResource/wlng.localTX.datasource/JdbcResource/wlng.localTX.datasource/JDBCDriverParams/NO_NAME_0')
set('DriverName', nonXADriver)
set('URL', nonXAURL)
set('PasswordEncrypted', nonXAPassword)
cd('Properties/NO_NAME_0/Property/user')
cmo.setValue(nonXAUser)

testTable =''
testConnection = 'false'

import re
isMySQL = re.search('mysql', nonXADriver, re.I) != None
isOracle = re.search('oracle', nonXADriver, re.I) != None

if isMySQL:
	testTable = 'SQL SELECT 1'
	testConnection = 'true'
if isOracle :
	testTable = 'SQL SELECT 1 FROM DUAL'
	testConnection = 'true'

cd('/JDBCSystemResource/wlng.localTX.datasource/JdbcResource/wlng.localTX.datasource/JDBCConnectionPoolParams/NO_NAME_0')
set('testTableName',testTable)
set('testConnectionsOnReserve', testConnection)

#=======================================================================================
# Assign application and jdbc system resource to the cluster
#=======================================================================================
print "Assigning jdbc system resources to cluster"

cd('/')
assign('JDBCSystemResource', 'wlng.datasource', 'Target', 'AdminServer')

cd('/')
assign('JDBCSystemResource', 'wlng.localTX.datasource', 'Target', 'AdminServer')

#=======================================================================================
# Deploying the portal
#=======================================================================================
print "Assigning jdbc system resources to cluster"

deploy('', '/u01/oracle/ocsg/ocsg/applications/')

#=======================================================================================
# Write the domain and close the domain template.
#=======================================================================================

print "Updating domain"
updateDomain()
closeDomain()
print "Closing domain"

#=======================================================================================
# Exit WLST.
#=======================================================================================

exit()
