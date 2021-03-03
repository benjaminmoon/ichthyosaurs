# Ichthyosauromorph Taxonomy

Contained within is a list of valid ichthyosaur species, with a steadily more
comprehensive synonymy list. I would like to have all references to ichthyosaur
species listed here, but that might be a pipe dream.

## Folder layout ##

The main documents are:

* `ichthyosauromorphtaxonomy.pdf` the master list (version 0.5 as of
2021-02-26).
* `ichthyosauromorphtaxonomy.tex` the LuaLaTeX file that the PDF is built from.

These are built using a Python script `write_synonymy.py`. This processes two
TSV files, one of valid species and the second with synonyms, references and
occurrences. A column, _accepted_name_ links the two files: rows from the
synonymy file are listed under their _accepted_name_ in the valid species file.

Use the following to process the taxonomy:

```
python3 write_synonymy.py ichthyosauromorph-species.tsv ichthyosauromorph-synonymy.tsv ichthyosauromorph-synonymy.tex
```

The four arguments required are:

1. `write_synonymy.py`: the python script.
2. `ichthyosauromorph-species.tsv`: TSV of valid species.
3. `ichthyosauromorph-synonymy.tsv`: TSV of records.
4. `ichthyosauromorph-synonymy.tex`: the name of the formatted TeX file to write.

## Dependencies for compiling the TeX file ##

I've used a custom Tufte-style class, _tufte-lualatex_ that I've also included.
This makes many changes in the style of Edward Tufte's books and the related
_tufte-latex_ class files.[^1][^2] I couldn't always get _tufte-latex_ to work,
wanted more control and an excuse to try making my own class file, so I built
this. It replicates many of the features, but will more of my opinions built
into it.

The most recent revision of _tufte-lualatex_ requires LuaLaTeX and fontspec –
recent versions should be adequate. As set up in `ichthyosauromorphtaxonomy.tex`
it also requires the recent releases of Adobe's _Source Serif 4_ and _Source
Sans 3,_ the former of which includes the nicety of optical sizing.

* _Source Serif 4:_ <https://github.com/adobe-fonts/source-serif>
* _Source Sans 3:_ <https://github.com/adobe-fonts/source-sans>

These fonts are not (yet?) included in CTAN, so should be downloaded and placed
somewhere that _luaotfload-tool_ can find them (e.g. a TEXMF tree or default
fonts directory). If you can't use these fonts, change the class option to
`font=oldsource` to use the older _Source Serif Pro_ and _Source Sans Pro_ fonts
included with their respective packages on CTAN.

[^1]: e.g. <https://www.edwardtufte.com/tufte/>

[^2]: <https://www.ctan.org/pkg/tufte-latex>
