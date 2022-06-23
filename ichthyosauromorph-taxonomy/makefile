# Makefile for ichthyosauromorphtaxonomy.pdf
#

.PHONY: all

all: ichthyosauromorphtaxonomy.pdf

# Process data tables into XML
ichthyosauromorpha.xml: write_synonymy_xml.py ichthyosauromorph-species.tsv ichthyosauromorph-synonymy.tsv
	python $< ichthyosauromorph-species.tsv ichthyosauromorph-synonymy.tsv Ichthyosauromorpha

# This will change to processing by ConTeXt
# ichthyosauromorphtaxonomy.pdf: ichthyosauromorphtaxonomy.tex introduction.tex hupehsuchia.tex ichthyosauriformes.tex synonymy.cls synonymy.bib
# 	latexmk -norc -silent -f -lualatex $< && latexmk -c $<

# clean:
# 	latexmk -c ichthyosauromorphtaxonomy.tex
