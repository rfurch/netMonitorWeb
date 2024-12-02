//------------------------------------------
//------------------------------------------

// destroy and recreate data table
function deleteAndCreateTable() {
	if ( $.fn.DataTable.isDataTable( '#example' ) ) {
	  $('#example').DataTable().destroy(true);
	  $('#example').dataTable().remove();
	  $('#TableContainer').prepend("<table id='example' class='display compact' style='width:80%'>");
	  }
	}  
	 
//------------------------------------------

function readMAC() {
  var mac = $('#MACData').val();
  mac = mac.replace(/\./g, "");
  mac = mac.replace(/\:/g, "");
  mac = mac.replace(/\ /g, "");
  mac = mac.replace(/\-/g, "");
  return([mac, mac.length]);   	   
}

//------------------------------------------

function readIP() {
  var ip = $('#IPData').val();
  ip = ip.replace(/\ /g, "");
  return([ip, ip.length]);   	   
}


//------------------------------------------

// show MAC info int a table!	 
function getMacInfo(mac) {
  
  var portType = $("input:radio[name ='radioAccess']:checked").val();
  var viewMode = $("input:radio[name ='viewAccess']:checked").val();

  $.ajax( {
//    url: 'http://10.14.2.81:5000/getDataForMAC?mac=' + mac + '&viewMode=' + viewMode + '&portType=' + portType ,
    url: '/getDataForMAC?mac=' + mac + '&viewMode=' + viewMode + '&portType=' + portType ,
    dataType: 'json',
    success: function ( jsonData ) {
    var vColumns = [];

    columnNumbers = Object.keys(jsonData.columns);
    columnNames = Object.values(jsonData.columns);
  
  for (var i in columnNames) {
	vColumns.push({data: columnNumbers[i], title: columnNames[i]});
	}

  deleteAndCreateTable();
  $('#example').DataTable( {
	  //retrieve: true,
	  destroy: true,
	  
	  columns: vColumns,
	  data: jsonData.data,
	  dom: 'Bfrtipl',
	   "paging": true,
	  "pageLength": 25,
	  "lengthMenu": [ [10, 25, 50, 100, -1], [10, 25, 50, 100, "All"] ],
	  buttons: [ 'copy', 'csv', 'excel', 'pdf', 'print' ],
	  } );
	} } );		  
}		 

//------------------------------------------

// show IP  info into a table!	 

function getIPInfo(ip) {
  
var portType = $("input:radio[name ='IPradioAccess']:checked").val();
var viewMode = $("input:radio[name ='IPviewAccess']:checked").val();

$.ajax( {
//url: 'http://10.14.2.81:5000/getDataForIP?ip=' + ip + '&viewMode=' + viewMode + '&portType=' + portType ,
url: '/getDataForIP?ip=' + ip + '&viewMode=' + viewMode + '&portType=' + portType ,
dataType: 'json',
success: function ( jsonData ) {
  var vColumns = [];

  columnNumbers = Object.keys(jsonData.columns);
  columnNames = Object.values(jsonData.columns);
  
  for (var i in columnNames) {
	vColumns.push({data: columnNumbers[i], title: columnNames[i]});
	}

  deleteAndCreateTable();
  $('#example').DataTable( {
	  //retrieve: true,
	  destroy: true,
	  
	  columns: vColumns,
	  data: jsonData.data,
	  dom: 'Bfrtipl',
	   "paging": true,
	  "pageLength": 25,
	  "lengthMenu": [ [10, 25, 50, 100, -1], [10, 25, 50, 100, "All"] ],
	  buttons: [ 'copy', 'csv', 'excel', 'pdf', 'print' ],
	  } );
	} } );		  
}		 

//------------------------------------------

function getVLANInfo(vlanID) {
	
// get radio check box all parts / connected ports 
//var portType = $("input:radio[name ='SwitchPorts']:checked").val();
var portType = true;

	
$.ajax( {
//url: 'http://10.14.2.81:5000/getMACPerVLAN?id=' + vlanID + '&portType=' + portType,
url: '/getMACPerVLAN?id=' + vlanID + '&portType=' + portType,
dataType: 'json',
success: function ( jsonData ) {
  var vColumns = [];

  columnNumbers = Object.keys(jsonData.columns);
  columnNames = Object.values(jsonData.columns);
  
  for (var i in columnNames) {
	vColumns.push({data: columnNumbers[i], title: columnNames[i]});
	}

  deleteAndCreateTable();
  $('#example').DataTable( {
	  //retrieve: true,
	  destroy: true,
	  columns: vColumns,
	  data: jsonData.data,
	  dom: 'Bfrtipl',
	   "paging": true,
	  "pageLength": 25,
	  "lengthMenu": [ [10, 25, 50, 100, -1], [10, 25, 50, 100, "All"] ],
	  buttons: [ 'copy', 'csv', 'excel', 'pdf', 'print' ],
	  } );
	} } );		  
	
}

//------------------------------------------

function getSwitchInfo(switchID) {
	
// get radio check box all parts / connected ports 
var portType = $("input:radio[name ='SwitchPorts']:checked").val();
	
$.ajax( {
//url: 'http://10.14.2.81:5000/getSwitchInfo?id=' + switchID + '&portType=' + portType,
url: '/getSwitchInfo?id=' + switchID + '&portType=' + portType,
dataType: 'json',
success: function ( jsonData ) {
  var vColumns = [];

  columnNumbers = Object.keys(jsonData.columns);
  columnNames = Object.values(jsonData.columns);
  
  for (var i in columnNames) {
	vColumns.push({data: columnNumbers[i], title: columnNames[i]});
	}

  deleteAndCreateTable();
  $('#example').DataTable( {
	  //retrieve: true,
	  destroy: true,
	  order: [],
	  aaSorting: [],
	  columns: vColumns,
	  data: jsonData.data,
	  dom: 'Bfrtipl',
	   "paging": true,
	  "pageLength": 100,
	  "lengthMenu": [ [10, 25, 50, 100, -1], [10, 25, 50, 100, "All"] ],
	  buttons: [ 'copy', 'csv', 'excel', 'pdf', 'print' ],
	  } );
	} } );		  
	
}


//------------------------------------------


function getSwitchList() {
	
// get switch list 
var portType = $("input:radio[name ='SwitchPorts']:checked").val();
	
$.ajax( {
url: '/getSwitchList',
dataType: 'json',
success: function ( jsonData ) {
  var vColumns = [];

  columnNumbers = Object.keys(jsonData.columns);
  columnNames = Object.values(jsonData.columns);

  for (var i in columnNames) {
    if ( columnNames[i].toUpperCase().indexOf('SSH') > -1) {   // make SSH hyperlink
      vColumns.push({data: columnNumbers[i], title: columnNames[i],
		render: function (data, type, row, meta) {
          data = '<a href=' + data + '>' + data + '</a>';
          return data;
          }
		});
      }
    else {
      vColumns.push({data: columnNumbers[i], title: columnNames[i]});
	  }  
	}

  deleteAndCreateTable();
  $('#example').DataTable( {
	  destroy: true,
	  columns: vColumns,
	  data: jsonData.data,
	  dom: 'Bfrtipl',
	   "paging": true,
	  "pageLength": 25,
	  "lengthMenu": [ [10, 25, 50, 100, -1], [10, 25, 50, 100, "All"] ],
	  buttons: [ 'copy', 'csv', 'excel', 'pdf', 'print' ],
	  } );
	} } );		  
	
}


//------------------------------------------

// show absolute Interface Errors (input / output) as table
function getErrorList() {
	
	// get check (all/trafic) status
	var listType = $("input:radio[name ='errorListCheckBox']:checked").val();
		
	$.ajax( {
	url: '/getInterfaceErrorsList?listType=' + listType,
	dataType: 'json',
    beforeSend: function(){
        $('#spinnerDiv').show();
    },
    complete: function(){
        $('#spinnerDiv').hide();
    },

	success: function ( jsonData ) {
	  var vColumns = [];
	
	  columnNumbers = Object.keys(jsonData.columns);
	  columnNames = Object.values(jsonData.columns);
	
	  for (var i in columnNames) {
		if ( columnNames[i].toUpperCase().indexOf('SSH') > -1) {   // make SSH hyperlink
		  vColumns.push({data: columnNumbers[i], title: columnNames[i],
			render: function (data, type, row, meta) {
			  data = '<a href=' + data + '>' + data + '</a>';
			  return data;
			  }
			});
		  }
		else {
		  vColumns.push({data: columnNumbers[i], title: columnNames[i]});
		  }  
		}
	
	  deleteAndCreateTable();
	  $('#example').DataTable( {
		  destroy: true,
		  columns: vColumns,
		  data: jsonData.data,
		  dom: 'Bfrtipl',
		   "paging": true,
		  "pageLength": 25,
		  "lengthMenu": [ [10, 25, 50, 100, -1], [10, 25, 50, 100, "All"] ],
		  buttons: [ 'copy', 'csv', 'excel', 'pdf', 'print' ],
		  } );
		} } );		  
		
	}
	
//------------------------------------------

// show  Interface Errors that has been incremented during last samples
// (input / output) as table
function getInputErrorIncrementList() {
	
	$.ajax( {
	url: '/getInterfaceInputErrorsIncrementList',
	dataType: 'json',
    beforeSend: function(){
        $('#spinnerDiv').show();
    },
    complete: function(){
        $('#spinnerDiv').hide();
    },
	success: function ( jsonData ) {
		var vColumns = [];
	
		columnNumbers = Object.keys(jsonData.columns);
		columnNames = Object.values(jsonData.columns);
	
		for (var i in columnNames) {
		if ( columnNames[i].toUpperCase().indexOf('SSH') > -1) {   // make SSH hyperlink
			vColumns.push({data: columnNumbers[i], title: columnNames[i],
			render: function (data, type, row, meta) {
				data = '<a href=' + data + '>' + data + '</a>';
				return data;
				}
			});
			}
		else {
			vColumns.push({data: columnNumbers[i], title: columnNames[i]});
			}  
		}
	
		deleteAndCreateTable();
		$('#example').DataTable( {
			destroy: true,
			columns: vColumns,
			data: jsonData.data,
			dom: 'Bfrtipl',
			"paging": true,
			"pageLength": 25,
			"lengthMenu": [ [10, 25, 50, 100, -1], [10, 25, 50, 100, "All"] ],
			buttons: [ 'copy', 'csv', 'excel', 'pdf', 'print' ],
			} );
		} } );		  
		
	}
		
//------------------------------------------		
	
// show  Interface Errors that has been incremented during last samples
// (input / output) as table
function getOutputErrorIncrementList() {
		
	$.ajax( {
	url: '/getInterfaceOutputErrorsIncrementList',
	dataType: 'json',
    beforeSend: function(){
        $('#spinnerDiv').show();
    },
    complete: function(){
        $('#spinnerDiv').hide();
    },
	success: function ( jsonData ) {
		var vColumns = [];
	
		columnNumbers = Object.keys(jsonData.columns);
		columnNames = Object.values(jsonData.columns);
	
		for (var i in columnNames) {
		if ( columnNames[i].toUpperCase().indexOf('SSH') > -1) {   // make SSH hyperlink
			vColumns.push({data: columnNumbers[i], title: columnNames[i],
			render: function (data, type, row, meta) {
				data = '<a href=' + data + '>' + data + '</a>';
				return data;
				}
			});
			}
		else {
			vColumns.push({data: columnNumbers[i], title: columnNames[i]});
			}  
		}
	
		deleteAndCreateTable();
		$('#example').DataTable( {
			destroy: true,
			columns: vColumns,
			data: jsonData.data,
			dom: 'Bfrtipl',
			"paging": true,
			"pageLength": 25,
			"lengthMenu": [ [10, 25, 50, 100, -1], [10, 25, 50, 100, "All"] ],
			buttons: [ 'copy', 'csv', 'excel', 'pdf', 'print' ],
			} );
		} } );		  		
	}		

//------------------------------------------
//------------------------------------------
//------------------------------------------


