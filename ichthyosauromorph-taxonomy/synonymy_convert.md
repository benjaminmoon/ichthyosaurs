---
---

```
$assignment_confidence & $reference$year & \emph{$given_species} {$given_authority$author^($given_authority$author):availability}; {p^pp:ranges} $pageref{ [{$bed}{, $member}{, $formation }({$stage}{, $series}{, $system}); {$location}{ , $country}{ ($utm{ = $latitude $longittude})}]}. $comments.
```

NB

* Dollar signs ("\$") indicate field values and subsets of those, similar to R.
* Braces ("{", "}") are used to show which parts are kept together.
* A caret ("^") is used to show alternatives, e.g. for plurals.
    - Colons indicate the use change.

# Column Descriptions

## ichthyosauromorph-species.tsv ##

* accepted_name
    - The currently valid name accepted according to ICZN rules.
* accepted_authority
    - The naming authority of the accepted name.
* accepted_status
    - Indicates whether this is an original or new combination (parenthesised).
    - avail: available
        + The original name as available following ICZN rules.
    - ncomb: new combination
        + A new combination of species name into a different genus from the
        original. The authority name is surrounded in parentheses.

## ichthyosauromorph-synonymy.tsv ##

* reference
    - The occurrence reference BibLaTeX key.
* pageref
    - The page in \$reference that the name in first mentioned on, or a range of
    pages.
* identified_name, identified_authority
    - The name and author of the species as given in \$reference.
* identified_status, accepted_status
    - The validity status of the species. This decides whether the authority
    name should be included in parentheses.
    - avail: available 
        + The original name as made available following ICZN rules.
        + E.g., _Ophthalmosaurus icenicus_ @Seeley1874QGJS.
    - ncomb: new combination
        + The species is valid but included under a different generic name from
        the original.
        + E.g., _Cryopterygius kielanae_ @Tyborowski2016APP recombined as
        _Undorosaurus kielanae_  [@Tyborowski2016APP].
        + Authority name is included in parentheses.
* assignment_confidence
    - Symbols from @Matthews1973P to indicate certainty in the occurrence
    assignment to the valid taxon.
    - "\*": valid according to the rules of the ICZN.
    - ".": we accept responsibility for assigning this reference.
    - "" (no sign): we have no right to assign this reference, but no reason to
    doubt it.
    - "?": the assignment of this reference is subject to doubt.
    - "(?)": this reference probably applies, but the material, description
    or illustrations cannot be checked to confirm this.
    - "p" (_partim_): only part of the material in this reference can be
    assigned.
* morphological_information
    - Does this reference contain useful morphological data?
    - "Y": yes it does.
    - "N": no, it can be skipped by those looking for morphology. The year of
    the reference is printed in italics.
* accepted_name
    - The currently valid name for this synonym
* formation, member, bed; stage, series, system
    - Lithostratigraphical occurrence information.
* locality, country, utm, latitude, longitude
    - Geographical occurrence information.
    - UTM location (WGS84) is preferred over just latitude and longitude.
* comments
    - Additional comments to include at the end of the reference.
