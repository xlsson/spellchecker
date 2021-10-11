#!/usr/bin/env python3
"""
Trie structure for the Spellchecker
"""
from operator import itemgetter
from node import Node
from errors import SearchMiss

class Trie():
    """ Main class for the trie structure """

    def __init__(self):
        """ Initiate an object """
        self.root = Node("")
        self.savedwords = []

    def insert_word(self, word, freq):
        """ Insert a word in structure """
        node = self.root
        index = len(word)-1
        for i in range(index):
            node = self._insert_letter(node, word[i])
        return self._insert_letter(node, word[index], freq, True)

    @staticmethod
    def _insert_letter(node, value, freq=None, stop=False):
        """ Insert a letter in structure, if not exists """
        if value in node.children:
            if stop:
                node[value].stop = stop
                node[value].freq = freq
        else:
            node[value] = value
            node.children[value].stop = stop
            node.children[value].freq = freq
        return node[value]

    def find_word(self, word):
        """ Check if word is in structure """
        if len(word) == 0:
            raise SearchMiss
        node = self.root
        index = len(word)-1
        for i in range(index):
            node = self._find_letter(node, word[i])
        return self._find_letter(node, word[index], True)

    @staticmethod
    def _find_letter(node, value, stop=False):
        """ Check if letter is child to node """
        if value in node.children:
            if stop is False:
                return node[value]
            if stop and node[value].is_word():
                return node[value]
        raise SearchMiss

    def find_prefix(self, letters, node):
        """ Find prefix node, append to words if word """
        self.savedwords = []

        for letter in letters:
            node = self._find_letter(node, letter)
        if node.is_word():
            self.savedwords.append((letters, node.freq))

        for child in node:
            self._find_and_save_words(node[child], letters)

        self._sort_print_prefixwords()

        newletter = input(f"\nAdd a letter ('quit' exits): {letters}")
        if newletter == "quit":
            return
        letters += newletter
        self.find_prefix(letters, self.root)

    def find_all_words(self):
        """ Find all words in structure """
        self.savedwords = []
        node = self.root
        for child in node:
            self._find_and_save_words(node[child], "")
        return self.savedwords

    def _find_and_save_words(self, node, letters):
        """ Traverse each child node, save words to list """
        letters += node.value
        if node.is_word():
            self.savedwords.append((letters, node.freq))
        for child in node:
            self._find_and_save_words(node[child], letters)

    def _sort_print_prefixwords(self):
        """ Order savedwords by frequency, print 10 most frequent """
        sortedwords = sorted(self.savedwords, key=itemgetter(1), reverse=True)
        counter = 0
        for word_freq in sortedwords:
            print(f"{word_freq[0]} {word_freq[1]}")
            counter += 1
            if counter > 9:
                break

    def remove(self, word):
        """
        Remove the node representing the last letter in word.
        If node has children: do not remove, only set 'stop' to False.
        """
        last_letter = self.find_word(word)
        if last_letter.has_children():
            last_letter.stop = False
            return
        parentnode = last_letter.parent
        del parentnode[word[-1]]
        del last_letter
        word = word[:-1]
        if len(word) > 0:
            self._remove(word, parentnode)
        else:
            return

    def _remove(self, word, node):
        """ Remove further nodes """
        if node.is_word() or node.has_children():
            return
        parentnode = node.parent
        del parentnode[word[-1]]
        del node
        word = word[:-1]
        if len(word) > 0:
            self._remove(word, parentnode)
        else:
            return
