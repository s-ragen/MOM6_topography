## Make ocean and atmospheric supergrids. Needs numpy, midas, and netCDF4

import midas
import netCDF4 as nc
import numpy as np
import set_fv_geom

## Ocean Grid
# Define the parameters of a cartesian grid
xrefine = 1
yrefine = 1
lat0 = -89 # 
lon0 = 0   # Start the grid at the prime meridian
lenlat = 178 #total latitude range (-90 to 90)
lenlon = 360 #total longitude range (0 to 360)
# Define parameters related to topography
ocean_depth = 4000. # Depth of ocean points in meters
land_depth = -0.    # "depth" of the land points
cap_extent = 70 # How far equatorward the land at poles extends

# Number of points in the super grid (twice as much as actual model grid)
# 'round' used here in case of roundoff error
#nx_super = round(360*xrefine) # Nominally 2-degree zonal resolution
#ny_super = round(180*yrefine) # Nominally 2-degree meridional resolution

ny_super = int(round(lenlat*yrefine))
nx_super = int(round(lenlon*xrefine)) # Nominally 2-degree zonal resolution

# Make a equally spaced lat-lon grid
ogrid = midas.rectgrid.supergrid(nx_super,ny_super,'spherical','degrees',lat0,lenlat,lon0,lenlon,cyclic_x=True)
ogrid.grid_metrics()

# Increase meridional resolution near equator
y = ogrid.y[:,0]
LAMBDA = ogrid.x[0,:]

dy = y[1:] - y[0:-1]
jind = np.where(y>-11.)[0][0]
jind = jind+np.mod(jind,2)
y = y[0:jind]
dy = dy[0:jind]

y2 = np.array([-10.0,-9.25,-8.5,-8.0,-7.5,-7.0,-6.5,-6.25,-6.0,-5.75,-5.5,-5.25])
y2_r = -y2[::-1]

y_s = -5.0
y_e = 0
y3 = np.linspace(y_s,y_e,num=33)
y3_r = -y3[::-1]
y3 = np.concatenate((y3,y3_r[1:]))
dy3 = y3[1:]-y3[0:-1]

PHI = np.concatenate((y,y2,y3,y2_r,-y[::-1]))

x,y = np.meshgrid(LAMBDA,PHI)
DPHI=PHI[1:]-PHI[0:-1]

# Create supergrid
ocean_grid = midas.rectgrid.supergrid(xdat=x,ydat=y,axis_units='degrees',cyclic_x=True)
ocean_grid.grid_metrics()
ocean_grid.write_nc('ocean_supergrid.nc')

# Make a tile variable and a string dimension...needed to generate exchange grids
fout=nc.Dataset('ocean_supergrid.nc','r+',format='NETCDF3_CLASSIC')
string=fout.createDimension('string',255)
tile=fout.createVariable('tile','S1',('string'))
tile[0:5]=nc.stringtochar(np.array(['tile1'],'S5'))
fout.sync()
fout.close()

# Generate topography based on a two pole planet
# Generate the T, U, V grid from the supergrid
grid = midas.rectgrid.quadmesh(supergrid = ocean_grid, is_latlon = True, cyclic = True)
ny_grid, nx_grid = grid.x_T.shape
# Initialize topography to land to start, shape based on size of a T-grid
topo = np.zeros(grid.x_T.shape) + land_depth
# Set ocean depth for all points equatorward of the cap_extent
topo[ np.abs(grid.y_T) <= cap_extent ] = ocean_depth
# Create two ridges
topo[(grid.x_T >= 1) & (grid.x_T < 5) & ((grid.y_T) > -50)] = land_depth
topo[(grid.x_T >= 113) & (grid.x_T < 117) & ((grid.y_T) > -50)] = land_depth
# Make a sill at latitude of NPAC DoubleDrake's northern Pacific boundary 
topo[(grid.x_T >= 116) & (grid.x_T < 361) & ((grid.y_T) > 61) & ((grid.y_T) < 63)] = land_depth + 3125
topo[(grid.x_T >= 116) & (grid.x_T < 361) & ((grid.y_T) > 59) & ((grid.y_T) < 61)] = land_depth + 2250
topo[(grid.x_T >= 116) & (grid.x_T < 361) & ((grid.y_T) > 57) & ((grid.y_T) < 59)] = land_depth + 1375
topo[(grid.x_T >= 116) & (grid.x_T < 361) & ((grid.y_T) > 55) & ((grid.y_T) < 57)] = land_depth + 500
topo[(grid.x_T >= 116) & (grid.x_T < 361) & ((grid.y_T) > 53) & ((grid.y_T) < 55)] = land_depth + 1375
topo[(grid.x_T >= 116) & (grid.x_T < 361) & ((grid.y_T) > 51) & ((grid.y_T) < 53)] = land_depth + 2250
topo[(grid.x_T >= 116) & (grid.x_T < 361) & ((grid.y_T) > 49) & ((grid.y_T) < 51)] = land_depth + 3125

# Write out the two-pole topography
fout = nc.Dataset('twopole_topography.nc', 'w', format='NETCDF3_CLASSIC')
# Set x,y dimensions
yax = fout.createDimension('ny',ny_grid)
xax = fout.createDimension('nx',nx_grid)
# Create the 'ntiles' dimension needed for mosaic generation
fout.createDimension('ntiles',1)
# Create variables storing mean and variance of topography
meantopo = fout.createVariable('depth','f8',('ny','nx'))
meantopo.units = 'meters'
meantopo.standard_name = 'topographic depth at T-cell centers'
meantopo[:] = topo
stdtopo = fout.createVariable('std','f8',('ny','nx'))
stdtopo.units = 'meters'
stdtopo.standard_name = 'subgrid variance of topography at T-cell centers'
stdtopo[:] = topo * 0. # No variance of topography within a cell
fout.sync()
fout.close()

## Atmospheric Grid
# Define the parameters.
xrefine = 0.8 # 2.5-degree resolution
yrefine = 1 # 2-degree resolution
lat0 = -90 # Start at the south pole
lon0 = 0   # Start the grid at the prime meridian
lenlat = 180 #total latitude range (-90 to 90)
lenlon = 360 #total longitude range (0 to 360)
lenlat = 180 #total latitude range (-90 to 90)
lenlon = 360 #total longitude range (0 to 360)
# Define parameters related to topography

# Number of points in the super grid (twice as much as actual model grid)
# 'round' used here in case of roundoff error
nx_super = round(360*xrefine*0.5)
ny_super = round(180*yrefine*0.5)

# Make a equally spaced lat-lon grid
atmos_grid = midas.rectgrid.supergrid(nx_super*2,ny_super*2,'spherical','degrees',lat0,lenlat,lon0,lenlon,cyclic_x=True)
atmos_grid.grid_metrics()
# Overwrite the metrics with those from set_fv_geoms
print(atmos_grid.area.shape)
y, x = set_fv_geom.set_fv_geom(int(ny_super), int(nx_super))
print( x.shape, y.shape)
atmos_grid.x[:,:] = x
atmos_grid.y[:,:] = y
atmos_grid.angle_dx[:,:] = 0.
atmos_grid.write_nc('atmos_supergrid.nc')

# Make a tile variable and a string dimension...needed to generate exchange grids
fout=nc.Dataset('atmos_supergrid.nc','r+',format='NETCDF3_CLASSIC')
string=fout.createDimension('string',255)
tile=fout.createVariable('tile','S1',('string'))
tile[0:5]=nc.stringtochar(np.array(['tile1'],'S5'))
fout.sync()
fout.close()
