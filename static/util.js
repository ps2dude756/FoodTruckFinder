/**
 * Dependencies:
 * Google Maps: https://maps.googleapis.com/maps/api/js
 */

/**
 * obtains GET parameters
 * @return
 *    The GET parameters in a dictionary
 */
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

/**
 * creates and sends a synchronous http request
 * @param url
 *    the url to send the request to
 * @method
 *    the http method to use
 * @payload
 *    any data that should be sent in a POST request. Should be set to null for a GET
 * @return
 *    the response of the request
 */

function httpRequest(url, method, payload)
{
  var request = new XMLHttpRequest();
  request.open(method, url, false);
  request.send(payload);
  return request.responseText;
}

/**
 * forms a url with GET parameters
 * @param base_url
 *    the url to add parameters to
 * @params
 *    a dictionary of parameters to add
 * @return
 *    the formatted url
 */
function create_url(base_url, params)
{
  param_list = [];
  for (index in params) {
    param_list.push(index + '=' + params[index]);
  }
  return base_url + '?' + param_list.join('&');
}

/**
 * Checks if a parameter is a number
 * @param
 *    The parameter to check
 * @return
 *    true if param is a number, false otherwise.
 */
function param_is_valid(param)
{
  return typeof param == 'number' && param != undefined && !isNaN(param);
}

/**
 * Creates an HTML table for the passed in foodtrucks
 * @param foodtrucks
 *    an array of dictionaries, with each dictionary containing information for a 
 *    foodtruck. A foodtruck should have the following parameters: Name, Address, 
 *    MenuItems.
 * @return
 *    the created HTML table
 */   
function create_table(foodtrucks)
{
  var table = document.createElement('table');
  var border = document.createAttribute('border');
  border.value = "1";
  table.setAttributeNode(border);
  var th = table.createTHead();
  var tr = th.insertRow();
  tr.insertCell().appendChild(document.createTextNode('Name'));
  tr.insertCell().appendChild(document.createTextNode('Address'));
  tr.insertCell().appendChild(document.createTextNode('Menu items'));
 
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

/** Requires Google maps
 * Obtains the latitude and longitude of the passed in address, adds them
 * to the passed in form, and then submits the form.
 * @param client_address
 *     A string containing the address to lookup
 * @param form
 *    The form to add the latitude and longitude to
 */
function add_latlng_to_form(client_address, form)
{
  var geocoder = new google.maps.Geocoder();
  geocoder.geocode(
    {address: client_address},
    function (results, status) {
      if (results.length) {
        var latitude = results[0].geometry.location.k;
        var longitude = results[0].geometry.location.B;
        form.latitude.value = latitude;
        form.longitude.value = longitude;
        form.address.remove();
        form.submit();
      }
    }
  );
}
