# Charting elevations of every major US Highway
# Using Google Maps APIs

import googlemaps
import json
#from pymongo import MongoClient
#import pandas as pd
#import pprint
#import urllib
#import simplejson
#import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from ggplot import *
from pykml import parser
import urllib2
import xmltodict

#sns.set(style = '')

mykey = 'AIzaSyD4ipXow67rS9YM9eljgCiVJkL0yyIg7nQ'
gmaps = googlemaps.Client(key=mykey)

# Testing that APIs are current:
#geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
# print(geocode_result)

elevlist=[]
dfelev=[]

def Routing(highway):
    # Wikipedia hosts a KML file for each major highway. Here is the URL I-40's:
    url = 'https://en.wikipedia.org/w/index.php?title=Template%3AAttached_KML%2FInterstate_40&action=raw'
    fileobject = urllib2.urlopen(url)
    # Parse this KML/XML, so that it can be treated like a JSON
    doc = xmltodict.parse(fileobject)

    rawcoords = doc['kml']['Document']['Placemark']['LineString']['coordinates']
    # Coordinates are basically a single enormous string. Need to split by spaces (waypoints), and commas (lat/lon)
    listcoords = rawcoords.split(' ')
    newcoords = []
    for pair in listcoords:
        pair = pair.split(',')
        pair = [float(pair[1]), float(pair[0])]     # Flip lat/lon presentation
        newcoords.extend(pair)
    coords = zip(newcoords[::2],newcoords[1::2])    # Pairs of records are zipped together to form tuples
    # len(coords) -> 7645 coordinates, might be too much for the API to handle at once? Getting an HTTP error: 413
    # Error message says max waypoints: 23.   7625/23 = 332.391304348
    # Get directions, based on the KML's waypoints (no other way to get polyline)
    I40_path = gmaps.directions(coords[0], coords[-1],
                                waypoints=coords[::350])
    # with open('I40_path.json', 'w') as fp: json.dump(I40_path, fp)
    # Parse out the polyline from the directions
    for rec in I40_path:
        poly40 = rec['overview_polyline']['points']
    # Encode as unicode, to avoid issues with backslashes in the polyline
    poly40 = poly40.encode('utf8')

    return poly40

# Plug this polyline into the Elevations API


def Elevations(poly40):
    # 500 seems to be the max. number of samples allowed? Not really sure about the error message, honestly
    I40_elev = gmaps.elevation_along_path(poly40, samples=500)

    # with open('I40_elev.json', 'w') as fp: json.dump(I40_elev, fp)

    # Create a dictionary. Key = longitude. Value = elevation.
    elevlist = {}
    for spt in I40_elev:
        elevlist[spt['location']['lng']] = spt['elevation']

    # Convert dictionary into a dataframe
    dfelev = pd.DataFrame.from_dict(elevlist, orient='index')
    dfelev.columns = ['elevation']
    dfelev.index.names = ['longitude']
    dfelev.reset_index(inplace=True)

    return dfelev

def Plotting(dfelev):
    #plotter = plt.scatter(x = dfelev['longitude'], y = dfelev['elevation'])
    #plt.savefig('I40plot.png')
    p = ggplot(dfelev, aes('longitude', 'elevation')) + geom_line() + xlab('Longitude') + ylab('Elevation') + ggtitle('Interstate 40') + theme_bw()
    ggplot.save(p, filename = 'I40plot.png')

def main():
    highway = 'I40'
    poly40 = Routing(highway)
    dfelev = Elevations(poly40)
    Plotting(dfelev)

main()
