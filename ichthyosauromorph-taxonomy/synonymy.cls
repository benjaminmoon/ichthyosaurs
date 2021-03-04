\NeedsTeXFormat{LaTeX2e}
\RequirePackage{expl3}
\RequirePackage{l3keys2e}
\ProvidesExplClass{synonymy}{2021/03/03}{0.1}{synonymy Package}
% A package to typeset synonymy lists with typographical niceties à la Edward
% Tufte, and reimagining the style of Tufte-LaTeX with my own preferences. It is
% an extension of the article class, with many things changed and the
% requirement of compiling with LuaLaTeX (luahblatex).
%
% This class file uses the custom key 'synonymy' for class-specific keys.


%%% Detect LuaLaTeX
%
% This package requires LuaLaTeX. This code checks for that. Taken from luacolor
% package.
% \ifx\directlua\@undefined
%   \PackageError{synonymy}{%
%     This package may only be run using LuaTeX%
%   }\@ehc
%   \expandafter
% \fi%


%%% Use LaTeX3 parsing
\ExplSyntaxOn

%%% Key options
%
% Options are given for selecting a pagesize and some font setup.
%
% The page size defaults to A4. Option definitions are given below, but this key
% switches beween A4, US letter, and tablet size (based on 4:3 aspect ratio, 10″
% screen diagonal; ~iPad size).
%
% * a4paper: A4 paper size
% * letter: US letter size
% * tablet: 4:3 tablet (landscape) size
%
% Source Serif 4 and Source Sans 3 are the preferred fonts, but if these aren't
% available then the older Source fonts can be used, which have packages
% available on CTAN.
\str_new:N \g__synonymy_pagesize_str
\keys_define:nn { synonymy } {
    font .code:n               = { \str_gset:Nn \g__synonymy_font_str {#1} },
    font .initial:n            = source,
    font .value_required:n     = false,
    pagesize .code:n           = { \str_gset:Nn \g__synonymy_pagesize_str {#1} },
    pagesize .initial:n        = a4paper,
    pagesize .value_required:n = false,
    oldsource .code:n          = { \str_gset:Nn \g__synonymy_font_str {oldsource} },
    letter .code:n             = { \str_gset:Nn \g__synonymy_pagesize_str {letter} },
    tablet .code:n             = { \str_gset:Nn \g__synonymy_pagesize_str {tablet} }
}
\ProcessKeysOptions{ synonymy }

% use article class as a base
\LoadClass{article}


%%% Language support
%
% These packages are loaded and used by several others. A language is not
% explicitly selected. Polyglossia does not set the language globally, so
% adding, e.g., 'UKenglish' into the class options may be needed.
\RequirePackage{csquotes}
\RequirePackage{polyglossia}


%%% Commands
%
% LaTeX3 style commands
\RequirePackage{xparse}


%%% Page layout
%
% Page layout follows Tufte's books in having a main column to the left of the
% page and a broad margin to the right to contain margin notes and figures. I've
% followed this but incorporated it into three different page sizes:
%
% 1. A4 paper (297 × 210 mm), globally used.
% 2. US letter paper (11 × 8.5 inches).
% 3. Tablet (~iPad) sized (4:3 aspect ratio landscape, 10″ diagonal).
%
% These are selected between using the `pagesize` key.
\RequirePackage{geometry}
\str_case:VnF \g__synonymy_pagesize_str {
    { a4paper }
    {
        \geometry{%
            paper          = a4paper,
            textwidth      = 26pc,
            marginparsep   = 2pc,
            marginparwidth = 16pc,
            left           = 3pc,
            textheight     = 60pc,
            headheight     = 1.5pc,
            top            = 4pc
        }
    }
    { letter }
    {
        \geometry{%
            paper          = letterpaper,
            textwidth      = 26pc,
            marginparsep   = 2pc,
            marginparwidth = 16pc,
            left           = 3pc,
            textheight     = 54pc,
            headheight     = 1.5pc,
            top            = 4pc
        }
    }
    { tablet }
    {
        % ipad 10.5 size
        % 2224 × 1668 px @ 264 ppi
        \geometry{%
            paperwidth      = 8.42in,
            paperheight     = 6.32in,
            left            = 4pc,
            right           = 22pc,
            top             = 2pc,
            bottom          = 3pc,
            marginparsep    = 2pc,
            marginparwidth  = 16pc,
            headheight      = 1.5pc,
            headsep         = 0.5pc,
            footskip        = 1.5pc
        }
    }
}{
    \ClassError {synonymy} {Unknown~page~size~setting}
    {
            Invalid~value~for~the~'pagesize'~option:~
               '\g__synonymy_pagesize_str'.
    }
}
% Where some more horizontal space is needed, the right margin can be used to do
% temporary 'full width' typesetting. More permanaent changes (e.g. references)
% should use `\newgeometry` instead.
\NewDocumentEnvironment{fullwidth}{}%
    {%
        \begin{list}{}{%
            \setlength{\leftmargin}{0pt}
            \setlength{\rightmargin}{-\marginparsep}\addtolength{\rightmargin}{-\marginparwidth}%
        } \item[]%
    }%
    {\end{list}}
    

%%% Font sizing
%
% Modified from the default article class. The font size is fixed at 11/14 pt.
% Sidenotes are set in footnotesize (9pt).
\RenewDocumentCommand{\normalsize}{}{%
    \@setfontsize\normalsize{11}{14}%
    \abovedisplayskip 11\p@ \@plus3\p@ \@minus6\p@
    \abovedisplayshortskip \z@ \@plus3\p@
    \belowdisplayshortskip 6\p@ \@plus2\p@ \@minus\p@
    \belowdisplayskip \abovedisplayskip
    \let\@listi\@listI}
\ProvideDocumentCommand{\synonymy@sidenotefontsize}{}{\footnotesize}
\ProvideDocumentCommand{\SetSidenoteFontSize}{ m }{
    \RenewDocumentCommand{\synonymy@sidenotefontsize}{}{#1}
}


%%% Colours
%
% Several custom colours are used to highlight text and links. The _accent
% colour_ can be changed; this is the main 'theme' of the document. Other
% colours, like for citations and URLs, are standardised.
\RequirePackage{xcolor}
\RequirePackage{luacolor}
% set up an accent colour
\NewDocumentCommand{\SetAccentColour}{o m}{
    \IfNoValueTF{#1}{
        \colorlet{synonymy@accentcolour}{#2}
    }{
        \definecolor{synonymy@accentcolour}{#1}{#2}
    }
}
\NewDocumentCommand{\accentcol}{}{synonymy@accentcolour}
% default colour is red
\SetAccentColour{red}
% accent text to bring it out
\NewDocumentCommand{\synonymy@accenttext}{ m }{%
    \textcolor{synonymy@accentcolour}{#1}%
}
\NewDocumentCommand{\textaccent}{m}{%
   % \textcolor{synonymy@accentcolour}{#1}%
    \synonymy@accenttext{#1}%
}
% hyperref link colours
\definecolor{synonymy@citelinkcolour}{Hsb}{185,0.80,0.40}
\colorlet{citelinkcolour}{synonymy@citelinkcolour}
\definecolor{synonymy@urllinkcolour}{Hsb}{300,0.80,0.40}
\colorlet{urllinkcolour}{synonymy@urllinkcolour}


%%% Typographical niceness
%
% A series of features and typographical extras.

%%%%%% LuaLaTeX logo
\RequirePackage{metalogo}

%%%%%% Microtypography
\RequirePackage{microtype}
% Don't use expansion as much of the text is ragged right
    \microtypesetup{expansion = false}

%%%%%% OpenType feature selection
\RequirePackage{fontspec}
\defaultfontfeatures{%
    SmallCapsFeatures = {LetterSpace = 5.0},
    Ligatures         = TeX
}
% The following commands give easier access to small caps and large caps with
% refined letterspacing and kerning.
\ProvideDocumentCommand{\textallsc}{ m }%
    {{\addfontfeatures{Letters = {UppercaseSmallCaps, SmallCaps}}#1}}
\ProvideDocumentCommand{\textcaps}{ m }%
    {{\addfontfeatures{Kerning = Uppercase, Numbers = Uppercase, LetterSpace = 8.0}\MakeUppercase{#1}}}
% Make typeset fractions with OpenType features.
\ProvideDocumentCommand{\txfrac}{ m m }%
    {{\addfontfeatures{Fractions = On}#1/#2}}
% Use OpenType sub- and superscripts by default.
\RequirePackage{realscripts}

%%%%%% Fonts
%
% This class by default uses the Source Serif 4, Source Sans 3, and Source Code
% Pro fonts. These are made freely available for use by Adobe and can be
% downloaded from:
%
% * Source Serif 4: https://github.com/adobe-fonts/source-serif
% * Source Sans 3: https://github.com/adobe-fonts/source-sans
% * Source Code Pro: https://github.com/adobe-fonts/source-code-pro
%
% Once downloaded, the fonts should be placed somehwere that LuaLaTeX and
% luaotfload can pick them up – either the OS font directory or in the TEXMFHOME
% tree, for instance.
%
% These fonts have a, to me, brilliant combination of features and design that
% makes them excellent for using in digital and printed documents. This includes
% optical sizing of the fonts (in Source Serif 4) to make text at small and
% large sizes seem more even. Checkout the differences between the species names
% and text in the synonymy. The optical sizes are not picked up by default, so
% are defined in the code below.
%
% The option 'oldsource' is included to typeset using the CTAN packages
% available for old versions of these fonts.
\str_case:VnF \g__synonymy_font_str {
    { oldsource }
    {
        % \setmainfont{Source Serif Pro}[Numbers = {OldStyle, Proportional}]
        % \setsansfont{Source Sans Pro}[Scale = MatchLowercase, Numbers = {OldStyle, Proportional}]
        % \setmonofont{Source Code Pro}[Scale = MatchLowercase]
        \RequirePackage[osf,proportional]{sourceserifpro}
        \RequirePackage[osf,proportional]{sourcesanspro}
        \RequirePackage[osf]{sourcecodepro}
    }
    { source }
    {
        \setmainfont{Source Serif 4}[%
            Scale = MatchLowercase,
            UprightFeatures = {
                SizeFeatures = {  
                    {Size = -8.5,   Font = Source Serif 4 Caption},
                    {Size = 8.5-11, Font = Source Serif 4 SmText},
                    {Size = 11-16,  Font = Source Serif 4},
                    {Size = 16-24,  Font = Source Serif 4 Subhead},
                    {Size = 24-,    Font = Source Serif 4 Display}
                } 
            }, 
            ItalicFeatures = {
                SizeFeatures = {  
                    {Size = -8.5,   Font = Source Serif 4 Caption Italic},
                    {Size = 8.5-11, Font = Source Serif 4 SmText Italic},
                    {Size = 11-16,  Font = Source Serif 4 Italic},
                    {Size = 16-24,  Font = Source Serif 4 Subhead Italic},
                    {Size = 24-,    Font = Source Serif 4 Display Italic}
                } 
            }, 
            BoldFeatures = {
                SizeFeatures = {  
                    {Size = -8.5,   Font = Source Serif 4 Caption Bold},
                    {Size = 8.5-11, Font = Source Serif 4 SmText Bold},
                    {Size = 11-16,  Font = Source Serif 4 Bold},
                    {Size = 16-24,  Font = Source Serif 4 Subhead Bold},
                    {Size = 24-,    Font = Source Serif 4 Display Bold}
                } 
            }, 
            BoldItalicFeatures = {
                SizeFeatures = {  
                    {Size = -8.5,   Font = Source Serif 4 Caption Bold Italic},
                    {Size = 8.5-11, Font = Source Serif 4 SmText Bold Italic},
                    {Size = 11-16,  Font = Source Serif 4 Bold Italic},
                    {Size = 16-24,  Font = Source Serif 4 Subhead Bold Italic},
                    {Size = 24-,    Font = Source Serif 4 Display Bold Italic}
                } 
            }, 
            Numbers = {OldStyle, Proportional}
        ]
        \setsansfont{Source Sans 3}[%
            Scale = MatchLowercase, Numbers = {OldStyle, Proportional}
        ]
        \setmonofont{Source Code Pro}[%
            Scale = MatchLowercase, Numbers = {OldStyle}
        ]
    }
}{
    \ClassError { synonymy } {Unknown~language~setting}
    {
            Invalid~value~for~the~'fonts'~option:~
               '\g__synonymy_font_str'.
    }
}

%%%%%% Columns
%
% Columns are used in the list of species and bibliography as the fonts used are
% smaller there.
\RequirePackage{multicol}

%%%%%% Dates
%
% Use the British format (3 March 2021) without the ordinal (st, nd, rd, th).
\RequirePackage[cleanlook, british]{isodate}

%%%%%% Lists
%
% Lists are formatted to include space between the top level items, then less
% vertical space and more indenting at lower levels.
\RequirePackage[inline]{enumitem}
% Two levels of itemising:
%
% * Level 1
%
%   * Level 2
%   * Level 2
%
% * Level 1
    \setlist[itemize,1]{%
    	noitemsep,%
    	align      = right,%
        leftmargin = 0em%
    }
    \setlist[itemize,2]{%
    	nosep,%
    	align      = right,%
        leftmargin = \parindent%
    }
% Three levels of enumeration:
% 
% (1) Level 1
% 
%    a. Level 2
%       a. Level 3
%    b. Level 2
%    c. Level 2
%    
% (2) Level 1
    \setlist[enumerate,1]{%
        label = {%
            {\addfontfeatures{Numbers={Monospaced,Lining}}(\arabic*)}%
        },%
        align      = right,%
        leftmargin = 0em%
    }
    \setlist[enumerate,2]{%
	    noitemsep,
    	label      = {(\alph*)},%
	    align      = right,%
	    leftmargin = \parindent%
    }
    \setlist[enumerate,3]{%
        nosep,
        label      = {(\alph*)},%
        align      = right,%
        leftmargin = 2\parindent%
    }
% Three levels of description:
% 
% Level 1
% 
%   Level 2
%       Level 3
%   Level 2
%   Level 2
%   
% Level 1
    \setlist[description,1]{%
    	leftmargin = 0\parindent,%
        font       = \normalfont\itshape
    }
    \setlist[description,2]{%
        noitemsep,%
    	labelindent = 1\parindent,%
        font        = \normalfont\itshape
    }
    \setlist[description,3]{%
        nosep,%
    	leftmargin  = 2\parindent,%
        font        = \normalfont\itshape%
    }
% Also create a new inline enumeration setup.
    \newlist{inlineenum}{enumerate*}{1}
    \setlist[inlineenum]{%
    	itemjoin  = {{, }},%
	    itemjoin* = {{, and }},%
	    label     = {{(\arabic*)}}
    }

%%%%%% New thought
%
% Rather than many levels of subsubsection and so on, Tufte suggests separating
% ideas as a 'new thought' with some empty space and beginning the next
% paragraph with small caps.
\ProvideDocumentCommand\newthought{ m }{%
    % Create vertical space before a new paragraph then typset the argument text
    % in small caps.
    \vspace{\baselineskip}\par
    {\noindent\textsc{#1}}
}

%%%%%% Ragged right
%
% Use ragged right (left justification) throughout, as in Tufte's books.
\RequirePackage{ragged2e}
    \setlength{\RaggedRightParindent}{\parindent}
    \AtBeginDocument{\RaggedRight}

%%%%%% Sidenotes
%
% Create rich sidenotes
\RequirePackage{marginfix}
\RequirePackage{sidenotes}
% Use sidenotes to include footnotes
\RenewDocumentCommand\footnote{ m }%
    {\sidenote{#1}}
% Make sidenote text sidenotesize with red number
\RenewDocumentCommand\sidenotetext{ o o +m }{% 
\IfNoValueOrEmptyTF{#1}{%
    \@sidenotes@placemarginal{#2}{%
        \RaggedRight\synonymy@sidenotefontsize\sffamily%
        \noindent\synonymy@accenttext{\thesidenote}{}~#3}%
    \refstepcounter{sidenote}%
}{%
    \@sidenotes@placemarginal{#2}{%
        \RaggedRight\synonymy@sidenotefontsize\sffamily%
        \noindent\synonymy@accenttext{#1}~#3}%
    }%
}
% Accent-colour sidenote numbers
% Modify sidenote mark to use opentype superscripts
\RenewDocumentCommand\@sidenotes@thesidenotemark{ m }{%
    \leavevmode%
    \ifhmode%
        \edef\@x@sf{\the\spacefactor}%
        \nobreak%
    \fi%
    \hbox{{\normalfont#1}}%
    \ifhmode%
        \spacefactor\@x@sf%
    \fi%
    \relax%
}
\RenewDocumentCommand\sidenotemark{ o }{%
    \@sidenotes@multichecker%
    \IfNoValueOrEmptyTF{#1}
        {\@sidenotes@thesidenotemark{\synonymy@accenttext%
            {\textsuperscript{\thesidenote}}}}
        {\@sidenotes@thesidenotemark{\synonymy@accenttext%
            {\textsuperscript{#1}}}}
    \@sidenotes@multimarker
}

%%%%%% Tables
%
% Use the booktabs package to print nice-looking tables.
\RequirePackage{longtable}
\RequirePackage{booktabs}


%%%%%% Tables and lists of contents, tables, figures, listings etc
%
% These are typeset in the accentcolour to stand out. Sections are upright and
% subsections are italicised and indented; seprate sections are spaced
% vertically. Similar for lists of tables, figure, and listings. No section numbers are
% set, as with titles below.
\RequirePackage[titles]{tocloft}
\RequirePackage{titletoc}
    \titlecontents{section}
        [0em]
        {}
        {}
        {}
        {\hspace{1em}\synonymy@accenttext{\contentspage}}
        [\addvspace{0.5\baselineskip}]
    \titlecontents{subsection}
        [2em]
        {\addvspace{-0.5\baselineskip}}
        {\itshape}
        {\itshape}
        {\hspace{1em}\synonymy@accenttext{\contentspage}}
        [\addvspace{0.5\baselineskip}]

%%%%%% Title formatting
%
% Tufte's style uses only the section and subsection headings, flush left and
% italicised. The main heading is larger but also italicised.
%
% Document title
\def\@maketitle{%
    \newpage
    \null
    {\noindent \itshape \LARGE \@title \par}%
    \vskip 1.5em%
    {\noindent \itshape \large \@author \par}%
    \vskip 1em%
    {\noindent \itshape \large \@date}%
    \par
    \vskip 1.5em%
}
% Section and subsection titles
\RequirePackage{titlesec}
    \titleformat{\section}{\Large\itshape}{}{0em}{}
    \titleformat{\subsection}{\large\itshape}{}{0em}{}

%%%%%% Captions
%
% Captions are printed at footnotesize with an accentcolour label and number.
% Additionally they can be printed in the margin alongside the figure, table,
% listing etc.
%\RequirePackage{caption}
%\DeclareCaptionFont{sidenotesize}{\synonymy@sidenotefontsize}
%\DeclareCaptionStyle{sidecaption}{%
%    font      = {sidenotesize,sf},
%    labelsep  = space,
%    labelfont = {color = synonymy@accentcolour}
%}
%\captionsetup{style = sidecaption}
%\DeclareCaptionStyle{marginfigure}{style = sidecaption}
%\DeclareCaptionStyle{margintable}{style = sidecaption}
%\DeclareCaptionStyle{widefigure}{style = sidecaption}
%\DeclareCaptionStyle{widetable}{style = sidecaption}

%%%%%% Headers and footers
%
% Headers and footers are simplified to show the document title in the header
% and current section and page in the footer.
\RequirePackage{fancyhdr}
    \pagestyle{fancy}
    \fancyhead[L,C,R]{}
    \fancyfoot[L,C,R]{}
    \fancyfoot[R]{\thepage}
\AtBeginDocument{
    \RenewDocumentCommand{\sectionmark}{m}{%
        \markboth{#1}{}}
    \fancyfoot[L]{\nouppercase{{\itshape\leftmark}}}
    \RenewDocumentCommand{\headrule}{}{}
    \let\runtitle\@title
    \rhead{\textallsc{\runtitle}}
}

%%%%%% Highlighted boxes
%
% These provide a little colour and emphasis on a piece of text, such as an
% example.
\RequirePackage[most]{tcolorbox}
\RequirePackage{tikz}
    \tcbuselibrary{skins,xparse}
% A box for examples with accentcolour bar on the left
% NB using xparse/expl3 requires replaceing spaces in keys with '~'
\ProvideTColorBox{examplebox}{}%
    {enhanced, frame~hidden, interior~hidden, borderline~west = {2pt}{2pt}{synonymy@accentcolour}, width = 44pc}

%%%%%% Abstract
%
% Environment for setting an abstract or beginning section.
% \RenewDocumentEnvironment{abstract}{ o }{%
%     % Environment for setting an abstract. The optional orgument specifies a
%     % title to be typeset.
% 	\small%
% 	\list{}{\rightmargin\parindent \leftmargin\parindent}\item[]
% 	\IfNoValueTF{#1}{}{\textallsc{#1}}%
% }{%
% 	\endlist%
% 	\vspace{\baselineskip} \par%
% }


%%% Versioning
%
% Records version and build numbers in an associated _version.dat_ file.
\RequirePackage{mVersion}
    \increaseBuild


%%% Synonymy-specific typesetting
%
% Each taxon consists of a species name with its LSID followed by a list of
% synonyms and references.
% Synonymy lists are typeset in a table to align the elements.
\setlength\LTpre{0.5\baselineskip}
\ProvideDocumentEnvironment{synonymy}
    {}%
    {
        \footnotesize
        \begin{longtable}[l]{@{\hspace{0em}}p{1.5em}@{\hspace{0.5em}}p{2.5em}@{\hspace{0.5em}}p{22em}@{\hspace{0.5em}}p{42em}}
    }%
    {
        \end{longtable}
    }
% LSID link 'buttons' are typeset with \lsid{urn} where there isn't enough space
% for the full URN itself.
\definecolor{lsid_link}{Hsb}{25, 0.8, 0.9}
\colorlet{lsid_link}[rgb]{lsid_link}
\ProvideDocumentCommand{\lsidlink}{ m }%
    {\sffamily\bfseries\footnotesize\href{http://zoobank.org/#1}{\textcolor{white}{\textallsc{LSID}}}}
\newtcbox{\lsidbox}{{/tcb/on~line}, colback=lsid_link, arc = 0.2em, left = -0.15em,
    right = -0.15em, top = -0.15em, bottom = -0.15em, boxrule = 0.0pt}
\ProvideDocumentCommand{\lsid}{ m }{\lsidbox{\lsidlink{#1}}}
\ProvideDocumentCommand{\lsidref}{ m }%
    {\href{http://zoobank.org/#1}{\textallsc{#1}}}
% A list of species gathers all taxa in the list into one single, easy to find
% place, with links to the fuller synonymy. Formatting takes after the lists
% above with titletoc.
\NewDocumentCommand{\listspeciesname}{}{{List~of~Species}}
\newlistof{species}{losp}{\listspeciesname}
% Set up a command for getting the species and author
% \species{Species name}{\cite{authoryear}}
\NewDocumentCommand{\species}{ m m }{%
    \refstepcounter{species}
    \par\noindent\emph{#1}~#2
    \addcontentsline{losp}{species}{\protect{#1}}\par%
}
\cftsetindents{species}{0em}{0em}
% Use three columns
\RenewDocumentCommand{\cftlospprehook}{}{%
    \addcontentsline{toc}{section}{\listspeciesname}
    \begin{fullwidth}%
    \begin{multicols}{3}%
}
\RenewDocumentCommand{\cftlospposthook}{}{%
    \end{multicols}%
    \end{fullwidth}
}
% Use titletoc to format: make names italic and footnotesize
\contentsuse{species}{losp}
\makeatletter
\titlecontents{species}
    [0em]
    {\addvspace{-0.5\baselineskip}}
    {\footnotesize\itshape}
    {\footnotesize\itshape}
    {\footnotesize\hspace{1em}\synonymy@accenttext{\contentspage}}
\makeatother
% These commands attempt to set up dictionary-like footers for the synonymy to
% show the first and last taxon on the page.
    % \fancyfoot[L]{\nouppercase{{\small\itshape\rightmark–\leftmark}}}
% single section in references
% \AtBeginBibliography{
%     \fancyfoot[L]{\nouppercase{{\itshape\leftmark}}}
% }
% these synonymy-specific citation commands sort out which ones should have
% author names, years, parentheses etc.
\ProvideDocumentCommand{\cauth}{ m }{\cite{#1}}
\ProvideDocumentCommand{\crefauth}{ m }{\citeauthor{#1}}
\ProvideDocumentCommand{\pauth}{ m }{\parencite{#1}}
\ProvideDocumentCommand{\cyear}{ m }{\cite*{#1}}
\ProvideDocumentCommand{\pyear}{ m }{\parencite*{#1}}
\ProvideDocumentCommand{\emyear}{ m }{\emph{\cite*{#1}}}
\ProvideDocumentCommand{\cauthyr}{ m }{\cite{#1}}
\ProvideDocumentCommand{\pauthyr}{ m }{\parencite{#1}}


%%% Bibliography
%
% Tufte's books usually have extensive citations within the margin notes. With
% the number of citations include, this doesn't really work well – a page of
% citations will likely spill over to the next, and the next… Equally formatting
% for ICZN rules suggests just the author and year, thus I use this style for
% citation.
%
% I have modified the bibliography, however, to suit my preferences. Author
% names are in small caps, DOIs included, and a few other bits and bobs too.
\RequirePackage[%
    style          = authoryear-comp,
    sortlocale     = auto,
    autocite       = footnote,
    terseinits     = true,
    maxbibnames    = 100,
    maxcitenames   = 2,
    minnames       = 1,
    uniquename     = false,
    uniquelist     = false,
    giveninits     = true,
    alldates       = year,
    labeldateparts = true,
    dashed         = true,
    url            = false,
    isbn           = false,
    mergedate      = maximum,
    hyperref       = auto,
    sorting        = dateauthor%
]{biblatex}

%%%%%% Bibliography formatting
%
% These control the fonts and setting of the whole bibliography. Use a small
% sans serif font, typset URLs in code font, use three columns.
\RenewDocumentCommand{\bibfont}{}{\small\sffamily}
\RenewDocumentCommand{\UrlFont}{}{\small\ttfamily\addfontfeatures{Numbers=Lowercase}}
% Use three columns with no right margin par.
\ProvideDocumentCommand{\mywidebib}{}{
	\newgeometry{left = 3pc, right = 3pc, textwidth = 44pc, top = 4pc, textheight = 60pc, nomarginpar}
	\begin{multicols}{3}[\printbibheading]
		\newrefcontext[sorting=authordate]
		\addcontentsline{toc}{section}{References}
		\printbibliography[heading=none]
	\end{multicols}
	\restoregeometry
}

%%%%%% Sorting
%
% I have defined the following sort scheme, similar to that used by
% _Palaeontology_:
%
% 1. Sort by first author surname,
% 2. Group into single author, two authors, three or more author groupings,
% 3. Order each grouping by date published.
%
% This is achieved using a source map to count the number of 'and's between
% authors, and group by those.
\DeclareStyleSourcemap{
    \maps[datatype=bibtex]{
        \map{
            \step[fieldsource=author]%, match=\regexp{(.+)\sand}, final]
            \step[fieldset=sortname, origfieldval]% fieldvalue=$1, final]  
            \step[fieldsource=sortname, match=\regexp{\sand\s.+}, replace=\regexp{}]
        }
        \map{
            \step[fieldsource=author]
            \step[fieldset=usera, origfieldval]
            \step[fieldsource=usera, match=\regexp{.+?\sand\s}, replace=\regexp{and}]
            \step[fieldsource=usera, match=\regexp{((?:and)*).+}, replace=\regexp{and$1}]
            \step[fieldsource=usera, match=\regexp{(andandand).+}, replace=\regexp{andandand}]
        }
    }}
% Multiple citations are sorted first by date then grouped by author.
\DeclareSortingTemplate{dateauthor}{
    \sort{
	    \field{presort}
    }
    \sort[final]{
	    \field{sortkey}
    }
    \sort{
	    \field{year}
    }
    \sort{
	    \field{month}
    }
    \sort{
	    \field{day}
    }
    \sort[direction=ascending]{
	    \field{sortname}
	    \field{author}
	    \field{editor}
	    \field{translator}		
    }
}
% Bibliography is sorted by first author, number of authors, date published.
\DeclareSortingTemplate{authordate}{
    \sort{
	    \field{presort}
    }
    \sort[final]{
	    \field{sortkey}
    }
    \sort[direction=ascending]{
	    \field{sortname}
	    \field{author}
	    \field{editor}
	    \field{translator}
    }
    \sort{
	    \field{usera}
    }
    \sort{
	    \field{year}
    }
    \sort{
	    \field{month}
    }
    \sort{
	    \field{day}
    }
}

%%%%%% Item formatting
%
% These are slightly modified from the default. all authors are gien as family,
% given.
\DeclareNameAlias{sortname}{family-given}
% Article:
% Author, A. 2021. Title, \emph{Journal}, \textbf{volume}, pages. doi
\DeclareBibliographyDriver{article}{%
    \usebibmacro{author}%
    \newunit%
    \printfield{title}%
    \newunit\newblock%
    \usebibmacro{journal+issuetitle}%
    \newunit\newblock%
    \printfield{doi}
    \newblock
    \usebibmacro{pageref}%
    \usebibmacro{finentry}%
}
% Memoir (e.g. article in names issue):
% Author, A. 2021. Title, pages. In Issuetitle, by Editor, E. Journal, Vol,
% page. DOI
\DeclareBibliographyDriver{memoir}{%
    \usebibmacro{author}%
    \newunit%
    \printfield{title}%
    \newunit\newblock%
    \printfield{pages}%
    \newunit\newblock%
    \usebibmacro{in:}%
    \printfield{maintitle}%
    \newunit\newblock%
    \usebibmacro{byeditor+others}%
    \usebibmacro{journal+issuetitle}%
    \newunit\newblock%
    \printfield{doi}%
    \newblock%
    \usebibmacro{pageref}%
    \usebibmacro{finentry}%
}
% Inbook:
% Author, A. 2021. Chapter, pages. In booktitle, by Editor, E. Publisher,
% Location. DOI
\DeclareBibliographyDriver{inbook}{%
    \usebibmacro{author}%
    \newunit%
    \printfield{title}%
    \newunit\newblock%
    \printfield{pages}%
    \newunit\newblock%
    \usebibmacro{in:}%
    \printfield{booktitle}%
    \newunit\newblock%
    \usebibmacro{byeditor+others}%
    \newunit\newblock%
    \usebibmacro{publisher}%
    \newunit\newblock%
    \printfield{doi}%
    \newblock%
    \usebibmacro{pageref}%
    \usebibmacro{finentry}%
}
% Incollection:
% Author, A. 2021. Title, pages. In booktitle, by Editor, E. Publisher. DOI
\DeclareBibliographyDriver{incollection}{%
    \usebibmacro{author}%
    \newunit%
    \printfield{title}%
    \newunit\newblock%
    \printfield{pages}%
    \newunit\newblock%
    \usebibmacro{in:}%
    \printfield{booktitle}%
    \newunit\newblock%
    \usebibmacro{byeditor+others}%
    \newunit\newblock%
    \usebibmacro{publisher}%
    \newunit\newblock%
    \printfield{doi}%
    \newblock%
    \usebibmacro{pageref}%
    \usebibmacro{finentry}%
}

%%%%%% Element formatting
%
% These commands format individual elements within each bibliography item.
% Make titles sentence case, without quotes
\DeclareFieldFormat[%
    article,
    inbook,
    incollection,
    inproceedings,
    patent,
    thesis,
    unpublished%
]{title}{\MakeSentenceCase*{#1\addperiod}}
\DeclareFieldFormat[%
    article,
    inbook,
	incollection,
	inproceedings,
	patent,
	thesis,
	unpublished%
]{titlecase}{\MakeSentenceCase*{#1}}
% Italic book and thesis titles
\DeclareFieldFormat[book,thesis]{title}{\itshape #1\addperiod}
% Roman memoir titles
\DeclareFieldFormat[memoir]{title}{\textup{#1}}
% Boldface volume
\DeclareFieldFormat[article,memoir]{volume}{\textbf{#1}}
\DeclareFieldFormat[book,incollection]{volume}{\textbf{\addfontfeature{Numbers=Uppercase}#1}}
% Uppercase numbers for year after author
\DeclareFieldFormat{date}{%
    {\addfontfeatures{Numbers={Uppercase,Proportional}}#1}%
}
% italic extradate
\DeclareFieldFormat*{extradate}{\itshape\mknumalph{#1}}
% No parentheses around date
\DeclareFieldFormat{parens}{#1}
% Roman page numbers
\DeclareFieldFormat[article,memoir,incollection]{pages}{#1}
% Separators
\RenewDocumentCommand{\bibnamedelimi}{}{} % no space between initials
\RenewDocumentCommand{\bibnamedelimc}{}{~} % space between prefix (von) and surname
\RenewDocumentCommand{\bibinitperiod}{}{.} % full stop after initial
\RenewDocumentCommand{\bibinitdelim}{}{} % no spacing between initials
\RenewDocumentCommand{\bibinithyphendelim}{}{{\addfontfeature{Letters=Uppercase} .-}} % hyphen between initials
\RenewDocumentCommand{\bibnamedash}{}{———} % replace repeated authors dash
\RenewDocumentCommand{\multinamedelim}{}{\addcomma\addspace} % comma-space between names
\RenewDocumentCommand{\finalnamedelim}{}{\addspace\textcaps{\&}\addspace} % space-&-space before last name
\RenewDocumentCommand{\nameyeardelim}{}{{,~}} % comma-space between name & year
\RenewDocumentCommand{\revsdnamepunct}{}{,~} % space between surname & forename
\RenewDocumentCommand{\intitlepunct}{}{~} % space after ‘in’ in bibliography
\RenewDocumentCommand{\mkbibnamefamily}{ m }{% make last names small caps
    \ifmknamesc{\textsc{#1}}{#1}}
\RenewDocumentCommand{\mkbibnameprefix}{ m }{% small cap name prefix
    \ifboolexpr{ test {\ifmknamesc} and test {\ifuseprefix} }
        {\textsc{#1}}
        {#1}}
% Make author and editor names small caps
\def\ifmknamesc{%
    \ifboolexpr{ ( test {\ifbibliography} or test {\ifbool{citetracker}} )
        and ( test {\ifcurrentname{labelname}}
            or test {\ifcurrentname{author}}
            or ( test {\ifnameundef{author}}
                and test {\ifcurrentname{editor}} ) ) }}

%%%%%% Macro formatting
%
% These are new of modified macros that go into the above drivers.
% Family, given naming
\renewbibmacro*{cite:full}{%
    \usebibmacro{cite:full:citepages}%
    \printtext[bibhypertarget]{%
        \usedriver
        {}
        {\thefield{entrytype}}}%
    \usebibmacro{shorthandintro}}
% Set et al. in italics
\renewbibmacro*{name:andothers}{% Based on name:andothers from biblatex.def
    \ifboolexpr{
        test {\ifnumequal{\value{listcount}}{\value{liststop}}}
        and
        test \ifmorenames
    }
    {\ifnumgreater{\value{liststop}}{1}
        {\finalandcomma}
        {}%
        \andothersdelim\bibstring[\emph]{andothers}}
    {}}
% Italic journal titles
\renewbibmacro*{journal}{%
    \iffieldundef{journaltitle}
        {}
        {\printtext[journaltitle]{%
            \printfield[noformat]{journaltitle}%
            \setunit{\subtitlepunct}%
            \printfield[noformat]{journalsubtitle}}}}
% join journal, volume, pages together
\renewbibmacro*{journal+issuetitle}{%
    \usebibmacro{journal}%
    \setunit{\addcomma\addspace}%
    \printfield{volume}%
    \setunit{\addcomma\space}%
    \printfield{pages}%
    \newunit}
% Typset publisher: address
\newbibmacro*{publisher}{%
    \printfield{publisher}%
    \setunit{\addcolon\addspace}%
    \printfield{address}%
    \newunit}


%%% Cross referencing and links
%
% I use _hyperref_ to create links to sections and references within the PDF and
% to URLs outside. These are coloured according the colours defined above. As it
% changes lots of things in other packages, _hyperref_ should go last.
\RequirePackage[%
    colorlinks = true,
    breaklinks = true,
    citecolor  = citelinkcolour,
    urlcolor   = urllinkcolour 
]{hyperref}

\ExplSyntaxOff
