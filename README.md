# LCards #


## Description ##
This script helps prepare data to language cards. It gets directory with text files and returns list of words, used in files. Script counts frequency of each word's usage and adds translation. Script uses [Yanded.Dictionary API](http://api.yandex.ru/dictionary) for words translation.


## Requirments ##
1. Installed `Python` => 2.7
2. Installed `requests` python module


## Usage ##
`python lcards.py`

Arguments:

`-h`
Show help.

`-i` , `--input`
Directory with source text files. Default is `./input`.

`-o` , `--output`
Output file. Result will be displayed on screen by default.

`-e` , `--exceptions`
File with words list to be excluded from result. Each word must be in new line.

`-tk` ,  `--translate_key`
Yandex.Dictionary API key. You can get it [here](http://api.yandex.ru/key/form.xml?service=dict) for free. Words will not be translated by default.

`-tl` , `--translate_lang`
Translation direction. You can get list of available directions [here](http://api.yandex.ru/dictionary/doc/dg/reference/getLangs.xml). EN-RU used by default.

`-trp` , `--trim_by_percent`
Trim results by percent of words' usage in text.
 
`-trf` , `--trim_by_freq`
Trim results by frequency of words' usage in text.

`-trn` , `--trinm_by_number`
Trim results by number of first most used words.


## Changelog ##
`0.0.1` 
: Initial
