# SpUncommonFinder
<b>Finds uncommon Spanish words and outputs to them to a .csv. Also can be used to check for unique words to given list of known words that you might already know/ are studding.</b>

## Requirements
- Python (at least version 3.9.6)
- NLTK library
- NLTK cess_esp corpora
- NLTK punkt
- (set_up.bat file provided for easier installation)

## Idea

New words are always what slows down the most when trying to read a language you are learning.

So, I wrote this program in order to find words I likey don't know before reading something, by searching a text for the most rare words according to a Spanish word frequency list generated from a corpora of text.

I use this in conjunction with 
- [AutoAnkiData](https://github.com/RRomreoJr/AutoAnkiData), a project I made to more quickly gather data for new flashcards
- [Anki](https://apps.ankiweb.net/) (an SRS flashcard program) to filter out any words I'm already studying

## Installation Instructions

1. Install Python (at least version 3.9.6).
   OR
   Activate your Python virtual environment if you have one you want to use.
2. Clone this to the folder you want to use it in. Either with git clone or downloading the .zip file and extracting.
3. Run `set_up.bat`.
