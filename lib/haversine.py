import math

def great_circle_distance(latitude1, longitude1, latitude2, longitude2):
    """Calculates the great circle distance between two latitude and longitude points

    Arguments:
    latitude1 -- float - the first point's latitude
    longitude1 -- float - the first point's longitude
    latitude2 -- float - the second point's latitude
    longitude2 -- float - the second point's longitude
    """
    RADIUS_OF_EARTH = 6371.0
    return 2*RADIUS_OF_EARTH*math.asin(
        haversine_formula(latitude1, longitude1, latitude2, longitude2)**.5
    )

def haversine_formula(latitude1, longitude1, latitude2, longitude2):
    """Computes the haversine formula for the given latitude and longitude points
    
    Arguments:
    latitude1 -- float - the first point's latitude
    longitude1 -- float - the first point's longitude
    latitude2 -- float - the second point's latitude
    longitude2 -- float - the second point's longitude
    """
    haversine_latitude = haversine_function(latitude1, latitude2)
    haversine_longitude = haversine_function(longitude1, longitude2)
    return haversine_latitude + math.cos(latitude1)*math.cos(latitude2)*haversine_longitude

def haversine_function(theta1, theta2):
    """Computes the haversine function for the given point.

    Arguments:
    theta1 -- float - the coordinate of the first point
    theta2 -- float - the coordinate of the second point
    """
    delta_theta = theta2 - theta1
    return math.sin(delta_theta/2.0)**2

def miles(kilometers):
    """Converts kilometers to miles

    Arguments:
    kilometers -- float - the number in kilometers
    """
    MILES_PER_KILOMETER = 0.621371
    return kilometers*MILES_PER_KILOMETER
