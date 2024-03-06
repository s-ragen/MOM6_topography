#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from matplotlib.gridspec import GridSpec
from netCDF4 import Dataset

riverfile='river_destination_field'
riverfilenew='river_destination_field_new'

f=open(riverfile,'r')

lines=f.readlines()[2:]
nblocks=int(len(lines)/5)
blocks=[]
for x in range(0,nblocks):
    thisthing=' '.join(lines[5*(x):5*x+5]).replace('\n','')
    blocks.append([int(x) for x in thisthing.split()])

blah=np.array(blocks)

#for line in f:
#    raw[line]=line
#    print(raw[line])

#nprint(blah.shape)
xdest=blah[0:80,:]
ydest=blah[80:,:]

fig=plt.figure(figsize=(12,12))
gs=GridSpec(2,4,height_ratios=[1,1],width_ratios=[15,1,15,1])
f1=plt.subplot(gs[0,0])
#cb=plt.imshow(xdest[45:85,45:],cmap=plt.cm.Set1,origin='lower',interpolation='none')#,range(45,90),cmap=plt.cm.flag)
cb=plt.imshow(xdest,cmap=plt.cm.flag,origin='lower',interpolation='none')#,range(45,90),cmap=plt.cm.flag)
#cb.set_clim(45,85)
plt.title('xdest original')
caxi=plt.subplot(gs[0,1])
plt.colorbar(cb,cax=caxi)
#plt.show()

#fig=plt.figure
f1=plt.subplot(gs[1,0])
#cb=plt.imshow(ydest[45:85,45:],cmap=plt.cm.Set1,origin='lower',interpolation='none')#range(45,90),cmap=plt.cm.flag)
cb=plt.imshow(ydest,cmap=plt.cm.flag,origin='lower',interpolation='none')#range(45,90),cmap=plt.cm.flag)
#cb.set_clim(45,90)
plt.title('ydest original')
caxi=plt.subplot(gs[1,1])
plt.colorbar(cb,cax=caxi)
#plt.show()

#f1=plt.subplot(gs[2,0])
#cb=plt.imshow(ds['q_ca'].values,origin='lower',interpolation='none')
#plt.show()

xdest2=np.zeros((80,96))
xdest2[:,:]=xdest
ydest2=np.zeros((80,96))
ydest2[:,:]=ydest
#print(xdest[:,0])

#print(np.shape(xdest))
for ii in range(96):
    for jj in range(80):

        xdest2[jj,ii]=ii
        ydest2[jj,ii]=jj
        if ydest2[jj,ii]>71:
            ydest2[jj,ii]=71
        if ydest2[jj,ii]<9:
            ydest2[jj,ii]=9
        
#        print(ii,jj)
#        print(xdest[ii,jj],ydest[ii,jj])

#        elif xdest[ii,jj]<72:# and xdest[ii,jj]!=i0i+1:
#            xdest2[ii,jj]=62
#        if ydest[jj,ii]<61 and xdest[jj,ii]<71 and xdest[jj,ii]!=ii+1 and ydest[jj,ii]!=jj+1:
#        if jj<59 and ii<71 and xdest[jj,ii]!=ii+1 and ydest[jj,ii]!=jj+1 and xdest[jj,ii]!=73:
#MIssissippi reroute
#            xdest2[jj,ii]=73
#            ydest2[jj,ii]=53
#        elif ydest[jj,ii]>=61 and xdest[jj,ii]<71 and xdest[jj,ii]!=ii+1 and ydest[jj,ii]!=jj+1:

f1=plt.subplot(gs[0,2])
#cb=plt.imshow(xdest2[45:85,45:],cmap=plt.cm.Set1,origin='lower',interpolation='none')#,range(45,90),cmap=plt.cm.flag)
cb=plt.imshow(xdest2,cmap=plt.cm.flag,origin='lower',interpolation='none')#,range(45,90),cmap=plt.cm.flag)
#cb.set_clim(45,85)
plt.title('xdest new')
caxi=plt.subplot(gs[0,3])
plt.colorbar(cb,cax=caxi)
#plt.show()

#fig=plt.figure
f1=plt.subplot(gs[1,2])
#cb=plt.imshow(ydest2[45:85,45:],cmap=plt.cm.Set1,origin='lower',interpolation='none')#range(45,90),cmap=plt.cm.flag)
cb=plt.imshow(ydest2,cmap=plt.cm.flag,origin='lower',interpolation='none')#range(45,90),cmap=plt.cm.flag)
#cb.set_clim(45,90)
plt.title('ydest new')
caxi=plt.subplot(gs[1,3])
plt.colorbar(cb,cax=caxi)
#

plt.tight_layout()
#plt.show()
plt.savefig('drainage_rerouting_fulldomain_flagvomit.png')
plt.close()

landfile = '/data2/sragen/MOM6_cases/aquaplanet/aqua/run/preprocessing/twopole_topography.nc'
t = xr.open_dataset(landfile)
depth = np.asarray(t['depth'][:])

fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(8,8))
ax1.imshow(ydest2,cmap=plt.cm.flag,origin='lower',interpolation='none')
ax1.set_title('ydest new')

ax2.imshow(depth[:,:96])
ax2.set_title('land')

plt.tight_layout()
plt.savefig('rerouting_vs_topo.png')
plt.close()

alreadydone=1

if alreadydone!=1:

    newfile=Dataset('testing.nc','w',Format='NETCDF4')
    x=range(0,96)
    y=range(0,80)
    data={}
    newfile.createDimension('x', 96)
    data['x'] = newfile.createVariable('x', 'f8',('x',))
    newfile.createDimension('y', 80)
    data['y'] = newfile.createVariable('y', 'f8',('y',))

    newfile.variables['y'][:] = y
    newfile.variables['x'][:] = x

    new_var = newfile.createVariable('xdest', 'int', ('y','x'))
    new_var = newfile.createVariable('ydest', 'int', ('y','x'))
    newfile.variables['xdest'][:] = xdest2
    newfile.variables['ydest'][:] = ydest2

    new_var = newfile.createVariable('xdestb', 'int', ('y','x'))
    new_var = newfile.createVariable('ydestb', 'int', ('y','x'))
    newfile.variables['xdestb'][:] = xdest
    newfile.variables['ydestb'][:] = ydest
    newfile.close()

f.close()
f=open(riverfile,'r')

g=open(riverfilenew,'w')
#print(f.readlines()[0:2])
for ind in range(0,2):
    xx=f.readline()
    print(xx)
    g.write(xx)

a,b=np.shape(xdest2)
for ind in range(0,a):
    for ind2 in range(0,5):
#        g.write(str(xdest2[ind,20*ind2:20*(ind2)+20].item))
        g.write(' ')
        xdest2[ind,20*ind2:20*(ind2)+20].tofile(g,sep=' ',format="%3d")
#        np.savetxt(g,xdest2[ind,20*ind2:20*(ind2)+20],fmt='%4d',delimiter='')
        g.write('\n')
#g.write("\n")
for ind in range(0,a):
    for ind2 in range(0,5):
        g.write(' ')
        ydest2[ind,20*ind2:20*(ind2)+20].tofile(g,sep=' ',format="%3d")
        g.write('\n')    
#np.savetxt(g,xdest2,fmt='%4d')


g.close()
f.close()
