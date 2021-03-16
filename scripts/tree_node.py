#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Mégane Boujeant"
__version__ = "1.0.0"
__license__ = "MIT"
__copyright__ = "Copyright 2021, @MeganeBoujeant"


class TreeNode:
    """ Class to make a tree node. """

    def __init__(self, char, data):
        self.char = char
        self.data = data
        self.left_child = None
        self.right_child = None
        self.bin = ''

    def __str__(self):
        return '[' + str(self.bin) + ":" + str(self.char) + ';' + \
               str(self.left_child) + "," + str(self.right_child) + "]"

    def is_leaf(self):
        """ This method test if my node is a leaf or not.

        Return
        ------
        True or False : booleen
            return true if node is leaf, else return false
        """
        return self.right_child is None and self.left_child is None

    def update_child(self, left, right):
        """ This method update child of a node.

        Parameters
        ----------
        left : object
            node which is the left child of the self node
        right : object
            node which is the right child of the self node
        """
        self.left_child = left
        self.right_child = right
