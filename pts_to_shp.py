import sys
import os
#make sure gdal bindings ok
try:
    from osgeo import ogr, osr, gdal
    print 'done'
except:
    sys.exit('ERROR: cannot find GDAL/OGR modules')


#data and file name to read 
DATADIR = "C:\pts_to_shp"
# e.g "C:\pts_to_shp"
DATAFILE = "sample.pts"

# DATACRS is your base coordinate system's EPSG code for referance layer
# more on http://spatialreference.org/ref/
# EPSG selected based on reference points 
# from tutorial http://www.exelisvis.com/docs/RegistrationImageToMap.html
DATACRS = 26713

def parse_gcp(datafile):
	with open(datafile) as gcps:
		data = gcps.readlines()
		return data

#unit test for .pts parse
def parse_test():
	datafile = os.path.join(DATADIR,DATAFILE)
	d = parse_gcp(datafile)
	firstline = '; ENVI Image to Map GCP File\n'
	thirdline = '; Map (x,y), Image (x,y)\n'

	#print d[0]
	#print firstline
	#print d[3]
	assert d[0] == firstline
	assert d[3] == thirdline
#parse_test()

def export_geometry(DATADIR,DATAFILE):
	#parse through *.pts file
	points = []
	seperate_points = []
	datafile = os.path.join(DATADIR,DATAFILE)
	d = parse_gcp(datafile)
	points[:] = d[6:]
	for point in points:
		point = point.strip()
		point = point.split()
		seperate_points.append(point)

	# divide coordinate two parts base coordinates and image-to-warp coordinates
	points_right = []
	points_left = []
	for pts in seperate_points:
		points_right.append(pts[:2])
		points_left.append(pts[2:])
	print len(points_right)
	print points_left[0]

	#necessary ogr operations to append coordinates
	point_ogr_left = ogr.Geometry(ogr.wkbMultiPoint)
	point_ogr_right = ogr.Geometry(ogr.wkbMultiPoint)
	temp_point_ogr_left = ogr.Geometry(ogr.wkbPoint)
	temp_point_ogr_right = ogr.Geometry(ogr.wkbPoint)
	for i in range(len(points_right)):
		temp_point_ogr_left.AddPoint(float(points_left[i][0]), float(points_left[i][1]))
		point_ogr_left.AddGeometry(temp_point_ogr_left)
		temp_point_ogr_right.AddPoint(float(points_right[i][0]), float(points_right[i][1]))
		point_ogr_right.AddGeometry(temp_point_ogr_right)
	#append base coordinates and image-to-warp coordinates
	#wkt coordinates if needed
	#wkt_left = point_ogr_left.ExportToWkt()
	#wkt_right = point_ogr_right.ExportToWkt()
	return (point_ogr_left,point_ogr_right)

#set output name and extension
base = 'base'
ref= 'referance'
extension = '.shp'
base_name = base+extension
ref_name =ref+extension

# etc. 'references.shp'
export_geom_left, export_geom_right = export_geometry(DATADIR,DATAFILE)

def write_geometry(export_geom, base_name):
	#set driver for output file
	#etc. 'GeoJSON'
	# more on http://www.gdal.org/ogr_formats.html
	driver_name = 'ESRI Shapefile'

	#check whether output file exists or not
	driver = ogr.GetDriverByName(driver_name)
	#if exist delete and continue
	if os.path.exists(base_name):
	     driver.DeleteDataSource(base_name)

	# new output Driver
	outDriver = ogr.GetDriverByName(driver_name)
	# New Feature and Layer
	outDataSource = outDriver.CreateDataSource(base_name)
	outLayer = outDataSource.CreateLayer(base_name, geom_type=ogr.wkbMultiPoint )

	# Get the output Layer's Feature Definition
	featureDefn = outLayer.GetLayerDefn()

	#from feature def TO new feature
	outFeature = ogr.Feature(featureDefn)

	# Set new geometry
	outFeature.SetGeometry(export_geom)

	# New layer from feature
	outLayer.CreateFeature(outFeature)

	# destroy the feature
	outFeature.Destroy

	# Close DataSources
	outDataSource.Destroy()

	#set .prj file for DATACRS variable 
	source_CRS = osr.SpatialReference()
	source_CRS.ImportFromEPSG(DATACRS)
	source_CRS.MorphToESRI()
	file = open( base_name.strip(extension)+'.prj', 'w')
	file.write(source_CRS.ExportToWkt())
	file.close()
	print 'done !'

write_geometry(export_geom_left,base_name)
write_geometry(export_geom_right,ref_name)

#write_geometry(export_geom_left,export_geom_right)