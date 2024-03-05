This directory contains a script that generates custom topography for MOM6. This was developed to do aquaplanet-like simulations for my dissertation.

Within this directory are the following files:
  - Python script that specifies topography. Alter this file to change ocean basin geometry: make_ocean_atmos_grids.py 
  - Shell script to run to create the new topography file: 'generate_grids.sh'  
  - Netcdf files with grid specifications for the oceanThis directory contains a script that generates custom topography for MOM6.
  - File that contains the topography that you generate with the make_ocean_atmos_grids.py and the generate_grids.sh files: twopole_topography.nc
  - Jupyter notebook file that can be run to look at the topography that you created: view_grids.ipynb 

To create custom topography in MOM6, follow the work flow outlined here:

Modify the make_ocean_atmos_grids.py file to designate depth of ocean and land as well as where to create land. The sample file included here is pretty simplistic - it creates an ocean of uniform depth and generates simple, narrow ridges which act as barriers designating the geometry of idealized ocean basins. It has a telescoping resolution at the equator that steps the horizontal resolution from a nominal 2 degrees to about 1/3 degree in the tropics. It also creates two polar land caps to preserve numerical stability at the poles. 

The generate_grids.sh file creates grids for the ocean and the atmosphere as well as mosaic files for the model components. It requires the MIDAS Python package (https://github.com/mjharriso/MIDAS). Modify the generate_grids.sh to include the path to MIDAS on your machine. Then run the script from the command line. Running this script will generate new netcdf files.

Copy all the newly created netcdf files into the INPUT/ directory within your MOM6 run directory. If you'd like, take a look at the topography file you generated (twopole_topography.nc) using the view_grids.ipynb notebook. 

Before running MOM6, you will need to update runtime parameters in the MOM6 input parameters. Ensure that the MOM_input file in your run directory contains the following parameters:
TOPO_CONFIG = "file"
TOPO_FILE = "twopole_topography.nc" 

And then you should be good to go! You can now run your custom continental geometry in MOM6, either in ocean-only or coupled simulations!
