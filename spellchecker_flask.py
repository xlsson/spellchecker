#!/usr/bin/env python3
"""
Web interface (Flask) module for the SpellChecker
"""
from trie import Trie
from errors import SearchMiss
from spellchecker import SpellChecker

class SpellCheckerFlask():
    """ Class for web interface """

    def __init__(self):
        """ Create an object """
        self.trie = Trie()
        self.filename = "frequency.txt"
        self._read_file()
        self.allwords_sorted = self.get_all_words()

    def find_word(self, word):
        """ Check if word in wordlist. Else: raise SearchMiss """
        try:
            self.trie.find_word(word)
            message = f"Correct! '{word}' is spelled correctly."
            return message
        except SearchMiss:
            message = f"SearchMiss: '{word}' is not in dictionary."
            return message

    def _read_file(self):
        """ Read wordlist line by line by calling generator function """
        for line in self._read_one_line():
            word, freq = line.split()[0], float(line.split()[1])
            self.trie.insert_word(word, freq)

    def _read_one_line(self):
        """ Generator function: read one line from list """
        with open(self.filename, "r") as file:
            for line in file:
                yield line

    def get_all_words(self):
        """ Display all words in wordlist """
        allwords = self.trie.find_all_words()
        allwords_sorted = SpellChecker().sort(allwords)
        return allwords_sorted
