#! /usr/bin/python
'''Create an XML file of occurrences from a TSV file

The output XML is structured to generate a formatted document in (e.g.) HTML (e.g. via XSL) or PDF (e.g. via ConTeXt).
'''

import sys
import csv
import re
from xml.etree import ElementTree as et
from xml.dom import minidom as md
import utm
from pybibtex import build_citekey_dict
from pybibtex import parse_bibfile_to_cite_dict

# return error if the wrong number of arguments are given
# usage is given in the error return value
try:
    script_file = sys.argv[0]
    taxon_file, synonymy_file, clade_name = sys.argv[1:]
except ValueError:
    print('Usage: {} taxon_file synonymy_file clade_name'.format(script_file))


def find_replace_multi(string, dictionary):
    '''Replace multiple patterns within string.
    '''

    for item in dictionary.keys():
        string = re.sub(item, dictionary[item], string)
    return string


def get_ref_dates(filename):
    '''Return the dates from a set of references given a reference key and Bib(La)TeX file.
    '''

    with open(filename, newline='') as f:
        syn = csv.DictReader(f, delimiter='\t')
        bibfile = parse_bibfile_to_cite_dict(bib_path='synonymy.bib')
    
        for row in syn:
            refkey = '\\cite{' + row['reference'] + '}'
            citekey_dict = build_citekey_dict(refkey.split('\n'))
            for citekey in citekey_dict:
                refdate = bibfile[citekey]['date']
            yield dict(date=refdate, **row)


def get_higher_taxon(filename):
    '''Return records for a specified clade name given as an input argument.
    '''

    with open(filename, newline='') as f:
        tax = csv.DictReader(f, delimiter='\t')

        for row in tax:
            if row['clade'] == clade_name:
                yield dict(**row)



def element_lsid(lsid, base_url = 'https://zoobank.org/'):
    '''Return an XMl element to hold an LSID value with attribute link url.
    '''

    lsid_elem = et.Element('lsid')
    lsid_elem.text = lsid

    lsid_url = base_url + lsid
    lsid_elem.set('url', lsid_url)

    return(lsid_elem)


def utm_to_latlon(utm_coord):
    '''Convert UTM-formatted coordinate strings to WGS84-formatted (latitutde-longitude).
    '''

    utm_parser = re.compile(r'(?P<column>\d+)(?P<row>[A-Z]) (?P<easting>\d+) (?P<northing>\d+)')
    parsed_utm = utm_parser.match(utm_coord).groupdict()

    converted_latlon = utm.to_latlon(int(parsed_utm['easting']),
                                     int(parsed_utm['northing']),
                                     int(parsed_utm['column']),
                                     parsed_utm['row'])

    return(converted_latlon)


def element_coordinates(latlon, utm):
    '''Return an XML element holding WGS84 and/or UTM coordinates for a given location, with a URL to that location on OpenStreetMap.
    '''

    if utm and not latlon:
        latlon = utm_to_latlon(utm)

    lat = str(round(latlon[0], 7))
    lon = str(round(latlon[1], 7))

    osm_url_str = f'https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=6/{lat}/{lon}'

    # First generate the holding coordinates element, which also hold the OpenStreetMap URL at the top level.
    coord_elem = et.Element('coordinates')
    coord_elem.set('osm-url', osm_url_str)

    coord_wgs_elem = et.SubElement(coord_elem, 'wgs')
    coord_wgs_elem.set('latitude', lat)
    coord_wgs_elem.set('longitude', lon)

    # Format the coordinates to print prettily.
    if latlon[0] > 0:
        lat = lat + '° N'
    else:
        lat = lat + '° S'

    if latlon[1] > 0:
        lon = lon + '° E'
    else:
        lon = lon + '° W'

    coord_wgs_elem.text = lat + ' ' + lon
    
    # Also return the UTM coordinates if present, but these don't contribute to the coordinates (except to generate latitude and longitude values).
    if utm:
        coord_utm_elem = et.SubElement(coord_elem, 'utm')
        coord_utm_elem.text = 'UTM WGS84 ' + utm

    return(coord_elem)


synonymy_dict = get_ref_dates(synonymy_file)
sorted_synonymy = sorted(synonymy_dict, key=lambda row: row['date'])

taxa_to_print = get_higher_taxon(taxon_file)

text_sanitising = {r'\.\.': r'.', r'\s\s': r' '}

unit_separator = ', '
lithostrat_keys = ['bed', 'member', 'formation', 'zone']
chronostrat_keys = ['stage', 'series', 'system']
coord_keys = ['utm_wgs84', 'long', 'lat']

outfile = clade_name.lower() + '.xml'

root = et.Element('synonymy')

# Build XML file
for taxon in taxa_to_print:
    current_taxon = taxon['accepted_name']
    # this_taxon = find_replace_multi(taxon_name, taxon)

    taxon_elem = et.SubElement(root, 'taxon')
    
    name_elem = et.SubElement(taxon_elem, 'name')
    name_elem.text = current_taxon

    if taxon['accepted_status'] == 'ncomb':
        name_elem.set('combination', 'new')
    else:
        name_elem.set('combination', 'original')
    
    if taxon['lsid_act']:
        lsid_act_elem = element_lsid(lsid = taxon['lsid_act'])

        taxon_elem.append(lsid_act_elem)

    


# tree = et.ElementTree(root)

# Format the XML content to make it easier to view
xml_str = md.parseString(et.tostring(root)).toprettyxml(indent="\t")

with open(outfile, 'w') as f:
    # tree.write(f)
    f.write(xml_str)