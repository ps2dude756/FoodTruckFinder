function getUrlParameters()
{
  var params = {};
  window.location.search.substr(1).split("&").forEach(
    function (item) {
      var keyvar = item.split("=");
      if (keyvar[0]) {
        params[keyvar[0]] = parseFloat(keyvar[1]);
      }
    }
  );
  return params;
}

function httpRequest(url, method, payload)
{
  var request = new XMLHttpRequest();
  request.open(method, url, false);
  request.send(payload);
  return request.responseText;
}

function create_url(params)
{
  return location.protocol + '//' + location.host + 
    '/api/foodtrucks?latitude=' + params['latitude'] + 
    '&longitude=' + params['longitude'] + 
    '&distance=' + params['distance'];
}

function create_table(foodtrucks)
{
  var table = document.createElement('table');
  
  for (index in foodtrucks) {
    var tr = table.insertRow();
    tr.insertCell().appendChild(
      document.createTextNode(
        foodtrucks[index]['name']
      )
    );
    tr.insertCell().appendChild(
      document.createTextNode(
        foodtrucks[index]['address']
      )
    );
    tr.insertCell().appendChild(
      document.createTextNode(
        foodtrucks[index]['fooditems'].replace(/:/g, ",")
      )
    );
  }
  return table;
}
