import pyproj


boston_lat = 42.+(15./60.); boston_lon = -71.-(7./60.)
london_lat = 51.+(32./60.); london_lon = -(5./60.)

earth_rad = 6378206.4
geodesic = pyproj.Geod(a = earth_rad,es=0) # eccentricity = 0 because it's a sphere

fwd_azimuth,back_azimuth,distance = geodesic.inv(boston_lon, boston_lat, london_lon, london_lat)

#print("bck azimuth: {0}\n".format(back_azimuth))
#print(distance/1000)
# I want the forward azimuth because that is what the matlavb function is calculating

# for titan

# to replicate gc_az1 = azimuth( [pt1x,pt1y],[pt2x,pt2y],titan_def ):
r_titan = 2575000 #radius in meters
e_titan = 0 # titan simplified to a sphere (no eccentricity)
geodesic = pyproj.Geod(a = earth_rad,es=0)# define Titan ellipsoid
fwd_azimuth,back_azimuth,distance = geodesic.inv(boston_lon, boston_lat, london_lon, london_lat)
gc_az1 = fwd_azimuth # considering azimuth from starting lat,lon pair like in the matlab function 

print("gc_az1: {0}\n".format(gc_az1))
