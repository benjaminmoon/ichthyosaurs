# Makefile for ichthyosauromorpha.pdf
#

.PHONY: all

all: ichthyosauromorpha.pdf

# Process data tables into XML
ichthyosauromorpha.xml: write_synonymy_xml.py ichthyosauromorph-species.tsv ichthyosauromorph-synonymy.tsv
	python $< ichthyosauromorph-species.tsv ichthyosauromorph-synonymy.tsv Ichthyosauromorpha

# This will change to processing by ConTeXt
ichthyosauromorpha.pdf: ichthyosauromorpha.xml introduction.tex synonymy-style.tex synonymy.bib
	context --environment=synonymy-style.tex $< 

# clean:
# 	latexmk -c ichthyosauromorphtaxonomy.tex
