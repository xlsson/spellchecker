#!/usr/bin/env python3
"""
Main module for the SpellChecker
"""
from trie import Trie
from errors import SearchMiss

class SpellChecker():
    """ Main class for SpellChecker """

    def __init__(self):
        """ Create an object """
        self.trie = Trie()
        self.filename = "tiny_frequency.txt"

    def _find_word(self):
        """ Check if word in wordlist. Else: raise SearchMiss """
        word = input("\nEnter word: ")
        try:
            self.trie.find_word(word)
            print(f"Correct! '{word}' is spelled correctly.")
        except SearchMiss:
            print(f"SearchMiss error: '{word}' is not in dictionary.")

    def _prefix_search(self):
        """ Take user input, three letters """
        letters = ""
        while len(letters) < 3:
            letters = input("\nEnter a prefix (three or more letters): ")
        try:
            self.trie.find_prefix(letters, self.trie.root)
        except SearchMiss:
            print("\nSearchMiss error: No words in dictionary start with those letters.")

    def _change_file(self):
        """ Create new Trie-instance and change wordlist file.  """
        self.filename = input("\nEnter filename: ")
        try:
            with open(self.filename, "r") as file:
                if len(file.readline()) > 0:
                    self.trie = Trie()
                    self._read_file()
                else:
                    print("Error: file is empty. Try another file.")
        except FileNotFoundError:
            print("Error: file not found. Try another filename.")

    def _read_file(self):
        """
        Read wordlist line by line with generator method
        """
        for line in self._read_one_line():
            word, freq = line.split()[0], float(line.split()[1])
            self.trie.insert_word(word, freq)

    def _read_one_line(self):
        """ Generator method: read one line from list """
        with open(self.filename, "r") as file:
            for line in file:
                yield line

    def _display_all_words(self):
        """ Display all words in wordlist """
        allwords = self.trie.find_all_words()
        allwords_sorted = self.sort(allwords)
        for word_freq in allwords_sorted:
            print(f"{word_freq[0]} {word_freq[1]}")

    def sort(self, list_):
        """ Sort list by splitting, comparing and merging """
        return self._recursive_split(list_)

    def _recursive_split(self, list_):
        """ Split one list in half """
        half = len(list_)//2
        if half < 1:
            return list_
        left, right = list_[:half], list_[half:]
        left = self._recursive_split(left)
        right = self._recursive_split(right)
        return self.mergesort(left, right)

    @staticmethod
    def mergesort(left, right):
        """ Sort and merge two list fragments """
        allwords_sorted = []
        l, r = 0, 0

        while l < len(left) and r < len(right):
            if left[l] < right[r]:
                allwords_sorted.append(left[l])
                l += 1
            else:
                allwords_sorted.append(right[r])
                r += 1

        if l < len(left):
            for i in range(l, len(left)):
                allwords_sorted.append(left[i])
        elif r < len(right):
            for i in range(r, len(right)):
                allwords_sorted.append(right[i])

        return allwords_sorted

    def _remove_word(self):
        """ Remove word. If word does not exist, raise SearchMiss """
        word = input("\nEnter word: ")
        try:
            self.trie.remove(word)
            print(f"'{word}' has been removed.")
        except SearchMiss:
            print(f"'{word}' is not in dictionary (SearchMiss)")

    @staticmethod
    def _display_menu():
        """ Displays all menu options """
        print('\n1: Check if word is in wordlist')
        print('2: Prefix search')
        print('3: Change wordlist file')
        print('4: Display all words in list (alphabetical order)')
        print('5: Remove word\n')
        print('q: Quit\n')

    def start(self):
        """ Read file and start the menu """
        self._read_file()
        while True:
            self._display_menu()
            choice = input("Your choice: ")
            if choice == "1":
                self._find_word()
            elif choice == "2":
                self._prefix_search()
            elif choice == "3":
                self._change_file()
            elif choice == "4":
                self._display_all_words()
            elif choice == "5":
                self._remove_word()
            elif choice == "q":
                print("Bye!")
                break
            else:
                print("Not a valid choice.")

            input("\nPress any key to continue ...")

if __name__ == "__main__":
    spellchecker = SpellChecker()
    spellchecker.start()
