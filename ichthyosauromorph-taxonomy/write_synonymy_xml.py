#! /usr/bin/python
'''Create an XML file of occurrences from a TSV file

The output XML is structured to generate a formatted document in (e.g.) HTML (e.g. via XSL) or PDF (e.g. via ConTeXt).
'''

import sys
import csv
import re
from xml.etree import ElementTree as et
from xml.dom import minidom
import utm
from pybibtex import build_citekey_dict
from pybibtex import parse_bibfile_to_cite_dict
import pandoc
# import html

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
            # if row['clade'] == clade_name:
            yield dict(**row)



def element_lsid(lsid, base_url = 'https://zoobank.org/'):
    '''Return an XMl element to hold an LSID value with attribute link url.
    '''

    lsid_elem = et.Element('lsid')
    lsid_elem.text = lsid

    lsid_url = base_url + lsid
    lsid_elem.set('url', lsid_url)

    if re.search('act', lsid):
        lsid_elem.set('lsid-type', 'act')
    elif re.search('pub', lsid):
        lsid_elem.set('lsid-type', 'publication')

    return(lsid_elem)


def parse_utm(utm_coord):
    '''Parse a UTM string into its constituent parts held in a dictionary.
    '''

    utm_parser = re.compile(r'(?P<zone>\d+)(?P<band>[A-Z]) (?P<easting>\d+) (?P<northing>\d+)')
    parsed_utm = utm_parser.match(utm_coord).groupdict()

    return(parsed_utm)


def utm_to_latlon(parsed_utm):
    '''Convert parsed UTM-formatted coordinate dictionary to WGS84-formatted (latitutde-longitude).
    '''

    converted_latlon = utm.to_latlon(int(parsed_utm['easting']),
                                     int(parsed_utm['northing']),
                                     int(parsed_utm['zone']),
                                     parsed_utm['band'])

    return(converted_latlon)


def element_utm(utm_coord):
    '''Return an XML element holding UTM coordinates for a given location.
    '''

    parsed_utm = parse_utm(utm_coord)
    converted_latlon = utm_to_latlon(parsed_utm)

    coord_utm_elem = et.Element('utm')

    zone_elem = et.SubElement(coord_utm_elem, 'zone')
    zone_elem.text = parsed_utm['zone']
    
    band_elem = et.SubElement(coord_utm_elem, 'band')
    band_elem.text = parsed_utm['band']

    easting_elem = et.SubElement(coord_utm_elem, 'easting')
    easting_elem.text = parsed_utm['easting']

    northing_elem = et.SubElement(coord_utm_elem, 'northing')
    northing_elem.text = parsed_utm['northing']

    return([converted_latlon, coord_utm_elem])


def parse_latlon(latlon):
    '''Parse a latitude or longitude coordinates and convert to decimal. Normalizes values with minutes (and seconds).

    NB this isn't used.
    '''

    if re.search(r'[\u2033\"\']+', latlon):
        coord_parser = re.compile(r'(?P<degree>-?\d+\.?\d+)°?\s+(?P<minute>\d+)[′\']?\s+(?P<second>\d+\.?\d+)[″\'\"]?\s+(?P<direction>[NESW]?)', re.UNICODE)
    elif re.search(r'[\u2032\']+', latlon):
        coord_parser = re.compile(r'(?P<degree>-?\d+\.?\d+)°?\s+(?P<minute>\d+\.?\d+)[′\']?\s+(?P<direction>[NESW]?)', re.UNICODE)
    else:
        coord_parser = re.compile(r'(?P<degree>-?\d+\.?\d+)°?\s?(?P<direction>[NESW]?)', re.UNICODE)

    parsed_latlon = coord_parser.match(latlon).groupdict()

    print(parsed_latlon)


def element_coordinates(lat, lon):
    '''Return an XML element holding WGS84 and/or UTM coordinates for a given location, with a URL to that location on OpenStreetMap.
    '''

    lat = str(round(float(lat), 7))
    lon = str(round(float(lon), 7))

    osm_url_str = f'https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=6/{lat}/{lon}'

    # First generate the holding coordinates element, which also hold the OpenStreetMap URL at the top level.
    coord_elem = et.Element('coordinates')
    coord_elem.set('osm-url', osm_url_str)

    coord_lat_elem = et.SubElement(coord_elem, 'latitude')
    coord_lat_elem.text = lat
    coord_lon_elem = et.SubElement(coord_elem, 'longitude')
    coord_lon_elem.text = lon
    
    return(coord_elem)


def parse_pandoc(str):
    '''Parse a string of Pandoc markdown input and return formatted XML. Includes rendering citations.
    '''
    comment = pandoc.read(str)
    comment = pandoc.write(comment, format='jats', options=['-C', '--bibliography=synonymy.bib', '--wrap=none'])
    parsed_comment = et.fromstring(comment)

    return(parsed_comment)


synonymy_dict = get_ref_dates(synonymy_file)
sorted_synonymy = sorted(synonymy_dict, key=lambda row: row['date'])

taxa_to_print = get_higher_taxon(taxon_file)

text_sanitising = {r'\.\.': r'.', r'\s\s': r' '}

unit_separator = ', '
lithostrat_keys = ('bed', 'member', 'formation')
chronostrat_keys = ('stage', 'series', 'system')
biostrat_keys = ('zone', 'subzone')


outfile = clade_name.lower() + '.xml'

root = et.Element('synonymy')

# Build XML file
for taxon in taxa_to_print:
    current_taxon = taxon['accepted_name']
    # this_taxon = find_replace_multi(taxon_name, taxon)

    taxon_elem = et.SubElement(root, 'taxon')
    taxon_elem.set('clade', taxon['clade'])
    
    name_elem = et.SubElement(taxon_elem, 'taxon-name')
    name_elem.text = current_taxon

    if taxon['accepted_status'] == 'ncomb':
        name_elem.set('combination', 'new')
    else:
        name_elem.set('combination', 'original')
    
    if taxon['lsid_act']:
        lsid_act_elem = element_lsid(lsid = taxon['lsid_act'])

        taxon_elem.append(lsid_act_elem)

    filter_synonyms = [x for x in sorted_synonymy if x['accepted_name'] == current_taxon]
    # filter_synonyms = [e for e in ({k: v for k, v in sub.items() if v} for sub in filter_synonyms) if e]

    if filter_synonyms:
        synonym_list_elem = et.SubElement(taxon_elem, 'synonym-list')

    # indent this a level?
    for synonym in filter_synonyms:
        current_synonym = synonym['identified_name']
        print('Record matched:', current_synonym, '→', current_taxon)

        synonym_elem = et.SubElement(synonym_list_elem, 'synonym')

        if synonym['morphological_information']:
            synonym_elem.set('morphology', synonym['morphological_information'])
        
        if synonym['assignment_confidence']:
            synonym_elem.set('confidence', synonym['assignment_confidence'])

        synonym_name_elem = et.SubElement(synonym_elem, 'identified-name')
        if re.search(r'\*', synonym['identified_name']):
            synonym_name = parse_pandoc(synonym['identified_name'])
        else:
            synonym_name = et.Element('italic')
            synonym_name.text = synonym['identified_name']

        synonym_name_elem.append(synonym_name)

        if synonym['identified_note']:
            synonym_note = parse_pandoc(synonym['identified_note'])

            synonym_note_elem = et.SubElement(synonym_name_elem, 'note')
            synonym_note_elem.append(synonym_note)
                
        
        if taxon['accepted_status'] == 'ncomb':
            synonym_name_elem.set('combination', 'new')
        else:
            synonym_name_elem.set('combination', 'original')

        authority_elem = et.SubElement(synonym_elem, 'authority')
        authority_elem.set('rid', synonym['identified_authority'])

        reference_elem = et.SubElement(synonym_elem, 'reference')
        reference_elem.set('rid', synonym['reference'])

        if synonym['pageref']:
            reference_elem.set('page', synonym['pageref'])

        if synonym['location'] or synonym['utm_wgs84'] or synonym['longitude']:
            location_elem = et.SubElement(synonym_elem, 'location')

            if synonym['location']:
                locality_elem = et.SubElement(location_elem, 'locality')
                locality_elem.text = synonym['location']

            if synonym['country']:
                country_elem = et.SubElement(location_elem, 'country-code')
                country_elem.text = synonym['country']

            if synonym['utm_wgs84']:
                utm_elem = element_utm(synonym['utm_wgs84'])
                location_elem.append(utm_elem[1])

                wgs_elem = element_coordinates(lat=utm_elem[0][0], lon=utm_elem[0][1])
                location_elem.append(wgs_elem)
            elif synonym['longitude'] and synonym['latitude']:
                coord_elem = element_coordinates(lat=synonym['latitude'], lon=synonym['longitude'])
                location_elem.append(coord_elem)
       
        lithostrat_elem = et.Element('lithostratigraphy')
        chronostrat_elem = et.Element('chronostratigraphy')
        biostrat_elem = et.Element('biostratigraphy')
        for key in lithostrat_keys:
            if synonym[key]:
                strat_elem = et.SubElement(lithostrat_elem, key)
                strat_elem.text = synonym[key]

        for key in chronostrat_keys:
            if synonym[key]:
                strat_elem = et.SubElement(chronostrat_elem, key)
                strat_elem.text = synonym[key]

        for key in biostrat_keys:
            if synonym[key]:
                parsed_text = parse_pandoc(synonym[key])

                strat_elem = et.SubElement(biostrat_elem, key)
                strat_elem.append(parsed_text)


        if lithostrat_elem or chronostrat_elem or biostrat_elem:
            stratigraphy_elem = et.SubElement(synonym_elem, 'stratigraphy')

            if lithostrat_elem:
                stratigraphy_elem.append(lithostrat_elem)
            if chronostrat_elem:
                stratigraphy_elem.append(chronostrat_elem)
            if biostrat_elem:
                stratigraphy_elem.append(biostrat_elem)

        if synonym['lsid_act']:
            lsid_act_elem = element_lsid(lsid=synonym['lsid_act'])
            synonym_elem.append(lsid_act_elem)

        if synonym['lsid_pub']:
            lsid_pub_elem = element_lsid(lsid=synonym['lsid_pub'])
            synonym_elem.append(lsid_pub_elem)

        if synonym['comments']:
            parsed_comment = parse_pandoc(synonym['comments'])

            comments_elem = et.SubElement(synonym_elem, 'comments')
            comments_elem.append(parsed_comment)

        
# tree = et.ElementTree(root)

# Format the XML content to make it easier to view
xml_str = minidom.parseString(et.tostring(root, encoding='unicode')).toprettyxml(indent='\t')
# xml_str = html.unescape(xml_str)

with open(outfile, 'w') as f:
    # tree.write(f, encoding='unicode')
    f.write(xml_str)
