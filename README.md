# PsychoPy-To-Medina converter (+ filter and anonymizer)
This quick-and-dirty (fairly quick, horribly dirty) script converts the output of PsychoPy experiments to input for my script to create a Medina (2007)-style Stochastic OT model. I wrote this program for the purposes of my PhD thesis about a StOT model of object drop, but it can easily be adapted to your needs.

## Getting started
The script should run on Python 3 and does not have to be installed. Runs fine on Python 3.9.4 in Ubuntu 21.04.

### Prerequisites
You need the following packages to make the script work:

    argparse
    collections
    pandas
    numpy
    
To install these packages in Python 3, make sure you have installed pip3 and run:

    pip3 install <package>

## Running the script
Make sure you have the script and the input files within the same folder before starting.

### Parameters
To run the script, simply run this command from the terminal in the folder containing both the script and the input files:

    python3 inspectLikert_share.py

You may pass an optional parameter to the script:

    --language, -l:        target language of Likert experiment

The default language tag is "eng" for English. You may use whichever tag(s) you want, if you run the same experiment on multiple languages! Just make sure the language tag you use as a parameter for the script is exactly the same you used in your input file names (see below).

### Input files
The script requires two input files:
* `original_[LANGUAGE-TAG].csv` contains the output of your PsychoPy experiment run on Pavlovia (i.e. the scores provided by each participant, plus all other information, as yielded by the platform). For English, the file is named `original_eng.csv`
* `info_verbs_[LANGUAGE-TAG].csv` contains relevant information you may need to add to the original PsychoPy dataframe (i.e. aspectual verb features). For English, the file is named `info_verbs_eng.csv`

The file `original_[LANGUAGE-TAG].csv` is a large comma-separated file with headers automatically created by PsychoPy when you run your experiment on Pavlovia (or locally). It contains a variable number of columns (~50) depending on where you distributed the experiment (Prolific, social media, email link...). It looks something like this:

| study_id | participant | slider.response | ... |
|-|-|-|-|
| 1 | fancyname | 7 | ... |
| 1 | fancyname | 7 | ... |
| 1 | fancyname | 2 | ... |

The file `info_verbs_[LANGUAGE-TAG].csv` is a small comma-separated file with headers containing any information about your verbs that you want to add to the results dataframe in order to consider them in your linguistic model of object drop. In my case, it looks something like this:

| verb | ita | mannspec | telicity |
|-|-|-|-|
| break | rompere | no | yes |
| build | costruire | no | yes |
| chop | spaccare | yes | yes |

### Preprocessing
In converting your PsychoPy output to Medina-like input, the script takes care of three possible issues:
* DE-DUPLICATION. Judgments are, of course, linked to the participant providing them. In order to avoid problems created by duplicate participant names, the script considers the completion timestamp as a participant name instead of the nicknames they inserted in the Pavlovia/PsychoPy interface. Comment out line 34 if you are not interested in this feature.
* FILTERING. It's possible that, despite being instructed otherwise, your participants ignored the full 7-point Likert scale and just provided extreme, binary judgments (i.e. 1 or 7). If this is something you DON'T want to happen to your experiment, the script finds the culprits, counts them, informs you in the terminal standard output, and removes them from further computation (and from the output!). If you don't care for this filter, just comment out lines 36 to 45.
* ANONYMIZATION. By default, the script renames all participants by assigning them an ordinal number (i.e. "part1, "part2"...), so that the output file you will use as input to the Medina-like script contains neither the participant nicknames nor their completion timestamps. If you are not interested in this feature, comment out line 88 and un-comment line 77

## Output files
The script yields some byproduct outputs you can delete (names start with two underscores), and the real output file you need, named `medina_likert_[LANGUAGE-TAG].csv`. This output file contains headed, tab-separated judgment files having the following columns (not necessarily in this order):

* `verb`: verb names
* `sentence`: sentence type based on experimental setting, may take the following values
    * `target`: verbs of interest, no object
    * `control`: verbs of interest, overt object
    * `filler_no`: intransitive verbs, no object
    * `filler_dobj`: intransitive verbs, overt object
* `telicity`: verb telicity, may be either "telic" or "atelic"
* `perfectivity`: sentence perfectivity, may be either "perf" or "imperf"
* `part1, part2, part3... partN`: a column for each participant to the experiment, numbered progressively, containing their raw Likert-scale judgments. This script has been tested on 7-point Likert judgments, but it will work with any Likert scale you choose.
* `iterativity`: sentence iterativity, may be either "iter" or "noiter" (OPTIONAL to run `optimizeMedinaBasic.py`)
* `mannspec`: verb manner specification, may be either "spec" or "nospec" (OPTIONAL to run `optimizeMedinaExtended1.py`)

For instance, your output file will be shaped like this:

verb | sentence | telicity | perfectivity | iterativity | mannspec | s1 | s2 | s3
|-|-|-|-|-|-|-|-|-|
eat | target | atelic | perf | iter | nospec | 4 | 5 | 4
eat | target | atelic | imperf | iter | nospec | 6 | 6 | 7
kill | target | telic | perf | iter | nospec | 2 | 3 | 2
kill | target | telic | imperf | iter | nospec | 5 | 4 | 5

## License
This project is licensed under the MIT License. May it provide optimal input for all your experimenting needs :mortar_board:

## References
* Medina, Tamara Nicol (2007). Learning which verbs allow object omission: verb semantic selectivity and the implicit object construction (PhD dissertation, Johns Hopkins University).
* Kim, Najoung; Rawlins, Kyle; Smolensky, Paul (2019). "The complement-adjunct distinction as gradient blends: the case of English prepositional phrases", [lingbuzz/004723](https://ling.auf.net/lingbuzz/004723)

## Acknowledgments
Many thanks to 
* @ellepannitto, my Python fairy
* @najoungkim, for sharing references that ultimately led to my PhD project
* the Stack Overflow community, for the many code snippets that saved me from frustration
