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
\\emph{accepted_name} \cite{accepted_authority}\n
'''

synonym_row = '''\
assignment_confidence & \\cite*{reference} & \\emph{identified_name} \\citeauthor*{identified_authority} \\\\
'''

def find_replace_multi(string, dictionary):
    for item in dictionary.keys():
        string = re.sub(item, dictionary[item], string)
    return string

def filter_taxon(row):
    return current_taxon in row['accepted_name']

# with open(taxon_file, newline = '') as taxa, open(synonymy_file, newline = '') as synonymy:
#     taxa = csv.DictReader(taxa, delimiter = '\t')
#     synonymy = csv.DictReader(synonymy, delimiter = '\t')

with open(outfile, 'wt') as out_file:
    
    for taxon in csv.DictReader(open(taxon_file, newline = ''), delimiter = '\t'):
        current_taxon = taxon['accepted_name']
        this_taxon = find_replace_multi(taxon_name, taxon)
        these_synonyms = str()
    
        for synonym in csv.DictReader(open(synonymy_file, newline = ''), delimiter = '\t'):
            current_synonym = synonym['accepted_name']
    
            if current_synonym == current_taxon:
                print('Synonym matched:', current_synonym, "=", current_taxon)
    
                these_synonyms = these_synonyms + find_replace_multi(synonym_row, synonym)

        if len(these_synonyms) > 0:
            these_synonyms = '\\begin{tabularx}{42em}{llX}\n' + these_synonyms + '\\end{tabularx}\n\n'
         
        # print(this_taxon)
        # print(these_synonyms)

        out_file.write(this_taxon)
        out_file.write(these_synonyms)

