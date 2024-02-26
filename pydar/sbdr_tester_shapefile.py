import astropy
import math
import spherical_geometry


lat1 = 10;
lon1 = 13;
az1 = 12;
lat2 = 0;
lon2 = 20;
az2 = -23;

A = spherical_geometry.great_circle_arc(lat1,lon1,az1,lat2,lon2,az2).intersection
print(A)
