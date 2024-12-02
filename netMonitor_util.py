
import  pyodbc   # For python3 MSSQL
import  pandas       as pd
import 	datetime
import traceback

#_DB_SERVER = 'BRJTXSNSRV01.bar.nucorsteel.local'
_DB_SERVER = '10.14.2.227'
_DB_DATABASE = 'networkInfo'
_DB_USER = 'JewettTests'
_DB_PASS = '#NstxErcot#'

## ------------------------------------------------------------------
# ------------------------------------------------------------------

## DB Connect
    
def dbConnect():

  ## get driver
  driver =  [item for item in pyodbc.drivers()]
  if len(driver) == 0:
    raise Exception("No driver found")

  driver = driver[-1]
  print(driver)

  conn_string = (f"Driver={driver};Server={_DB_SERVER};\
      Database={_DB_DATABASE};UID={_DB_USER}; PWD={_DB_PASS};Encrypt=no")
  
  print(conn_string)

  try:
    #conn_string = 'DRIVER={ODBC Driver 18 for SQL Server};' 'SERVER=' + _DB_SERVER + ';DATABASE=' + _DB_DATABASE + \
    #                ';UID=' + _DB_USER + ';PWD=' + _DB_PASS + ';Encrypt=No'

    print (conn_string)  
    _sql_conn = pyodbc.connect(conn_string)
  except Exception as e:  
    print ("Exception:::", e)
    logging.info("Exception:::")
    logging.info(e)
  return(_sql_conn)

## ------------------------------------------------------------------

## DB Close
   
def dbClose(conn):
  conn.close()
  return(None)

## ------------------------------------------------------------------
## ------------------------------------------------------------------

## get Network info for any specific MAC

def getDataFromMAC(sql_conn, mac, simpleData=True, accessOnly=True ):


  retValue=0
  try:

 
    sqlStr = """SELECT TOP(400)
      mac.mac as MAC, mac.vlan as "MAC VLAN", vendor.vendor as Vendor, arp.mac as "ARP MAC", arp.ip as "ARP IP", 
      arp.vlan as "ARP VLAN", arp.age as "ARP AGE",  
      IIF(CHARINDEX('Port-channel',mac.port) > 0 , REPLACE(mac.port, 'Port-channel', 'Po') , mac.port) as SwitchPort,
      CONCAT( dev.hostname, ' - (' ,dev.ip, ')' ) as "Switch",
      inte.name as "Int. name", inte.vlan as "Int V/T", inte.vlanNumber as "Int. VLAN#", inte.status as "Int. stat", inte.description as "Int. desc",
      (case when arp.lastUpdate < mac.lastUpdate and arp.lastUpdate < dev.lastUpdate then arp.lastUpdate 
      when mac.lastUpdate < dev.lastUpdate then mac.lastUpdate else dev.lastUpdate end) as lastUpdate,
      mac.lastUpdate as "MAC last seen", arp.lastUpdate as "ARP last seen", dev.lastUpdate as "Switch last seen"
    FROM 
      mac mac LEFT JOIN 
      arp arp on arp.mac=mac.mac LEFT JOIN
      devices dev on mac.deviceID=dev.id LEFT JOIN 
      interfaces inte on inte.deviceID=dev.id and (mac.port=inte.name  OR  IIF(CHARINDEX('Port-channel',mac.port) > 0 , REPLACE(mac.port, 'Port-channel', 'Po') , mac.port) = inte.name ) LEFT JOIN
      macvendor vendor ON UPPER(LEFT(vendor.mac,6))=UPPER(LEFT(arp.mac,6))
      WHERE upper(mac.mac) LIKE upper('%{}%')
      AND  DATEDIFF(minute, arp.lastUpdate, getdate()) < 360     
	  AND  DATEDIFF(minute, mac.lastUpdate, getdate()) < 360
	  AND  DATEDIFF(minute, dev.lastUpdate, getdate()) < 360""".format(mac)     
    

    df = pd.read_sql(sqlStr, sql_conn)
    df['MAC last seen'] = df['MAC last seen'].apply(lambda x: x.strftime('%m/%d %H:%M'))
    df['Switch last seen'] = df['Switch last seen'].apply(lambda x: x.strftime('%m/%d %H:%M'))
    df['ARP last seen'] = df['ARP last seen'].apply(lambda x: x.strftime('%m/%d %H:%M'))
    df['lastUpdate'] = df['lastUpdate'].apply(lambda x: x.strftime('%m/%d %H:%M'))
    #sql_conn.close()

    #print (df.dtypes)

  except Exception as e:  
    print ("Exception:::", e)
    print ('Cannot connect to DB' )

  if (accessOnly is not None and accessOnly):
    df = df[ df['Int. VLAN#'] > 0]

  if (simpleData is not None and simpleData):
    return(df[['MAC','Vendor', 'MAC VLAN', 'ARP IP', 'Switch', 'SwitchPort', 'lastUpdate']])
  else:
    return(df)


## ------------------------------------------------------------------

## get Network info for any specific IP

def getDataFromIP(sql_conn, ip, simpleData=True, accessOnly=True ):


  retValue=0
  try:
 
    sqlStr = """SELECT TOP(400)
      arp.ip as "ARP IP", arp.mac as "ARP MAC", arp.vlan as "ARP VLAN", arp.age as "ARP AGE",
      mac.mac as MAC, mac.vlan as "MAC VLAN", vendor.vendor as Vendor,  
      IIF(CHARINDEX('Port-channel',mac.port) > 0 , REPLACE(mac.port, 'Port-channel', 'Po') , mac.port) as SwitchPort,
      CONCAT( dev.hostname, ' - (' ,dev.ip, ')' ) as "Switch",
      inte.name as "Int. name", inte.vlan as "Int V/T", inte.vlanNumber as "Int. VLAN#", inte.status as "Int. stat", inte.description as "Int. desc",
      (case when arp.lastUpdate < mac.lastUpdate and arp.lastUpdate < dev.lastUpdate then arp.lastUpdate 
      when mac.lastUpdate < dev.lastUpdate then mac.lastUpdate else dev.lastUpdate end) as lastUpdate,
      mac.lastUpdate as "MAC last seen", arp.lastUpdate as "ARP last seen", dev.lastUpdate as "Switch last seen"
    FROM 
      arp arp LEFT JOIN 
      mac mac on arp.mac=mac.mac LEFT JOIN
      devices dev on mac.deviceID=dev.id LEFT JOIN 
      interfaces inte on inte.deviceID=dev.id and (mac.port=inte.name  OR  IIF(CHARINDEX('Port-channel',mac.port) > 0 , REPLACE(mac.port, 'Port-channel', 'Po') , mac.port) = inte.name ) LEFT JOIN
      macvendor vendor ON UPPER(LEFT(vendor.mac,6))=UPPER(LEFT(arp.mac,6))
      WHERE upper(arp.ip) LIKE upper('%{}')
      AND  DATEDIFF(minute, arp.lastUpdate, getdate()) < 360     
	  AND  DATEDIFF(minute, mac.lastUpdate, getdate()) < 360
	  AND  DATEDIFF(minute, dev.lastUpdate, getdate()) < 360""".format(ip)     
    

    df = pd.read_sql(sqlStr, sql_conn)
    df['MAC last seen'] = df['MAC last seen'].apply(lambda x: x.strftime('%m/%d %H:%M'))
    df['Switch last seen'] = df['Switch last seen'].apply(lambda x: x.strftime('%m/%d %H:%M'))
    df['ARP last seen'] = df['ARP last seen'].apply(lambda x: x.strftime('%m/%d %H:%M'))
    df['lastUpdate'] = df['lastUpdate'].apply(lambda x: x.strftime('%m/%d %H:%M'))
    #sql_conn.close()

  except Exception as e:  
    print ("Exception:::", e)
    print ('Cannot connect to DB' )

  if (accessOnly is not None and accessOnly):
    df = df[ df['Int. VLAN#'] > 0]

  if (simpleData is not None and simpleData):
    return(df[['MAC','Vendor', 'MAC VLAN', 'ARP IP', 'Switch', 'SwitchPort', 'lastUpdate']])
  else:
    return(df)

## ------------------------------------------------------------------

## get Network info for any specific IP

def getDevicesList(sql_conn, dataString):
  retValue=0
  try:

    sqlStr = """  SELECT DISTINCT TOP(100) 
      id, CONCAT( dev.hostname, ' - (' ,dev.ip, ')' ) as text FROM 
      devices dev WHERE dev.hostname like '%{}%' OR dev.ip like '%{}%'
      ORDER BY CONCAT( dev.hostname, ' - (' ,dev.ip, ')' )""".format(dataString, dataString)

    df = pd.read_sql(sqlStr, sql_conn)
    #sql_conn.close()

  except Exception as e:  
    print ("Exception:::", e)
    print ('Cannot connect to DB' )

  return(df)


## ------------------------------------------------------------------

## get Switch info

def getDeviceInfo(sql_conn, switchID, allMacs):
  retValue=0
  try:
  
    # get device info
    sqlStr = """SELECT id as deviceID, TRIM(hostname) as hostname, TRIM(ip) as ip, TRIM(COALESCE(adminIP, '---')) as adminIP,
      TRIM(serialNum) as serialNum, TRIM(platform) as platform, TRIM(net) as net,
      TRIM(uptime) as uptime, lastUpdate as devLast
      FROM devices dev WHERE dev.id={}""".format(switchID)
    dfDevice = pd.read_sql(sqlStr, sql_conn)
    
    # get interface info
    sqlStr = """SELECT deviceID, TRIM(name) as name, TRIM(description) as description, trim(status) as status, 
      TRIM(vlan) as vlan, vlanNumber, TRIM(type) as type, TRIM(speed) as  speed, TRIM(duplex) as duplex, lastUpdate as intLast
      FROM interfaces inte WHERE inte.deviceID={}""".format(switchID)
    dfIface = pd.read_sql(sqlStr, sql_conn)

    ## merge INTERFACES (N) AND DEVICE (1)
    dfIntDev = pd.merge(dfIface, dfDevice, how="left", on=["deviceID", "deviceID"])

    # get MAC info
    sqlStr = """SELECT mac.deviceID as deviceID, TRIM(mac.mac) as mac, max(mac.lastUpdate) as macLast, TRIM(mac.port) as port , 
      TRIM(mac.type) as type FROM mac mac where mac.deviceID = {}
	  AND   ( ( DATEDIFF(minute, ( mac.lastUpdate ), getdate()) < 180 ) OR mac.lastUpdate IS NULL )
	  group by mac.deviceID,  mac.mac, port, vlan, type order by mac""".format(switchID)
	  
    dfMAC = pd.read_sql(sqlStr, sql_conn)
    dfMAC['port'] = dfMAC['port'].str.replace('Port-channel','Po')
    dfMAC['port'] = dfMAC['port'].str.replace('TenGigabitEthernet','Te')
    dfMAC['port'] = dfMAC['port'].str.replace('TwentyFiveGigE','Twe')
    dfMAC['port'] = dfMAC['port'].str.replace('HundredGigE','Hu')

    ## remove column 'type' 
    dfMAC.drop(columns=['type'], inplace=True)

    # only last mac per port/device
    if (allMacs is None or (allMacs is not None and allMacs is False)):
      dfMAC = dfMAC.groupby(by=['deviceID','port'], as_index=False).agg({'macLast': 'max', 'mac': 'last' }) 

    print(dfMAC)

    ## merge interfaces and MAC addresses, and delet some columns
    dfIntDevMac = pd.merge(dfIntDev, dfMAC, how="left", left_on=["deviceID","name"], right_on=["deviceID","port"])
    dfIntDevMac.drop(columns=['port', 'uptime', 'platform', 'net', 'adminIP', 'deviceID', 'serialNum', 'ip', 'hostname', 'devLast'], inplace=True)
    
    dfIntDevMac['macLast'] = dfIntDevMac['macLast'].astype("datetime64[ns]")
    dfIntDevMac['intLast'] = dfIntDevMac['intLast'].astype("datetime64[ns]")
    
    dfIntDevMac['macLast'] = dfIntDevMac['macLast'].dt.strftime('%m/%d %H:%M')
    dfIntDevMac['intLast'] = dfIntDevMac['intLast'].dt.strftime('%m/%d %H:%M')
    
    dfIntDevMac['matchingMac'] = dfIntDevMac['mac'].str[:6]   # get first 6 charactes of MAC to match on vendor
    dfIntDevMac.fillna('-', inplace=True)

    # get Vendor info
    sqlStr = """select TRIM(mac) as matchingMac, TRIM(vendor) as vendor from macVendor"""
    dfVendor = pd.read_sql(sqlStr, sql_conn)

    ## merge interfaces + MAC with Vendors
    dfIntDevMacVendor = pd.merge(dfIntDevMac, dfVendor, how="left", left_on=["matchingMac"], right_on=["matchingMac"])
    dfIntDevMacVendor.fillna('-', inplace=True)

    # get ARP info
    sqlStr = """SELECT TRIM(mac) as mac, TRIM(ip) as ip, TRIM (vlan) as arpVlan, lastupdate as arpLast from arp 
	  where ( ( DATEDIFF(minute, ( arp.lastUpdate ), getdate()) < 180 ) OR arp.lastUpdate IS NULL )"""
    dfARP = pd.read_sql(sqlStr, sql_conn)
    dfARP['arpLast'] = dfARP['arpLast'].astype("datetime64[ns]")
    dfARP['arpLast'] = dfARP['arpLast'].dt.strftime('%m/%d %H:%M')
    
    #sql_conn.close()

    ## merge Dev + Int + Mac + vendor with ARP (IP)
    dfARP = dfARP.groupby(by=['mac'], as_index=False).agg({'arpLast': 'max', 'ip': 'last', 'arpVlan':'last' }) 
    dfIntDevMacVendorArp = pd.merge(dfIntDevMacVendor, dfARP, how="left", on=["mac", "mac"])
    dfIntDevMacVendorArp.fillna('-', inplace=True)

    dfIntDevMacVendorArp['length'] = dfIntDevMacVendorArp['name'].str.len()
    dfIntDevMacVendorArp.sort_values ( by = ['length', 'name'], ascending = [True, True], na_position = 'first', inplace=True)

    #print(dfIntDevMacVendorArp) 

  except Exception as e:  
	  
    traceback.print_exc()
	  
    print ("Exception:::", e)
    print ('Cannot connect to DB' )

  #if (allPorts is not None and allPorts is not True):
  #  df = df[ df['Status'] == 'connected']

  return(dfIntDevMacVendorArp[['name','status', 'description','vlan', 'mac', 'ip', 'vendor','type', 'macLast', 'arpLast']])

## ------------------------------------------------------------------

## get VLAN List for Select2

def getVLANList(sql_conn, searchPattern):
  retValue=0
  try:
 
    sqlStr = """
      SELECT TOP (1000) 
      id as id
	  ,CONCAT(TRIM([net]),' - VLAN ', vlan, ' - ', [description]) as text
      FROM [networkInfo].[dbo].[vlan]
      WHERE ( UPPER(STR([vlan])) LIKE UPPER('%{}%') 
      OR  (UPPER([description]) LIKE UPPER('%{}%')) )""".format(searchPattern, searchPattern)

    df = pd.read_sql(sqlStr, sql_conn)
    #sql_conn.close()

  except Exception as e:  
    print ("Exception:::", e)
    print ('Cannot connect to DB' )

  return(df)

## ------------------------------------------------------------------

## get MACs/IPs per VLAN

def getMACPerVLAN(sql_conn, vlanID, allPorts):
  retValue=0
  try:
 
    sqlStr = """
       --- show MACS on VLAN,  only access ports 
       select top(2000)
       vlan.vlan as "VLAN #", vlan.net as "BUS / PRO", vlan.description as VLAN_NAME,
       mac.mac as MAC, vendor.vendor as "Vendor", 
       arp.ip as "IP",
       dev.hostname as "Switch Name", 
       inte.name as "Port", inte.status as Status, inte.description, 
       mac.lastUpdate as "MAC Last Seen"
       --, arp.lastUpdate as "ARP LastSeen", inte.lastUpdate as "Int. LastSeen", dev.lastUpdate as "Device lastSeen"
    FROM 
      [networkInfo].[dbo].[vlan] vlan LEFT JOIN
      [networkInfo].[dbo].[mac] mac on mac.vlan = vlan.vlan LEFT JOIN 
      [networkInfo].[dbo].[devices] dev on mac.deviceID=dev.id LEFT JOIN 
      [networkInfo].[dbo].[arp] arp on mac.mac = arp.mac LEFT JOIN 
      [networkInfo].[dbo].[interfaces] inte on inte.deviceID=dev.id AND 
      (mac.port=inte.name  OR  IIF(CHARINDEX('Port-channel',mac.port) > 0 , REPLACE(mac.port, 'Port-channel', 'Po') , mac.port) = inte.name ) LEFT JOIN
      [networkInfo].[dbo].[macVendor] vendor ON UPPER(LEFT(vendor.mac,6))=UPPER(LEFT(mac.mac,6))
      where vlan.id = {}
      AND  LEN(dev.hostname) > 4  
      AND inte.vlanNumber>0
      order by dev.id, mac.mac asc""".format(vlanID)

    df = pd.read_sql(sqlStr, sql_conn)
    #sql_conn.close()
    
    df['MAC Last Seen'] = df['MAC Last Seen'].apply(lambda x: x.strftime('%m/%d %H:%M'))

  except Exception as e:  
    print ("Exception:::", e)
    print ('Cannot connect to DB' )

#  if (allPorts is not None and allPorts is not True):
#    df = df[ df['Status'] == 'connected']

  return(df)

## ------------------------------------------------------------------

## get MACs/IPs per VLAN

def getSwitchList(sql_conn):
  retValue=0
  try:

 
    sqlStr = """SELECT TOP (1000) [hostname]
      , IIF(LEN([adminIP]) > 2,adminIP, [ip]) as Switch_IP
      ,[serialNum] as Serial
      ,[platform] as Platform
      ,[net] as "BUSI/PROD"
      ,[uptime] as Uptime
      ,[lastUpdate] as "Last Update"
	  ,CONCAT('ssh://', IIF(LEN([adminIP]) > 2, [adminIP], [ip])) as "SSH link"
     FROM [networkInfo].[dbo].[devices]
     WHERE LEN(COALESCE ([hostname], '-')) > 3
     ORDER BY [hostname]"""

    df = pd.read_sql(sqlStr, sql_conn)
    #sql_conn.close()
    
    df['Last Update'] = df['Last Update'].apply(lambda x: x.strftime('%m/%d %H:%M'))

  except Exception as e:  
    print ("Exception:::", e)
    print ('Cannot connect to DB' )

  return(df)

## ------------------------------------------------------------------

## get Interfaces error (absolute count)

def getInterfaceErrorList(sql_conn, listType='OnlyTrafficInt'):
  retValue=0
  try:
 
    if (listType=='OnlyTrafficInt'):
      sqlStr = """SELECT TOP (20000) 
      dev.hostname as Switch
      ,[interfaceName] ,[inputRate] ,[outputRate]
      ,[inputErrors],[outputErrors] ,[crcErrors]
      ,[collisionErrors] ,[datetime] as LastSampleTime
      FROM [networkInfo].[dbo].[interfaceErrors] err
      LEFT jOIN [networkInfo].[dbo].[devices] dev 
      ON err.deviceID = dev.id
      WHERE [datetime]  > DATEADD(MINUTE,-150, GETDATE())
      AND ([inputRate] + [outputRate]) > 10
      AND ([inputErrors] + [outputErrors]) > 1
      ORDER BY ([inputErrors]+[outputErrors]) desc"""     
    else:
      sqlStr = """SELECT TOP (20000) 
      dev.hostname as Switch
      ,[interfaceName] ,[inputRate] ,[outputRate]
      ,[inputErrors],[outputErrors] ,[crcErrors]
      ,[collisionErrors] ,[datetime] as LastSampleTime
      FROM [networkInfo].[dbo].[interfaceErrors] err
      LEFT jOIN [networkInfo].[dbo].[devices] dev 
      ON err.deviceID = dev.id
      WHERE [datetime]  > DATEADD(MINUTE,-150, GETDATE())
      AND ([inputErrors] + [outputErrors]) > 1
      ORDER BY ([inputErrors]+[outputErrors]) desc"""      

    df = pd.read_sql(sqlStr, sql_conn)
    #sql_conn.close()
    
    df['LastSampleTime'] = df['LastSampleTime'].apply(lambda x: x.strftime('%m/%d %H:%M'))

  except Exception as e:  
    print ("Exception:::", e)
    print ('Cannot connect to DB' )

  return(df)


## ------------------------------------------------------------------

## get Interfaces error (incremental, Input errors)

def getInterfaceIncrementalInputErrorList(sql_conn, listType='OnlyTrafficInt'):
  retValue=0
  try:
 
    if (listType=='OnlyTrafficInt'):
      sqlStr = """SELECT TOP (100000) 
      dev.hostname as Switch
      ,[interfaceName] ,[inputRate] ,[outputRate]
      ,[inputErrors],[outputErrors] ,[crcErrors]
      ,[collisionErrors] ,[datetime] as LastSampleTime
      FROM [networkInfo].[dbo].[interfaceErrors] err
      LEFT jOIN [networkInfo].[dbo].[devices] dev 
      ON err.deviceID = dev.id
      WHERE ([inputRate] + [outputRate]) > 10
      AND ([inputErrors] + [outputErrors]) > 1
      ORDER BY [datetime] ASC"""
    else:
      sqlStr = """SELECT TOP (100000) 
      dev.hostname as Switch
      ,[interfaceName] ,[inputRate] ,[outputRate]
      ,[inputErrors],[outputErrors] ,[crcErrors]
      ,[collisionErrors] ,[datetime] as LastSampleTime
      FROM [networkInfo].[dbo].[interfaceErrors] err
      LEFT jOIN [networkInfo].[dbo].[devices] dev 
      ON err.deviceID = dev.id
      WHERE ([inputErrors] + [outputErrors]) > 1
      ORDER BY [datetime] ASC"""

    errorListIncrementDF = pd.read_sql(sqlStr, sql_conn)
    #sql_conn.close()
    
    # Filter valid hostnames 
    errorListIncrementDF  =  errorListIncrementDF.loc[errorListIncrementDF['Switch'].str.len() > 2]
    
    # format date time
    #errorListIncrementDF['LastSampleTime'] = errorListIncrementDF['LastSampleTime'].apply(lambda x: x.strftime('%m/%d %H:%M'))
    
    # build groups by host/interface
    switchInterfaceGroups = errorListIncrementDF.groupby(['Switch', 'interfaceName'])

    # create empty dataframes for input/output errors
    dfInputErrors = pd.DataFrame(columns=['Switch','interfaceName','inputErrorsMin','inputErrorsMax', 'firstSampleTime', 'lastSampleTime', 'deltaTimeHours'])

    for name, group in switchInterfaceGroups:
      if (group['inputErrors'].is_monotonic_increasing  and group['inputErrors'].is_unique) == True:
        print(f"Monotonic increasing (IN): {name} ", group['inputErrors'].is_monotonic_increasing  and group['inputErrors'].is_unique)
        deltaInputErrors = group.agg({'inputErrors': ['min', 'max']}) 
        deltaTime = group.agg({'LastSampleTime': ['min', 'max']}) 

        difference = ( ( deltaTime.loc['max'][0] - deltaTime.loc['min'][0] )  )
        seconds = difference.total_seconds()  
        strHours = '{:.2f}'.format(seconds / 3600)

        deltaTime['LastSampleTime'] = deltaTime['LastSampleTime'].apply(lambda x: x.strftime('%m/%d %H:%M'))

        myList = (name[0], name[1], deltaInputErrors.loc['min'][0], deltaInputErrors.loc['max'][0] ,deltaTime.loc['min'][0], deltaTime.loc['max'][0], strHours)
        dfInputErrors.loc[len(dfInputErrors)] = myList
        dfInputErrors.loc[len(dfInputErrors)] = myList

  except Exception as e:  
    print ("Exception:::", e)
    print ('Cannot connect to DB' )

  return(dfInputErrors)

## ------------------------------------------------------------------

## get Interfaces error (incremental, Output errors)

def getInterfaceIncrementalOutputErrorList(sql_conn, listType='OnlyTrafficInt'):
  retValue=0
  try:
 
    if (listType=='OnlyTrafficInt'):
      sqlStr = """SELECT TOP (100000) 
      dev.hostname as Switch
      ,[interfaceName] ,[inputRate] ,[outputRate]
      ,[inputErrors],[outputErrors] ,[crcErrors]
      ,[collisionErrors] ,[datetime] as LastSampleTime
      FROM [networkInfo].[dbo].[interfaceErrors] err
      LEFT jOIN [networkInfo].[dbo].[devices] dev 
      ON err.deviceID = dev.id
      WHERE ([inputRate] + [outputRate]) > 10
      AND ([inputErrors] + [outputErrors]) > 1
      ORDER BY [datetime] ASC"""
    else:
      sqlStr = """SELECT TOP (100000) 
      dev.hostname as Switch
      ,[interfaceName] ,[inputRate] ,[outputRate]
      ,[inputErrors],[outputErrors] ,[crcErrors]
      ,[collisionErrors] ,[datetime] as LastSampleTime
      FROM [networkInfo].[dbo].[interfaceErrors] err
      LEFT jOIN [networkInfo].[dbo].[devices] dev 
      ON err.deviceID = dev.id
      WHERE ([inputErrors] + [outputErrors]) > 1
      ORDER BY [datetime] ASC"""

    errorListIncrementDF = pd.read_sql(sqlStr, sql_conn)
    #sql_conn.close()
    
    # Filter valid hostnames 
    errorListIncrementDF  =  errorListIncrementDF.loc[errorListIncrementDF['Switch'].str.len() > 2]
    
    # format date time
    #errorListIncrementDF['LastSampleTime'] = errorListIncrementDF['LastSampleTime'].apply(lambda x: x.strftime('%m/%d %H:%M'))
    
    # build groups by host/interface
    switchInterfaceGroups = errorListIncrementDF.groupby(['Switch', 'interfaceName'])

    # create empty dataframes for input/output errors
    dfOutputErrors = pd.DataFrame(columns=['Switch','interfaceName','outputErrorsMin','outputErrorsMax', 'firstSampleTime', 'lastSampleTime', 'deltaTimeHours'])

    for name, group in switchInterfaceGroups:
      if (group['outputErrors'].is_monotonic_increasing  and group['outputErrors'].is_unique) == True:
        print(f"Monotonic increasing (IN): {name} ", group['outputErrors'].is_monotonic_increasing  and group['inputErrors'].is_unique)
        deltaOutputErrors = group.agg({'outputErrors': ['min', 'max']}) 
        deltaTime = group.agg({'LastSampleTime': ['min', 'max']}) 

        difference = ( ( deltaTime.loc['max'][0] - deltaTime.loc['min'][0] )  )
        print( ( deltaTime.loc['max'][0] - deltaTime.loc['min'][0] )  )
        seconds = difference.total_seconds()  
        strHours = '{:.2f}'.format(seconds / 3600)

        deltaTime['LastSampleTime'] = deltaTime['LastSampleTime'].apply(lambda x: x.strftime('%m/%d %H:%M'))

        myList = (name[0], name[1], deltaOutputErrors.loc['min'][0], deltaOutputErrors.loc['max'][0] ,deltaTime.loc['min'][0], deltaTime.loc['max'][0], strHours)
        dfOutputErrors.loc[len(dfOutputErrors)] = myList
        dfOutputErrors.loc[len(dfOutputErrors)] = myList

  except Exception as e:  
    print ("Exception:::", e)
    print ('Cannot connect to DB' )

  return(dfOutputErrors)

## ------------------------------------------------------------------
## ------------------------------------------------------------------

