# Makefile for ichthyosauromorphtaxonomy.pdf
#

.PHONY: all

all: ichthyosauromorphtaxonomy.pdf

hupehsuchia.tex: write_synonymy.py ichthyosauromorph-species.tsv ichthyosauromorph-synonymy.tsv
	python $< ichthyosauromorph-species.tsv ichthyosauromorph-synonymy.tsv Hupehsuchia

ichthyosauriformes.tex: write_synonymy.py ichthyosauromorph-species.tsv ichthyosauromorph-synonymy.tsv
	python $< ichthyosauromorph-species.tsv ichthyosauromorph-synonymy.tsv Ichthyosauriformes

ichthyosauromorphtaxonomy.pdf: ichthyosauromorphtaxonomy.tex introduction.tex hupehsuchia.tex ichthyosauriformes.tex synonymy.cls synonymy.bib
	latexmk -norc -silent -f -lualatex $< && latexmk -c $<

clean:
	latexmk -c ichthyosauromorphtaxonomy.tex
