"""
Module for user defined exception errors for trie.py
"""

class Error(Exception):
    """ Base class for own exceptions """

class SearchMiss(Error):
    """ Raised when word could not be found in dictionary """
