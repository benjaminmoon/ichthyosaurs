#!/usr/bin/env python3

import sys
import os
import pandas as pd
import numpy as np

matrices = len(sys.argv)

def df_strip(df):
    df = df.copy()
    for c in df.columns:
        if df[c].dtype == np.object:
            df[c] = pd.core.strings.str_strip(df[c])
    return df

def polymorph(df):
    df = df.copy()
    df.replace({'(\d)\&(\d)' : '\(\1\s\2\)'}, regex = True)
    return df

# turn list of states into taxon-character matrix
for file in range(1, matrices):
    name = os.path.splitext(os.path.basename(sys.argv[file]))[0]
    csvfile = pd.read_csv(sys.argv[file], encoding='utf-8')
    csvfile.replace({'(\d)\&(\d)' : '\(\1\s\2\)'}, regex = True)
    csvfile.columns = csvfile.columns.str.strip()
    pivot = csvfile.pivot(index='Taxon', columns = 'Number', values = 'State')
    filename = name + '.nex'
    pivot.to_csv(filename, encoding='utf-8')