#! /usr/bin/python
'''Create taxonomy and synonymy lists from TSV files

This script fills a LaTeX template file to produce a document showing a list of
taxa and synonymy.
'''

import sys
import csv
import re
from xml.etree import ElementTree as ET
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

taxon_name = '''\
\\species{accepted_name}{\\cauthyr{accepted_authority}}id_link\n
'''

synonym_row = '''\
assignment_confidence & \\cyear{reference} & \\emph{identified_name} \\cauth{identified_authority} identified_note & \\crefauth{reference} pageref locality_info \\\\
'''


def find_replace_multi(string, dictionary):
    '''Replace multiple patterns within string.
    '''

    for item in dictionary.keys():
        string = re.sub(item, dictionary[item], string)
    return string


def get_ref_dates(filename):
    '''Retrieve the dates from a set of references given a reference key and Bib(La)TeX file.
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


def format_lsidref(lsid):
    '''Format an LSID reference.
    '''

    formatted_href = r'\\lsidref{' + lsid + '}'

    return(formatted_href)


def format_lsidlink(lsid):
    '''Format an LSID string
    '''

    formatted_href = r'\\lsid{' + lsid + '}'

    return(formatted_href)


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

# def latlong_to_utm(latlon_coord):
#     ll_parser =


def prettify_latlon(utm_latlon):
    '''Add typographical features for printing latitude-longitude coordinates.
    '''

    lat = str(round(utm_latlon[0], 7))
    lon = str(round(utm_latlon[1], 7))

    if utm_latlon[0] > 0:
        lat = lat + '° N'
    else:
        lat = lat + '° S'

    if utm_latlon[1] > 0:
        lon = lon + '° E'
    else:
        lon = lon + '° W'

    return(lat + ' ' + lon)


def osm_link_latlon(latlon):
    '''Geneate an OpenStreetMap URL from latitude-longitude coordinates.
    '''

    lat = str(round(latlon[0], 7))
    lon = str(round(latlon[1], 7))

    osm_link_str = f'https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=6/{lat}/{lon}'

    return(osm_link_str)

def create_xml_element(element, text, attrib={}):
    elem = ET.Element(element, attrib=attrib)
    elem.text = text

    return(elem)

def osm_pretty_link_latlon(latlon):
    '''Generate a typographically-formatted link for printing latitude-longitude coordinates.
    '''

    osm_link_str = osm_link_latlon(latlon)
    pretty_latlon = prettify_latlon(latlon)

    coord_elem = create_xml_element('coord', pretty_latlon, attrib={ 'osm_uri': osm_link_str })
    test = ET.SubElement(coord_elem, 'test')
    test.text = "Some extra text"
    # tex_str = r'\\osm{' + pretty_latlon + '}{' + osm_link_str + '}'

    return(coord_elem)


def osm_pretty_link_utm(utm_coord):
    '''Generate a typographically-formatted link for printing UTM coordinates.
    '''

    latlon = utm_to_latlon(utm_coord)
    osm_link_str = osm_link_latlon(latlon)

    tex_str = r'\\osm{UTM WGS84 ' + utm_coord + '}{' + osm_link_str + '}'

    return(tex_str)


synonymy_dict = get_ref_dates(synonymy_file)
sorted_synonymy = sorted(synonymy_dict, key=lambda row: row['date'])

taxa_to_print = get_higher_taxon(taxon_file)

text_sanitising = {r'\.\.': r'.', r'\s\s': r' '}

unit_separator = ', '
lithostrat_keys = ['bed', 'member', 'formation', 'zone']
chronostrat_keys = ['stage', 'series', 'system']
coord_keys = ['utm_wgs84', 'long', 'lat']

outfile = clade_name.lower() + '.tex'


with open(outfile, 'wt') as out_file:

    out_file.write('%! TEX root = ichthyosauromorphtaxonomy.tex\n\n')

    for taxon in taxa_to_print:
        current_taxon = taxon['accepted_name']
        this_taxon = find_replace_multi(taxon_name, taxon)

        if taxon['accepted_status'] == 'ncomb':
            this_taxon = re.sub('cauthyr', 'pauthyr', this_taxon)

        if len(taxon['lsid_act']) > 0:
            this_taxon = re.sub('id_link', '[' + taxon['lsid_act'] + ']', this_taxon)
        else:
            this_taxon = re.sub('id_link', '', this_taxon)

        these_synonyms = str()

        for synonym in sorted_synonymy:
            current_synonym = synonym['identified_name']

            if synonym['accepted_name'] == current_taxon:
                print('Record matched:', current_synonym, "→", current_taxon)

                lithostratigraphy = unit_separator.join([x for x in [synonym.get(key) for key in lithostrat_keys] if x])

                chronostratigraphy = unit_separator.join([x for x in [synonym.get(key) for key in chronostrat_keys] if x])

                locality_info = str()
                if len(chronostratigraphy) > 0 and len(lithostratigraphy) > 0:
                    locality_info = lithostratigraphy + ' (' + chronostratigraphy + ')'
                elif len(chronostratigraphy) > 0:
                    locality_info = chronostratigraphy
                elif len(lithostratigraphy) > 0:
                    locality_info = lithostratigraphy

                if len(synonym['location']) > 0 and len(locality_info) > 0:
                    locality_info = locality_info + '; ' + synonym['location']
                elif len(synonym['location']) > 0:
                    locality_info = synonym['location']

                coord_info = str()
                if len(synonym['utm_wgs84']) > 0 and len(synonym['longitude']) > 0:
                    pretty_utm = osm_pretty_link_utm(synonym['utm_wgs84'])
                    coord_info = pretty_utm + r' = \\textallsc{' + synonym['latitude'] + ' ' + synonym['longitude'] + '}'
                elif len(synonym['utm_wgs84']) > 0:
                    pretty_utm = osm_pretty_link_utm(synonym['utm_wgs84'])
                    latlon_convert = utm_to_latlon(synonym['utm_wgs84'])
                    coord_info = pretty_utm + ' = ' + str(ET.tostring(osm_pretty_link_latlon(latlon_convert), encoding='unicode'))

                if len(locality_info) > 0 and len(coord_info) > 0:
                    locality_info = '[' + locality_info + ' (' + coord_info + ').] '
                elif len(locality_info) > 0 and len(coord_info) == 0:
                    locality_info =  '[' + locality_info + '.] '
                elif len(locality_info) == 0 and len(coord_info) > 0:
                    locality_info = '[' + coord_info + '] '
                 
                if len(synonym['pageref']) > 0:
                    synonym['pageref'] = 'p~' + synonym['pageref']

                if len(synonym['lsid_act']) > 0:
                    synonym['identified_note'] = synonym['identified_note'] + format_lsidlink(synonym['lsid_act'])

                if len(synonym['lsid_pub']) > 0:
                    locality_info = locality_info + format_lsidref(synonym['lsid_pub']) + ' '

                if len(synonym['comments']) > 0:
                    locality_info = locality_info + synonym['comments']

                this_synonym = find_replace_multi(synonym_row, synonym)

                if synonym['identified_status'] == 'ncomb':
                    this_synonym = re.sub('cauth', 'pauth', this_synonym)

                if synonym['morphological_information'] == 'N':
                    this_synonym = re.sub('cyear', 'emyear', this_synonym)

                these_synonyms = these_synonyms + re.sub('locality_info', locality_info, this_synonym)

        if len(these_synonyms) > 0:
            these_synonyms = find_replace_multi(these_synonyms, text_sanitising)
            these_synonyms = '\\begin{synonymy}\n' + these_synonyms + '\\end{synonymy}\n\n'

        out_file.write(this_taxon)
        out_file.write(these_synonyms)
