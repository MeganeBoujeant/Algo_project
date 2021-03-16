#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Mégane Boujeant"
__version__ = "1.0.0"
__license__ = "MIT"
__copyright__ = "Copyright 2021, @MeganeBoujeant"


class TransformeeBW:
    """ Class of Burrows-Weeler transformation. """

    def __init__(self, controller):
        self.controller = controller
        self.list_step_trans_seq = []
        self.list_el_matrix_final_trans = []
        self.list_step_recons_seq = []

    def transformation_seq(self, sequence: str):
        """ Transformation method to obtain the BWT sequence.

        Parameter
        ---------
        sequence : str
            DNA sequence that we want to make Burrows-Weeler transformation

        Return
        ------
        bwt : str
            BWT sequence corresponding to Burrows-Weeler transformation of DNA
            sequence
        """

        # Add '$' after the sequence
        seq = sequence.upper() + "$"

        # Initialization of the square matrix of all the offsets of the sequence
        seq_matrix = [seq]

        previous_seq = seq

        # Filling of the square matrix
        for i in range(0, len(seq)-1, 1):
            next_seq = previous_seq[len(seq)-1] + previous_seq[0:len(seq)-1]
            # Complete list for print step by step
            self.list_step_trans_seq.append(next_seq)
            seq_matrix.append(next_seq)
            previous_seq = next_seq

        # Sorting the square matrix and display
        self.sort_and_print_matrix(seq_matrix, self.list_el_matrix_final_trans)

        # Recovering the last character of each line
        bwt = ""

        for line in seq_matrix:
            bwt += line[len(line)-1]

        self.save(bwt)

        return bwt

    @staticmethod
    def save(bwt: str):
        """ Method which save bwt sequence when a transformation of sequence is
        made.

        Parameter
        ---------
        bwt : str
            BWT sequence
        """

        f = open('../data/bwt.txt', 'w')
        f.write(bwt)
        f.close()

    def reconstruction_seq(self, bwt: str):
        """ Method of re-transformation of the BWT sequence into the original
        sequence.

        Parameter
        ---------
        bwt : str
            BWT sequence

        Return
        ------
        seq : str
            initial DNA sequence
        """

        # Repetition of insertion of the word bwt in the 1st column then sorting
        r_matrix = []

        for char in bwt:
            r_matrix.append(char)

        self.sort_and_print_matrix(r_matrix, self.list_step_recons_seq)

        for i in range(0, len(bwt)-1, 1):
            for j in range(0, len(bwt), 1):
                r_matrix[j] = bwt[j] + r_matrix[j]

            self.sort_and_print_matrix(r_matrix, self.list_step_recons_seq)

        # Search for the last character == '$'
        for element in r_matrix:
            if element[len(element)-1] == '$':
                seq = element[0:len(element)-1]
                return seq

    @staticmethod
    def sort_and_print_matrix(m: list, list_of_mat: list):
        """ Method to sort and allows display matrix m.

        Parameters
        ----------
        m : list
            matrix with elements that we want to sort and display
        list_of_mat : list
            list of elements that we will display in the GUI later
        """
        m.sort()
        for element in m:
            list_of_mat.append(element)
