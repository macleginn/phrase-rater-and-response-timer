phrase-rater-and-response-timer
===============================

A small gui script for conducting linguistic interviews of
a certain type. Reads phrases separated by linebreaks from 
a file whose name is given as the sole command-line argument.
A file could like this:
```
Phrase 1.
Phrase 2.
Phrase 3.
```
Processing times for phrases and ratings are written out to
a file in the same directory with the time of the end of the interview as a name.

Written in Python 3.4 using Tkinter (i.e., does not use any external libraries).

Usage:

~ $ python3 phraseRater.py [yourfilename]
