#!/usr/bin/env python3
"""
Test module for the Spellchecker
"""
import unittest
from errors import SearchMiss
from spellchecker import SpellChecker
from trie import Trie
from node import Node

class Tests(unittest.TestCase):
    """Submodule for unittests, derives from unittest.TestCase"""

    def setUp(self):
        """ Setup test """
        self.trie = Trie()

        with open("tiny_frequency.txt", "r") as file:
            for line in file:
                word = line.split()[0]
                freq = float(line.split()[1])
                self.trie.insert_word(word, freq)

    def tearDown(self):
        """ Tear down test """
        self.trie = None

    def test_find_word_raise_searchmiss(self):
        """ Test if non-existant words raise SearchMiss errors """
        with self.assertRaises(SearchMiss):
            self.trie.find_word("thisworddoesnotexist")
        with self.assertRaises(SearchMiss):
            self.trie.find_word("")

    def test_find_word_not_raise_searchmiss(self):
        """ Test that existing word does not raise SearchMiss error """
        try:
            self.trie.find_word("bicycle")
        except SearchMiss:
            self.fail("SearchMiss raised")
        try:
            self.trie.find_word("shoe")
        except SearchMiss:
            self.fail("SearchMiss raised")

    def test_find_prefix_raise_searchmiss(self):
        """ Test if non-existant prefixes raise SearchMiss errors """
        with self.assertRaises(SearchMiss):
            self.trie.find_prefix("abc", self.trie.root)
        with self.assertRaises(SearchMiss):
            self.trie.find_prefix("xyz", self.trie.root)

    def test_insert_word_exists(self):
        """
        Test that word can be inserted and not raise SearchMiss when
        searched for
        """
        testword = ("testword", 4.87)
        self.trie.insert_word(testword[0], testword[1])
        try:
            self.trie.find_word(testword[0])
        except SearchMiss:
            self.fail("SearchMiss raised")

    def test_insert_word_letter_is_node(self):
        """ Test that last inserted letter is an instance of Node """
        testword = ("testword", 4.87)
        testword_node = self.trie.insert_word(testword[0], testword[1])
        self.assertIsInstance(testword_node, Node)

    def test_insert_word_attributes(self):
        """ Test that last inserted letter has expected attribute values """
        testword = ("testword", 4.87)
        testword_last_letter = testword[0][len(testword[0])-1]
        testword_node = self.trie.insert_word(testword[0], testword[1])
        self.assertEqual(testword_last_letter, testword_node.value)
        self.assertEqual(testword[1], testword_node.freq)

    def test_insert_word_relationship(self):
        """ Test that inserted word nodes are connected as expected """
        testword = ("testword", 4.87)
        testword2 = ("testwordz", 9.17)
        testword_node = self.trie.insert_word(testword[0], testword[1])
        testword2_node = self.trie.insert_word(testword2[0], testword2[1])
        self.assertEqual(testword_node, testword2_node.parent)

    def test_remove_no_searchmiss(self):
        """ Test that removing existing word does not raise SearchMiss """
        try:
            self.trie.remove("bicycle")
        except SearchMiss:
            self.fail("SearchMiss raised")

    def test_remove_searchmiss(self):
        """ Test that removing non-existing word raises SearchMiss """
        with self.assertRaises(SearchMiss):
            self.trie.remove("tricycle")

    def test_removed_word_searchmiss(self):
        """ Test that searching for removed word raises SearchMiss """
        self.trie.remove("bicycle")
        with self.assertRaises(SearchMiss):
            self.trie.find_word("bicycle")

    def test_sort_inner(self):
        """ Test """
        left = [('banan', 1.1), ('bulle', 23.0), ('stor', 4.4), ('truck', 3.3)]
        right = [('Japan', 5123.122), ('bank', 21.1), ('boll', 24.0), ]

        sorted_list = [('Japan', 5123.122), ('banan', 1.1), ('bank', 21.1),
                       ('boll', 24.0), ('bulle', 23.0), ('stor', 4.4), ('truck', 3.3)]

        spellchecker = SpellChecker()
        merged_list = spellchecker.mergesort(left, right)
        self.assertEqual(merged_list, sorted_list)

    def test_sort(self):
        """ Test merge sort with wordlists with even/uneven lengths """
        wordlist_1 = [('bank', 21.1)]
        wordlist_7 = [
            ('stor', 4.4), ('truck', 3.3), ('banan', 1.1), ('bulle', 23.0),
            ('Japan', 5123.122), ('boll', 24.0), ('bank', 21.1)]
        sorted_7 = [
            ('Japan', 5123.122), ('banan', 1.1), ('bank', 21.1),
            ('boll', 24.0), ('bulle', 23.0), ('stor', 4.4), ('truck', 3.3)]
        wordlist_16 = [
            ('spritsa', 20.0), ('stork', 19.2), ('truck', 3.3), ('spraka', 18.0),
            ('banan', 1.1), ('svulstig', 4.4), ('spankulera', 17.1), ('svit', 15.0),
            ('spurt', 15.0), ('boll', 24.0), ('stor', 4.4), ('sval', 33.0),
            ('bank', 21.1), ('spricka', 19.0), ('bulle', 23.0), ('Japan', 5123.122)]
        sorted_16 = [
            ('Japan', 5123.122), ('banan', 1.1), ('bank', 21.1), ('boll', 24.0),
            ('bulle', 23.0), ('spankulera', 17.1), ('spraka', 18.0),
            ('spricka', 19.0), ('spritsa', 20.0), ('spurt', 15.0), ('stor', 4.4),
            ('stork', 19.2), ('sval', 33.0), ('svit', 15.0), ('svulstig', 4.4),
            ('truck', 3.3)]

        spellchecker = SpellChecker()
        merge_sorted_1 = spellchecker.sort(wordlist_1)
        merge_sorted_7 = spellchecker.sort(wordlist_7)
        merge_sorted_16 = spellchecker.sort(wordlist_16)

        self.assertEqual(wordlist_1, merge_sorted_1)
        self.assertEqual(sorted_7, merge_sorted_7)
        self.assertNotEqual(wordlist_7, merge_sorted_7)
        self.assertEqual(sorted_16, merge_sorted_16)
        self.assertNotEqual(wordlist_16, merge_sorted_16)

    def test_sort_freq(self):
        """ Test that merge sort does not sort by frequency """
        wordlist_12 = [
            ('spritsa', 20.0), ('truck', 3.3), ('spraka', 18.0), ('banan', 1.1),
            ('spurt', 15.0), ('boll', 24.0), ('spankulera', 17.1), ('stor', 4.4),
            ('bank', 21.1), ('spricka', 19.0), ('bulle', 23.0), ('Japan', 5123.122)]
        sorted_freq_12 = [
            ('banan', 1.1), ('truck', 3.3), ('stor', 4.4), ('spurt', 15.0),
            ('spankulera', 17.1), ('spraka', 18.0), ('spricka', 19.0),
            ('spritsa', 20.0), ('bank', 21.1), ('bulle', 23.0), ('boll', 24.0),
            ('Japan', 5123.122)]

        spellchecker = SpellChecker()
        test_12 = spellchecker.sort(wordlist_12)

        self.assertNotEqual(sorted_freq_12, test_12)

if __name__ == '__main__':
    unittest.main(verbosity=3)
