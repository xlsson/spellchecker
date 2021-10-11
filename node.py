#!/usr/bin/env python3
"""
Node module for the Spellchecker trie structure
"""
class Node():
    """ Node class """
    def __init__(self, value, parent=None, stop=False, freq=None):
        """ Constructor for Node """
        self.value = value
        self.parent = parent
        self.stop = stop
        self.freq = freq
        self.children = {}

    def has_children(self):
        """ Return True if node has children """
        return len(self.children) > 0

    def is_word(self):
        """ Return True if node is end of a word """
        return self.stop is True

    def __iter__(self):
        """ Magic method to make node children iterable """
        for child in self.children:
            yield child

    def __setitem__(self, key, value):
        """ Magic method for adding attributes to node children """
        self.children[key] = Node(value, self)

    def __getitem__(self, key):
        """ Magic method for getting attributes from node children """
        return self.children[key]

    def __delitem__(self, key):
        """ Magic method for deleting attributes from node children """
        del self.children[key]
