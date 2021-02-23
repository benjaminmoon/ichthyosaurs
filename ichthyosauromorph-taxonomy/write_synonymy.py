#! /usr/bin/python
'''Create taxonomy and synonymy lists from CSV files

This script fills a LaTeX template file to produce a document showing a list of
taxa and synonymy.
'''

import sys
import csv

# return error if the wrong number of arguments are given
# usage is given in the error return value
try:
    script_file = sys.argv[0]
    taxon_file, synonymy_file, outfile = sys.argv[1:]
except ValueError:
    print('Usage: {} taxon_file synonymy_file outfile'.format(script_file))

# function to read in file given as script arguments
# def read_file(filename):
#     try:
#         with open(filename) as f:
#             return f.read()
#     except FileNotFoundError:
#         print("Could not find input file: {}".format(filename))
#         sys.exit()

with open(taxon_file, newline = '') as taxa, open(synonymy_file, newline = '') as synonymy:
    taxa = csv.DictReader(taxa, delimiter = '\t')
    synonymy = csv.DictReader(synonymy, delimiter = '\t')
    
    for trow in taxa:
        current_taxon = trow['accepted_name']

        print(list(trow))
        # synonymy[synonymy['accepted_name'] == current_taxon]
            # print(srow)
        # print(filtered)
        # print(row['accepted_name'], '\cite{', row['accepted_authority'], '}')
        # csv.writer(open(r'abx.csv', 'w'), delimiter = '\t').writerows(filtered)
