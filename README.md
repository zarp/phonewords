The main script (Phoneword_generator.py) implements the following functions:

● number_to_words(), which takes as an argument a string representing a US phone
number and which outputs a string which has transformed part or all of the phone
number into a single "wordified" phone number that can be typed on a US telephone (for
example, a valid output of number_to_words("1-800-724-6837") could be
"1-800-PAINTER").

● words_to_number(), which does the reverse of the above function (for example, the
output of words_to_number("1-800-PAINTER") should be "1-800-724-6837")

● all_wordifications(), which outputs all possible combinations of numbers and English
words in a phone number.

In addition to the main .py file this repo contains Jupyter notebook which has some additional information: usage examples, additional comments, etc.
