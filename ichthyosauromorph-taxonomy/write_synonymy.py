#! /usr/bin/python
'''Create taxonomy and synonymy lists from TSV files

This script fills a LaTeX template file to produce a document showing a list of
taxa and synonymy.
'''

import sys
import csv
import re
from pybibtex import build_citekey_dict
from pybibtex import parse_bibfile_to_cite_dict

# return error if the wrong number of arguments are given
# usage is given in the error return value
try:
    script_file = sys.argv[0]
    taxon_file, synonymy_file, clade_name, outfile = sys.argv[1:]
except ValueError:
    print('Usage: {} taxon_file synonymy_file outfile'.format(script_file))

taxon_name = '''\
\\species{accepted_name}{\\cauthyr{accepted_authority}}id_link\n
'''

synonym_row = '''\
assignment_confidence & \\cyear{reference} & \\emph{identified_name} \\cauth{identified_authority} identified_note & \\crefauth{reference} pageref locality_info \\\\
'''

def find_replace_multi(string, dictionary):
    for item in dictionary.keys():
        string = re.sub(item, dictionary[item], string)
    return string

def get_ref_dates(filename):
    with open(filename, newline = '') as f:
        syn = csv.DictReader(f, delimiter = '\t')
        bibfile = parse_bibfile_to_cite_dict(bib_path='synonymy.bib')
    
        for row in syn:
            refkey = '\\cite{' + row['reference'] + '}'
            citekey_dict = build_citekey_dict(refkey.split('\n'))
            for citekey in citekey_dict:
                refdate = bibfile[citekey]['date']
            yield dict(date = refdate, **row)

def get_higher_taxon(filename):
    with open(filename, newline = '') as f:
        tax = csv.DictReader(f, delimiter = '\t')

        for row in tax:
            if row['clade'] == clade_name:
                yield dict(**row)

def format_lsidref(lsid):
    formatted_href = r'\\lsidref{' + lsid + '}'

    return(formatted_href)

def format_lsidlink(lsid):
    formatted_href = r'\\lsid{' + lsid + '}'

    return(formatted_href)

synonymy_dict = get_ref_dates(synonymy_file)
sorted_synonymy = sorted(synonymy_dict, key = lambda row: row['date'])

taxa_to_print = get_higher_taxon(taxon_file)

text_sanitising = {r'\.\.': r'.', r'\s\s': r' '}

unit_separator = ', '
lithostrat_keys = ['bed', 'member', 'formation', 'zone']
chronostrat_keys = ['stage', 'series', 'system']
coord_keys = ['utm_wgs84', 'long', 'lat']

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
                    coord_info = r'\\textallsc{UTM WGS84 ' + synonym['utm_wgs84'] + ' = ' + synonym['latitude'] + ' ' + synonym['longitude'] + '}'
                elif len(synonym['utm_wgs84']) > 0:
                    coord_info = r'\\textallsc{UTM WGS84 ' + synonym['utm_wgs84'] + '}'

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

