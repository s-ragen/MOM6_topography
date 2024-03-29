#!/bin/bash

# Load the MIDAS python package used to generate the supergrids on the land and ocean
FREPATH=/ptardat2/ashao/local/gaggle/FRE-NCtools/build.fre-nctools.gnu-gaggle.bronx12.nS9sx/bronx12/gnu-gaggle/bin
# modify the path above to point to where MIDAS is on your computer

source activate MIDAS
#rm *.nc

python make_ocean_atmos_grids.py 

# Now that the grids have been generated, the mosaics can be made
# 1) Each component needs to first have a 'solo' mosaic generated that describes the contact points
# 2) Once the solo mosaics have been generated, the mosaics describing land, ice, ocean, and atmosphere can be generated

$FREPATH/make_solo_mosaic --num_tiles 1 --dir ./ --mosaic_name atmos_mosaic --tile_file atmos_supergrid.nc --periodx 360.
$FREPATH/make_solo_mosaic --num_tiles 1 --dir ./ --mosaic_name ocean_mosaic --tile_file ocean_supergrid.nc --periodx 360.

# For the full coupled model
$FREPATH/make_coupler_mosaic --verbose  --atmos_mosaic atmos_mosaic.nc --ocean_mosaic ocean_mosaic.nc  --ocean_topog twopole_topography.nc --mosaic_name grid_spec

# For the ice_ocean_SIS2 model
#$FREPATH/make_quick_mosaic --input_mosaic ocean_mosaic.nc --mosaic_name grid_spec --ocean_topog twopole_topography.nc

# All input grids and mosaics are now generated, copy them over to the INPUT directory
#mkdir ../INPUT/

#cp *.nc ../INPUT/
