Foodtruck Lookup
================
<table>
  <tr><td>Method</td><td>Endpoint</td></tr>
  <tr><td>GET</td><td>/api/foodtrucks</td></tr>
</table>

This endpoint will lookup the foodtrucks within a given radius of a given 
initial point. A request to this endpoint should have the parameters below.

<table>
  <tr><td>Parameter</td><td>Type</td><td>Description</td></tr>
  <tr><td>latitude</td><td>Float</td><td>The latitude of the initial point.</td></tr>
  <tr><td>longitude</td><td>Float</td><td>The longitude of the initial point.</td></tr>
  <tr><td>distance</td><td>Float</td><td>The distance from the initial point to search from.</td></tr>
</table>

The response from this endpoint is a list of foodtrucks. Foodtrucks have the 
parameters below.

<table>
  <tr><td>Parameter</td><td>Type</td><td>Description</td></tr>
  <tr><td>name</td><td>String</td><td>The name of the foodtruck.</td></tr>
  <tr><td>address</td><td>String</td><td>The address of the foodtruck.</td></tr>
  <tr><td>fooditems</td><td>String</td><td>A list of items sold at the foodtruck.
    The items are ': '-separated.</td></tr>
</table>
