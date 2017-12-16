#!/usr/bin/env python3

import sys
import os
import pandas as pd

matrices = len(sys.argv)

# turn list of states into taxon-character matrix
for file in range(1, matrices):
    name = os.path.splitext(os.path.basename(sys.argv[file]))[0]
    csvfile = pd.read_csv(sys.argv[file])
    pivot = csvfile.pivot(index='Taxon', columns = 'Number', values = 'State')
    filename = name + '.nex'
    pivot.to_csv(filename, encoding='utf-8')