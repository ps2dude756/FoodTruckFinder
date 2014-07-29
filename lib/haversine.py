import math

RADIUS_OF_EARTH = 6371.0
MILES_PER_KILOMETER = 0.621371

def great_circle_distance(latitude1, longitude1, latitude2, longitude2):
    return 2*RADIUS_OF_EARTH*math.asin(
        haversine_formula(latitude1, longitude1, latitude2, longitude2)**.5
    )

def haversine_formula(latitude1, longitude1, latitude2, longitude2):
    haversine_latitude = haversine_function(latitude1, latitude2)
    haversine_longitude = haversine_function(longitude1, longitude2)
    return haversine_latitude + math.cos(latitude1)*math.cos(latitude2)*haversine_longitude

def haversine_function(theta1, theta2):
    delta_theta = theta2 - theta1
    return math.sin(delta_theta/2.0)**2

def miles(kilometers):
    return kilometers*MILES_PER_KILOMETER
