\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{myreport}[2015/10/22 My report class]

%%% load article class and settings as base
\LoadClass{article}


%%% additional typographic commands
\newcommand{\textallsc}[1]{{\addfontfeatures{Letters={SmallCaps,UppercaseSmallCaps},Numbers={Lowercase}}#1}}
\newcommand\textcaps[1]{{{\addfontfeatures{Numbers=Uppercase,Letters=Uppercase}\uppercase{#1}}}}


%%% vertically centre in-text figures
\newcommand*{\vcenteredhbox}[1]{\begingroup
\setbox0=\hbox{#1}\parbox{\wd0}{\box0}\endgroup}


%%% use fontspec with TeX replacements and letterspaced small caps
\RequirePackage{fontspec}
\defaultfontfeatures{Ligatures=TeX,SmallCapsFeatures={LetterSpace=5}}


%%% use microtype
\RequirePackage[protrusion=true,expansion=true]{microtype}
\UseMicrotypeSet[protrusion,expansion]{basictext}


%%% setup page layout
\RequirePackage[a4paper]{geometry}
\geometry{left=7cm,right=1.75cm,top=1.65cm,bottom=3cm,marginparsep=0.25cm,marginparwidth=5cm}



%%%%%%%%%%%%%%%%%
%               %
% Class options %
%               %
%%%%%%%%%%%%%%%%%


%%% new option: ‘textfigs’: use text figures as default
\DeclareOption{textfigs}{\defaultfontfeatures{Ligatures=TeX,Numbers=Lowercase,SmallCapsFeatures={LetterSpace=5}}}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax

%%% outdented-number footnote formatting
%\renewcommand\@makefntext[1]{%
%	\makebox[-1em][r]{\@thefnmark}\quad\noindent\parbox[t][\height][c]{\textwidth}{#1}}


%%% \LuaLaTeX stylised logo
\RequirePackage{metalogo}


%%% use ISO date format
\RequirePackage{isodate}


%%% caption formatting
%\RequirePackage{graphicx}
%\RequirePackage{caption}
%\RequirePackage{subcaption}
%\RequirePackage{textcomp}
%\DeclareCaptionFont{captionlabelfont}{\fontspec{Avenir Next}[UprightFont={* Medium},ItalicFont={* Medium Italic},BoldFont={* Bold},BoldItalicFont={* Bold Italic},Scale=MatchLowercase]}
%\DeclareCaptionFont{captioncondlabelfont}{\fontspec{Avenir Next}[UprightFont={* Condensed Medium},ItalicFont={* Condensed Medium Italic},BoldFont={* Condensed Bold},BoldItalicFont={* Condensed Bold Italic},Scale=MatchLowercase]}
%\DeclareCaptionFont{captionfont}{\fontspec{Kepler Std Semicondensed}[Scale=MatchLowercase]}
%\DeclareCaptionLabelFormat{captionlabelformat}{{#1~#2}}
%\captionsetup{justification=justified,singlelinecheck=false,font={footnotesize},textfont={captionfont},labelfont={captioncondlabelfont},labelsep=colon,labelformat=captionlabelformat,format=plain,width=\marginparwidth}
%\captionsetup[subfigure]{justification=justified,singlelinecheck=false,font={footnotesize},textfont={captionfont},labelfont={captionlabelfont},labelsep=quad,labelformat=parens,format=hang,margin={0cm,5.25cm}}
%\captionsetup[lstlisting]{justification=justified,singlelinecheck=false,font={footnotesize},textfont={captionfont},labelfont={captioncondlabelfont},labelsep=colon,labelformat=captionlabelformat,format=hang,margin={0cm,5.25cm}}


%%% floats with side captions setup
%\RequirePackage{floatrow}
%\floatsetup[figure]{margins=hangleft,capposition=beside,capbesideposition={top,left},floatwidth=\textwidth}


%%% headers & footer formatting
%\RequirePackage{fancyhdr}
%\pagestyle{fancy}
%\fancyhf{}%
%\renewcommand{\sectionmark}[1]{\markboth{\textcaps{#1}}{}}
%\renewcommand{\headrulewidth}{0pt}
%\renewcommand{\footrulewidth}{0pt}
%\fancyhfoffset[R]{2em}
%\fancyfoot[R]{\small{\leftmark\hspace{1em}\vrule\hspace{1em}\makebox[0.45em][c]{\thepage}}}


%%% reformat \maketitle
\renewcommand*{\maketitle}{%
{\LARGE\addfontfeatures{Letters=Uppercase,Numbers=Uppercase,LetterSpace=8,WordSpace=2}\MakeUppercase{\@title}\par\vspace{1em}}
	{\large\@author\par\vspace{1em}}
	{\large\textsf{\@date}\par}
}


\endinput