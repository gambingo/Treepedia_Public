
# This function is used to collect the metadata of the GSV panoramas based on the sample point shapefile
# Copyright(C) Xiaojiang Li, Ian Seiferling, Marwa Abdulhai, Senseable City Lab, MIT 

# import urllib
import numpy as np
from urllib.request import urlopen
import xmltodict
# from io import StringIO
# import ogr
# import osr
from osgeo import ogr, osr
import time
import os, os.path
from tqdm import tqdm

from directories import POINT_GRIDS, PANO_DIR, format_folder_name


def GSVpanoMetadataCollector(samplesFeatureClass,num,ouputTextFolder):
    '''
    This function is used to call the Google API url to collect the metadata of
    Google Street View Panoramas. The input of the function is the shpfile of the create sample site, the output
    is the generate panoinfo matrics stored in the text file 
    
    Parameters: 
        samplesFeatureClass: the shapefile of the create sample sites
        num: the number of sites proced every time
        ouputTextFolder: the output folder for the panoinfo
        
    '''
    if not os.path.exists(ouputTextFolder):
        os.makedirs(ouputTextFolder)
    
    driver = ogr.GetDriverByName('ESRI Shapefile')
    
    # change the projection of shapefile to the WGS84
    dataset = driver.Open(samplesFeatureClass)
    layer = dataset.GetLayer()
    
    sourceProj = layer.GetSpatialRef()
    targetProj = osr.SpatialReference()
    targetProj.ImportFromEPSG(4326)
    transform = osr.CoordinateTransformation(sourceProj, targetProj)
    
    # loop all the features in the featureclass
    feature = layer.GetNextFeature()
    featureNum = layer.GetFeatureCount()
    batch = featureNum/num
    batch = int(np.ceil(batch))
    
    for b in range(batch):
        # for each batch process num GSV site
        start = b*num
        end = (b+1)*num
        if end > featureNum:
            end = featureNum
        
        ouputTextFile = 'Pnt_start%s_end%s.txt'%(start,end)
        ouputGSVinfoFile = os.path.join(ouputTextFolder,ouputTextFile)
        
        # skip over those existing txt files
        if os.path.exists(ouputGSVinfoFile):
            continue
        
        time.sleep(1)
        
        with open(ouputGSVinfoFile, 'w') as panoInfoText:
            # process num feature each time
            for i in tqdm(range(start, end)):
                feature = layer.GetFeature(i)        
                geom = feature.GetGeometryRef()
                
                # trasform the current projection of input shapefile to WGS84
                #WGS84 is Earth centered, earth fixed terrestrial ref system
                geom.Transform(transform)
                lon = geom.GetX()
                lat = geom.GetY()
                key = r'' #Input Your Key here 
                
                # get the meta data of panoramas 
                urlAddress = r'http://maps.google.com/cbk?output=xml&ll=%s,%s'%(lat,lon)
                
                time.sleep(0.05)
                # the output result of the meta data is a xml object
                metaDataxml = urlopen(urlAddress)
                metaData = metaDataxml.read()    
                
                data = xmltodict.parse(metaData)
                
                # in case there is not panorama in the site, therefore, continue
                if data['panorama']==None:
                    continue
                else:
                    panoInfo = data['panorama']['data_properties']
                                        
                    # get the meta data of the panorama
                    panoDate = panoInfo.items()[4][1]
                    panoId = panoInfo.items()[5][1]
                    panoLat = panoInfo.items()[8][1]
                    panoLon = panoInfo.items()[9][1]
                    
                    print('The coordinate (%s,%s), panoId is: %s, panoDate is: %s'%(panoLon,panoLat,panoId, panoDate))
                    lineTxt = 'panoID: %s panoDate: %s longitude: %s latitude: %s\n'%(panoId, panoDate, panoLon, panoLat)
                    panoInfoText.write(lineTxt)
                    
        panoInfoText.close()


def metadata_community_area(area_number=1, batch_size=1000):
    inputShp = POINT_GRIDS / format_folder_name(area_number)
    inputShp = str(inputShp)
    outputTxt = PANO_DIR / format_folder_name(area_number)
    GSVpanoMetadataCollector(inputShp, batch_size, outputTxt)


# ------------Main Function -------------------    
if __name__ == "__main__":
    metadata_community_area()
