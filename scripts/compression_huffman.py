#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Mégane Boujeant"
__version__ = "1.0.0"
__license__ = "MIT"
__copyright__ = "Copyright 2021, @MeganeBoujeant"


from tree_node import TreeNode


class HuffmanCompression:
    """ Class of Huffman Compression. """

    def __init__(self, sequence: str):
        self.sequence = sequence.upper()
        self.len_binary_seq = 0
        self.dict_freq = self.freq_nucleotide()
        self.tree = self.creation_tree()
        self.dict_char = {}
        self.char_to_str_binary(self.tree)
        self.binary_seq = ''
        self.dict_unicode = {}
        self.seq_unicode = ''
        self.compression()
        self.save_compression()

    def freq_nucleotide(self):
        """ This method create the frequency dictionary of the characters of the
        sequence.

        Return
        ------
        freq : dict
            frequency dictionary of the characters of the sequence
        """
        freq = {'A': 0, 'C': 0, 'T': 0, 'G': 0, 'N': 0}
        for char in self.sequence:
            if char in freq.keys():
                freq[char] += 1
            else:
                freq['N'] += 1
        return freq

    def creation_tree(self):
        """ This method create the binary tree which represent the best
        compression.

        Return
        ------
        tree_list[0] : object
            root node of the tree
        """
        tree_list = []

        for char, freq in self.dict_freq.items():
            # Creation of a list which contain the leaves of the tree
            tree_list.append(TreeNode(char, freq))

        while len(tree_list) > 1:
            # Sorting the list of nodes according to their frequency
            # Allows to have the 2 smaller frequencies at the beginning
            # of the list
            tree_list.sort(key=lambda x: x.data)

            # Creation of a new node that merges the 2 first nodes of the list
            new_freq = tree_list[0].data + tree_list[1].data
            new_char = tree_list[0].char + tree_list[1].char

            # Creation of the new node
            new_node = TreeNode(new_char, new_freq)

            new_node.update_child(tree_list[0], tree_list[1])

            # Added binary path of the 2 nodes that have been merged
            # And deleting this after added
            tree_list[0].bin = '0'
            tree_list.pop(0)
            tree_list[0].bin = '1'
            tree_list.pop(0)

            # Added the new node to the list of nodes
            tree_list.append(new_node)

        return tree_list[0]

    def char_to_str_binary(self, node, bin_char=''):
        """ This method create a dictionary which give the binary number of each
        character.
        This binary number corresponds to the path taken from the root of the
        tree: 0 = left; 1 = right.

        Parameters
        ----------
        node : node object
            root node of the tree
        bin_char : str
            binary character associated with the node according to if is a left
            child or a right child
        """

        bin_char = bin_char + node.bin

        if node.is_leaf():
            self.dict_char[node.char] = bin_char

        if node.left_child:
            self.char_to_str_binary(node.left_child, bin_char)
        if node.right_child:
            self.char_to_str_binary(node.right_child, bin_char)

    def compression(self):
        """ This method compress the sequence. This method given the unicode
        sequence which correspond to the initial sequence. """

        seq = self.sequence

        # Transformation of the sequence into binary sequence
        for char in seq:
            if char in self.dict_char.keys():
                self.binary_seq += self.dict_char[char]
            else:
                self.binary_seq += self.dict_char['N']

        # Storage of the len of the initial binary sequence
        self.len_binary_seq = len(self.binary_seq)

        # Added, if needed, binary to divide the sequence into 8 binary
        while len(self.binary_seq) % 8 != 0:
            self.binary_seq = self.binary_seq + '0'

        # Transformation of the 8 bytes sequences in the corresponding unicode
        # characters
        # Added this characters in dictionary
        # and Transformation of the binary sequence to unicode sequence
        for i in range(0, len(self.binary_seq), 8):
            self.dict_unicode[self.binary_seq[i:i+8]] = \
                chr(int(self.binary_seq[i:i+8], 2))
            self.seq_unicode = self.seq_unicode + \
                chr(int(self.binary_seq[i:i+8], 2))

    def save_compression(self):
        """ This method save parameters of Huffman compression. """

        f = open('../data/huffile.txt', 'w')
        f.write(self.seq_unicode + "\n" + str(self.len_binary_seq) + "\n" +
                str(self.dict_char))
        f.close()


class HuffmanDecompression:
    """ Class of Huffman Decompression. """

    def __init__(self, unicode_sequence, len_seq, dict_bin_char):
        self.unicode_seq = unicode_sequence
        self.binary_seq = ""
        self.len_init_binary_seq = len_seq
        self.initial_seq = ""
        self.dict_bin_char = dict_bin_char
        self.initial_binary_seq = ""
        self.decompression()

    def decompression(self):
        """ This method decompress the unicode sequence to given the initial
        sequence. """

        # Transformation of unicode sequence to binary sequence
        for char in self.unicode_seq:
            dec = ord(char)
            self.binary_seq += format(dec, '08b')

        self.binary_seq = str(self.binary_seq)

        # Remove binary which was add to obtain a multiple of 8
        nb_char_over = len(self.binary_seq) - self.len_init_binary_seq
        self.initial_binary_seq = \
            self.binary_seq[0:len(self.binary_seq)-nb_char_over]

        # Course of binary sequence and verification if the path corresponds to
        # a DNA character to rebuild the initial DNA sequence
        path_in_progress = ""

        for binary in self.initial_binary_seq:
            path_in_progress += binary
            for key, value in self.dict_bin_char.items():
                if value == path_in_progress:
                    self.initial_seq += key
                    path_in_progress = ""
                    break

    def save_decompression(self):
        """ This method save parameters of Huffman decompression. """

        f = open('../data/dechuffile.txt', 'w')
        f.write(self.initial_seq)
        f.close()
