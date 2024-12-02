from    flask        import Flask, make_response, render_template
from    subprocess   import check_output
from    flask        import request
from    flask        import Response
from    flask        import jsonify
import  pandas       as pd
import  sys
import  pyodbc   # For python3 MSSQL

import    netMonitor_util as util

app = Flask(__name__)

_dbHandler = None

## --------------------------------------------------
## --------------------------------------------------

# this simple routine uses trend_f and returns everything as string....
def get_shell_script_output_using_check_output(ini,fin,samples,fname):
    return "a"

## --------------------------------------------------

app = Flask(__name__)

## --------------------------------------------------

# valid route to get traffic RAW data. 
# eg: http://192.168.230.131:5000/get_traffic_data?samples=1000&ini=3&fin=4&fname=ACHA_INSE

@app.route('/get_traffic_data',methods=['GET',])
def home():
    ini = request.args.get('ini')
    fin = request.args.get('fin')
    samples = request.args.get('samples')
    fname = request.args.get('fname')

    response = make_response(get_shell_script_output_using_check_output(ini,fin,samples,fname))                                           
    # text as plain...
    response.headers['Content-Type'] = 'text/plain'            

    ## VERY VERY important.  read CORS....
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

## --------------------------------------------------

@app.route('/returnjson', methods = ['GET'])
def returnjson():
  if(request.method == 'GET'):
    data = {
         "Modules" : 15,
         "Subject" : "Data Structures and Algorithms",
         }
  return jsonify(data)


## --------------------------------------------------
## --------------------------------------------------

# eg: http://x.x.x.x:y/getDataForIP?ip=192.168.4.4

@app.route('/getDataForIP', methods=['GET',])
def getDataForIP():
  ip = request.args.get('ip')
  viewMode = "FULL" not in request.args.get('viewMode').upper()
  portType = "ALL" not in request.args.get('portType').upper()
  print(ip, ' ', viewMode, ' ', portType)
  df = util.getDataFromIP(_dbHandler, ip, viewMode, portType) 
  return df.to_json(orient='split', index=False)

## --------------------------------------------------

# eg: http://x.x.x.x:y/getDataForIP?mac=AABBCCDDEEFF
# MAC with no symbols, just hex. digits please!

@app.route('/getDataForMAC', methods=['GET',])
def getDataForMAC():
  mac = request.args.get('mac')
  viewMode = "FULL" not in request.args.get('viewMode').upper()
  portType = "ALL" not in request.args.get('portType').upper()
  print(mac, ' ', viewMode, ' ', portType)
  df = util.getDataFromMAC(_dbHandler, mac, viewMode, portType) 
  return df.to_json(orient='split', index=False)

## --------------------------------------------------

# eg: http://x.x.x.x:y/getDataForIP?mac=AABBCCDDEEFF
# MAC with no symbols, just hex. digits please!

@app.route('/getDevicesList', methods=['GET',])
def devicesList():
  dterm = request.args.get('term')
  print(dterm)
  df = util.getDevicesList(_dbHandler, dterm) 
  return  ( df.to_json(orient='records') )

## --------------------------------------------------

# eg: http://x.x.x.x:y/getDeviceInfo?id=x
# get info from switch ID = x

@app.route('/getSwitchInfo', methods=['GET',])
def deviceInfo():
  switchID = request.args.get('id')
  allMacs = "ALL"  in request.args.get('portType').upper()
  print(switchID, allMacs)
  df = util.getDeviceInfo(_dbHandler, switchID, allMacs) 
  return df.to_json(orient='split', index=False)

## --------------------------------------------------

# eg: http://x.x.x.x:y/getVLANList?q=200
# get info for VLANs

@app.route('/getVLANList', methods=['GET',])
def getVLAN():
  searchPattern = request.args.get('q')
  print(searchPattern)
  df = util.getVLANList(_dbHandler, searchPattern) 
  return  ( df.to_json(orient='records') )

## --------------------------------------------------

# eg: http://x.x.x.x:y/getMACPerVLAN?id=x
# get info from switch ID = x

@app.route('/getMACPerVLAN', methods=['GET',])
def vlanInfo():
  vlanID = request.args.get('id')
  #allPorts = "ALL"  in request.args.get('portType').upper()
  allPorts = True
  print(vlanID)
  df = util.getMACPerVLAN(_dbHandler, vlanID, allPorts) 
  return df.to_json(orient='split', index=False)

## --------------------------------------------------

# eg: http://x.x.x.x:y/getInterfaceErrorsList?q=x
# get list of abolute errors on interface = x

@app.route('/getInterfaceErrorsList', methods=['GET',])
def interfaceErrorsList():
  listType = request.args.get('listType')
  print(listType)
  print(type(listType))
  df = util.getInterfaceErrorList(_dbHandler, listType) 
  return df.to_json(orient='split', index=False)
 
## --------------------------------------------------

# eg: http://x.x.x.x:y/getInterfaceInputErrorsIncrementList?q=x
# get list of incremental input errors on interface = x

@app.route('/getInterfaceInputErrorsIncrementList', methods=['GET',])
def interfaceErrorsInputIncrementList():
  listType = request.args.get('listType')
  print(listType)
  print(type(listType))  
  df = util.getInterfaceIncrementalInputErrorList(_dbHandler, listType) 
  return df.to_json(orient='split', index=False) 
## --------------------------------------------------

# eg: http://x.x.x.x:y/getInterfaceOutputErrorsIncrementList?q=x
# get list of incremental input errors on interface = x

@app.route('/getInterfaceOutputErrorsIncrementList', methods=['GET',])
def interfaceErrorsOutputIncrementList():
  listType = request.args.get('listType')
  print(listType)
  print(type(listType))  
  df = util.getInterfaceIncrementalOutputErrorList(_dbHandler, listType) 
  return df.to_json(orient='split', index=False)

## --------------------------------------------------

# eg: http://x.x.x.x:y/getSwitchList?q=x
# get list of switches = x

@app.route('/getSwitchList', methods=['GET',])
def switchList():
  #vlanID = request.args.get('id')
  #allPorts = True
  #print(vlanID)
  df = util.getSwitchList(_dbHandler) 
  return df.to_json(orient='split', index=False)

## --------------------------------------------------

@app.route('/')
def hello():
    return render_template('index.html')

## --------------------------------------------------

@app.route('/netMonitor')
def interactive():
  return render_template('netReport.html', file='xx', devBWID=123 )

## --------------------------------------------------

## run application on port 5000, bind to internal IP, threaded version (threads to check....)
if __name__ == '__main__':
    
  _dbHandler = util.dbConnect()
  if (_dbHandler is None):
    print( sys.argv[0] + ' DB init error. Exiting....')
    exit(1)
  else:
    print( sys.argv[0] + ' DB init OK! ')
  

  app.run(host='10.14.2.251', port='5005', threaded=True, debug=True)

## --------------------------------------------------
## --------------------------------------------------
