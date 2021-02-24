#! /usr/bin/python
'''Create taxonomy and synonymy lists from TSV files

This script fills a LaTeX template file to produce a document showing a list of
taxa and synonymy.
'''

import sys
import csv
import re

# return error if the wrong number of arguments are given
# usage is given in the error return value
try:
    script_file = sys.argv[0]
    taxon_file, synonymy_file, outfile = sys.argv[1:]
except ValueError:
    print('Usage: {} taxon_file synonymy_file outfile'.format(script_file))

taxon_name = '''\
\\emph{accepted_name}~\cite{accepted_authority}\n
'''

synonym_row = '''\
assignment_confidence & \\cyear{reference} & \\emph{identified_name} \\cauth{identified_authority}; p~pageref locality_info \\\\
'''

def find_replace_multi(string, dictionary):
    for item in dictionary.keys():
        string = re.sub(item, dictionary[item], string)
    return string

texy_strings = {
        '* ' : '\textasterisk '
}

with open(outfile, 'wt') as out_file:
    
    out_file.write('%! TEX root = test_tex.tex\n\n')

    for taxon in csv.DictReader(open(taxon_file, newline = ''), delimiter = '\t'):
        current_taxon = taxon['accepted_name']
        this_taxon = find_replace_multi(taxon_name, taxon)
        these_synonyms = str()
    
        for synonym in csv.DictReader(open(synonymy_file, newline = ''), delimiter = '\t'):
            current_synonym = synonym['identified_name']
    
            if synonym['accepted_name'] == current_taxon:
                print('Record matched:', current_synonym, "→", current_taxon)
    
                if synonym['identified_status'] == 'ncomb':
                    synonym_row = re.sub('citeauthor\*', 'pciteauthor', synonym_row)

                unit_separator = ', '

                lithostrat_keys = ['bed', 'member', 'formation', 'zone']
                lithostratigraphy = unit_separator.join([x for x in [synonym.get(key) for key in lithostrat_keys] if x])

                chronostrat_keys = ['stage', 'series', 'system']
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

                if len(locality_info) > 0:
                    locality_info = '[' + locality_info + '.] '
                if len(synonym['comments']) > 0:
                    locality_info = locality_info + synonym['comments']

                this_synonym = find_replace_multi(synonym_row, synonym)
                these_synonyms = these_synonyms + re.sub('locality_info', locality_info, this_synonym)

        if len(these_synonyms) > 0:
            these_synonyms = '\\begin{tabularx}{42em}{rlX}\n\\small\n' + these_synonyms + '\\end{tabularx}\n\n'

        out_file.write(this_taxon)
        out_file.write(these_synonyms)

