# Pts to Shp

Bunch of code enables you to convert your ENVI .pts tie points file to ESRI shapefile format 

### Version
0.0.1

### Dependencies

GDAL/OGR python bindings 
GDAL 1.11.2 release

###Data
- DATACRS is your base coordinate system's EPSG code for referance layer
more is available on http://spatialreference.org/ref/
- EPSG selected based on reference points from tutorial http://www.exelisvis.com/docs/RegistrationImageToMap.html

### Usage
Path of gcp file to use in image-to-map registration
```sh
DATADIR = "C:\pts_to_shp"
DATAFILE = "sample.pts"
DATACRS = 26713
```
Export geometry and save 
```sh
export_geometry(DATADIR,DATAFILE)
write_geometry(export_geom, base_name)
```

License
----

MIT




