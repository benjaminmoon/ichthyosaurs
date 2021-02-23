#! /usr/bin/python

import sys
import csv

# return error if the wrong number of arguments are given
# usage is given in the error return value
try:
    script_file = sys.argv[0]
    taxon_file, synonymy_file, outfile = sys.argv[1:]
except ValueError:
    print("Usage: {} taxon_file synonymy_file outfile".format(script_file))

# function to read in file given as script arguments
# def read_file(filename):
#     try:
#         with open(filename) as f:
#             return f.read()
#     except FileNotFoundError:
#         print("Could not find input file: {}".format(filename))
#         sys.exit()

with open(taxon_file, newline = "") as taxa:
    taxa = csv.reader(taxa, delimiter = "\t")
    
    for row in taxa:
        print(row[0], "\cite{", row[1], "}")
