<!--
SPDX-FileCopyrightText: 2023 hugues de keyzer

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# tabeltekstilo

tabeltekstilo is a multi-purpose tool for manipulating text in tabular data format.

## introduction

text in tabular data format is text formatted as a table (usually stored as a spreadsheet file), where each row of the table contains one word of the text.
one column contains the actual word as it appears in the text, while other columns may contain more information about the word, like the page and line number where it appears, a cleaned-up form (with uniform casing and no punctuation), its lemma, its grammatical category,…

from text in that format, tabeltekstilo can generate:

*   an alphabetical dictionary by aggregating columns
*   an alphabetical index (like the ones that appear at the end of books)
*   an xml file

see [the examples section](#examples) below for concrete examples.

## features

general features:

*   alphabetical sorting using the unicode collation algorithm
*   right-to-left text support

dictionary features:

*   dictionary generation
*   multiple column aggregation with custom join string

index features:

*   multi-level index generation
*   multiple values in parent columns support for agglutinated forms
*   multiple reference support (for example: page, line)
*   grouping of identical references with count
*   total count of form occurrences at each parent level
*   filtering with regular expressions

xml features:

*   nesting of forms under multiple levels of parent columns
*   custom attributes on form elements
*   custom root element
*   optional header with custom copyright and licensing information

## usage

tabeltekstilo takes a subcommand, an input filename and an output filename as arguments, as well as some options.
input and output files should be in opendocument (.ods) or office open xml (.xlsx) format.

### dictionary

the minimal usage is:

```
tabeltekstilo dictionary --form-col form --agg-col agg input.ods output.ods
```
where `form` is title of the column (in `input.ods`) that contains the form that will appear in the dictionary and `agg` is the title of the column (in `input.ods`) that contains the values to aggregate next to the form.

to display a full description of the usage syntax:

```
tabeltekstilo dictionary --help
```

### index

the minimal usage is:

```
tabeltekstilo index --ref-col ref --form-col form input.ods output.ods
```
where `ref` is the title of the column (in `input.ods`) that contains the reference to use in the index (the page number, for example) and `form` is title of the column (in `input.ods`) that contains the form that will appear in the index.

to display a full description of the usage syntax:

```
tabeltekstilo index --help
```

### xml

the minimal usage is:

```
tabeltekstilo xml input.ods output.xml
```
where `input.ods` is the input file and `output.xml` the output file to generate.

to display a full description of the usage syntax:

```
tabeltekstilo xml --help
```

## examples

### dictionary

let’s take the following example text:

> le reste des avions vola vers l’est. nous avions du retard. c’est ce qu’il reste des vers à propos des vers.

it must first be converted to this format as `input.ods`:

| word    | form   | lemma      | type         |
| ------- | ------ | ---------- | ------------ |
| le      | le     | le (la)    | det_art      |
| reste   | reste  | reste      | noun         |
| des     | des    | de+le (la) | prep+det_art |
| avions  | avions | avion      | noun         |
| vola    | vola   | voler      | verb         |
| vers    | vers   | vers       | prep         |
| l’      | l’     | le (la)    | det_art      |
| est.    | est    | est        | noun         |
| nous    | nous   | nous       | pro_per      |
| avions  | avions | avoir      | verb         |
| du      | du     | de+le (la) | prep+det_art |
| retard. | retard | retard     | noun         |
| c’      | c’     | ce         | pro_dem      |
| est     | est    | être       | verb         |
| ce      | ce     | ce         | pro_dem      |
| qu’     | qu’    | que        | conjs        |
| il      | il     | il         | pro_per      |
| reste   | reste  | rester     | verb         |
| des     | des    | de+le (la) | prep+det_art |
| vers    | vers   | vers       | noun         |
| à       | à      | à          | prep         |
| propos  | propos | propos     | noun         |
| des     | des    | de+le (la) | prep+det_art |
| vers.   | vers   | ver        | noun         |

now, let’s generate the dictionary by calling:

```
tabeltekstilo dictionary --form-col form --agg-col lemma --agg-col type input.ods output.ods
```

this will generate the following table as `output.ods`:

|    | form   | lemma           | type             |
| -- | ------ | --------------- | ---------------- |
| 0  | à      | à               | prep             |
| 1  | avions | avion; avoir    | noun; verb       |
| 2  | c’     | ce              | pro_dem          |
| 3  | ce     | ce              | pro_dem          |
| 4  | des    | de+le (la)      | prep+det_art     |
| 5  | du     | de+le (la)      | prep+det_art     |
| 6  | est    | est; être       | noun; verb       |
| 7  | il     | il              | pro_per          |
| 8  | l’     | le (la)         | det_art          |
| 9  | le     | le (la)         | det_art          |
| 10 | nous   | nous            | pro_per          |
| 11 | propos | propos          | noun             |
| 12 | qu’    | que             | conjs            |
| 13 | reste  | reste; rester   | noun; verb       |
| 14 | retard | retard          | noun             |
| 15 | vers   | ver; vers; vers | noun; noun; prep |
| 16 | vola   | voler           | verb             |

### index

let’s take the following example text, and say that it appears on line 1 and 2 of page 42:

> la suno brilas hodiaŭ. hieraŭ estis malvarme, sed hodiaŭ estas varme.<br>
> ni estas bonŝancaj!

it must first be converted to this format as `input.ods`:

| page | line | word       | form      | lemma      |
| ---- | ---- | ---------- | --------- | ---------- |
| 42   | 1    | la         | la        | la         |
| 42   | 1    | suno       | suno      | suno       |
| 42   | 1    | brilas     | brilas    | brili      |
| 42   | 1    | hodiaŭ.    | hodiaŭ    | hodiaŭ     |
| 42   | 1    | hieraŭ     | hieraŭ    | hieraŭ     |
| 42   | 1    | estis      | estis     | esti       |
| 42   | 1    | malvarme,  | malvarme  | varma      |
| 42   | 1    | sed        | sed       | sed        |
| 42   | 1    | hodiaŭ     | hodiaŭ    | hodiaŭ     |
| 42   | 1    | estas      | estas     | esti       |
| 42   | 1    | varme.     | varme     | varma      |
| 42   | 2    | ni         | ni        | ni         |
| 42   | 2    | estas      | estas     | esti       |
| 42   | 2    | bonŝancaj! | bonŝancaj | bona+ŝanco |

now, let’s generate the index by calling:

```
tabeltekstilo index --ref-col page --ref-col line --parent-col lemma --form-col form --split-char + input.ods output.ods
```

this will generate the following table as `output.ods`:

|    | lemma_count | lemma  | form_count | form      | refs         |
| -- | ----------- | ------ | ---------- | --------- | ------------ |
| 0  | 1           | bona   | 1          | bonŝancaj | 42, 2        |
| 1  | 1           | brili  | 1          | brilas    | 42, 1        |
| 2  | 3           | esti   | 2          | estas     | 42, 1; 42, 2 |
| 3  |             |        | 1          | estis     | 42, 1        |
| 4  | 1           | hieraŭ | 1          | hieraŭ    | 42, 1        |
| 5  | 2           | hodiaŭ | 2          | hodiaŭ    | 42, 1 (2)    |
| 6  | 1           | la     | 1          | la        | 42, 1        |
| 7  | 1           | ni     | 1          | ni        | 42, 2        |
| 8  | 1           | ŝanco  | 1          | bonŝancaj | 42, 2        |
| 9  | 1           | sed    | 1          | sed       | 42, 1        |
| 10 | 1           | suno   | 1          | suno      | 42, 1        |
| 11 | 2           | varma  | 1          | malvarme  | 42, 1        |
| 12 |             |        | 1          | varme     | 42, 1        |

note that “bonŝancaj” appears twice in the index, once under the form “bona” and once under the form “ŝanco”.
this is because the lemma column contained two values, separated by the defined split character.

note that the word “hodiaŭ” appears twice on the same line.
this is why its reference has “(2)” appended to it.

#### filtering

the tabeltekstilo index function allows to filter rows based on column values using regular expressions.

for example, using the same input file as in the previous example, let’s say that only noun lemmas should appear.
in this case, they all end with “o”, so this command can be used:

```
tabeltekstilo index --ref-col page --ref-col line --parent-col lemma --form-col form --split-char + --filter "lemma:.*o" input.ods output.ods
```

in this example, the argument is quoted to avoid the `*` character to be interpreted by the shell.
this depends on the shell used.

this will generate the following table:

|   | lemma_count | lemma | form_count | form      | refs  |
| - | ----------- | ----- | ---------- | --------- | ----- |
| 0 | 1           | ŝanco | 1          | bonŝancaj | 42, 2 |
| 1 | 1           | suno  | 1          | suno      | 42, 1 |

note that “bonŝancaj” appears only once in this case, because the lemma “bona” was filtered out.

multiple filter arguments may be used.
the format of the filter expressions is `col:regex`, where `col` is a column name and `regex` is a regular expression matching the value (after splitting).
any column of the input table can be used, even those not used by the index.

by default, filtering is inclusive, which means that at least one expression should match for the row to be included.
this behavior can be reversed with `--filter-exclude`.
in this case, any row matching an expression is excluded; only the rows not matching any of the expressions are included.

for example, still using the same input file, let’s say that forms with less than 4 letters should be excluded.
this command can be used:

```
tabeltekstilo index --ref-col page --ref-col line --parent-col lemma --form-col form --split-char + --filter "form:.{1,3}" --filter-exclude input.ods output.ods
```

this will generate the following table:

|   | lemma_count | lemma  | form_count | form      | refs         |
| - | ----------- | ------ | ---------- | --------- | ------------ |
| 0 | 1           | bona   | 1          | bonŝancaj | 42, 2        |
| 1 | 1           | brili  | 1          | brilas    | 42, 1        |
| 2 | 3           | esti   | 2          | estas     | 42, 1; 42, 2 |
| 3 |             |        | 1          | estis     | 42, 1        |
| 4 | 1           | hieraŭ | 1          | hieraŭ    | 42, 1        |
| 5 | 2           | hodiaŭ | 2          | hodiaŭ    | 42, 1 (2)    |
| 6 | 1           | ŝanco  | 1          | bonŝancaj | 42, 2        |
| 7 | 1           | suno   | 1          | suno      | 42, 1        |
| 8 | 2           | varma  | 1          | malvarme  | 42, 1        |
| 9 |             |        | 1          | varme     | 42, 1        |

tabeltekstilo uses python’s regular expressions.
their documentation is [here](https://docs.python.org/3/library/re.html).

### xml

let’s take the table from the index command example, but change it slightly by renaming the first 2 columns and putting the word column last :

| page p | line l | form      | lemma      | word       |
| ------ | ------ | --------- | ---------- | ---------- |
| 42     | 1      | la        | la         | la         |
| 42     | 1      | suno      | suno       | suno       |
| 42     | 1      | brilas    | brili      | brilas     |
| 42     | 1      | hodiaŭ    | hodiaŭ     | hodiaŭ.    |
| 42     | 1      | hieraŭ    | hieraŭ     | hieraŭ     |
| 42     | 1      | estis     | esti       | estis      |
| 42     | 1      | malvarme  | varma      | malvarme,  |
| 42     | 1      | sed       | sed        | sed        |
| 42     | 1      | hodiaŭ    | hodiaŭ     | hodiaŭ     |
| 42     | 1      | estas     | esti       | estas      |
| 42     | 1      | varme     | varma      | varme.     |
| 42     | 2      | ni        | ni         | ni         |
| 42     | 2      | estas     | esti       | estas      |
| 42     | 2      | bonŝancaj | bona+ŝanco | bonŝancaj! |

now, let’s generate the xml file by calling:

```
tabeltekstilo xml input.ods output.xml
```

this will generate the following file as `output.xml`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<document>
  <page p="42">
    <line l="1">
      <word form="la" lemma="la">la</word>
      <word form="suno" lemma="suno">suno</word>
      <word form="brilas" lemma="brili">brilas</word>
      <word form="hodiaŭ" lemma="hodiaŭ">hodiaŭ.</word>
      <word form="hieraŭ" lemma="hieraŭ">hieraŭ</word>
      <word form="estis" lemma="esti">estis</word>
      <word form="malvarme" lemma="varma">malvarme,</word>
      <word form="sed" lemma="sed">sed</word>
      <word form="hodiaŭ" lemma="hodiaŭ">hodiaŭ</word>
      <word form="estas" lemma="esti">estas</word>
      <word form="varme" lemma="varma">varme.</word>
    </line>
    <line l="2">
      <word form="ni" lemma="ni">ni</word>
      <word form="estas" lemma="esti">estas</word>
      <word form="bonŝancaj" lemma="bona+ŝanco">bonŝancaj!</word>
    </line>
  </page>
</document>
```

the parent columns are identified by the fact that they contain a space character which separates the element name from the attribute name.

the last column is used as the deepest element, with all non-parent columns before it used as attributes.

## credits

This development was funded by Bastien Kindt for the GREgORI Project.<br>
<https://uclouvain.be/fr/instituts-recherche/incal/ciol/gregori-project.html><br>
<https://www.v2.gregoriproject.com/><br>
with financial support from<br>
INCAL - Institut des civilisations, arts et lettres<br>
<https://uclouvain.be/fr/instituts-recherche/incal><br>
CIOL - Centre d'études orientales - Institut orientaliste de Louvain<br>
<https://uclouvain.be/fr/instituts-recherche/incal/ciol>
