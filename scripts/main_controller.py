#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Mégane Boujeant"
__version__ = "1.0.0"
__license__ = "MIT"
__copyright__ = "Copyright 2021, @MeganeBoujeant"


from view import View
from BWT import TransformeeBW
from compression_huffman import HuffmanCompression, HuffmanDecompression


class Controller:
    """ Class of controller which make the link between TransformeeBW,
    HuffmanCompression, HuffmanDecompression models and the view of the GUI."""

    def __init__(self):
        self.view = View(self)
        self.bwt = TransformeeBW(self)
        self.results_bwt = ''
        self.step = 0
        self.results_seq = ''
        self.compression = None
        self.unicode_seq = ''

    def main(self):
        """ This method allows initialization of the main interface. """

        self.view.main()

    def bwt_button(self, seq):
        """ This method is called when using the BWT button.
        This method launches Burrows-Weeler transformation of DNA sequence, and
        update the view consequently.

        Parameter
        ---------
        seq : str
            DNA sequence
        """

        self.results_bwt = self.bwt.transformation_seq(seq)
        self.view.bwt_page()

    def huffman_button(self, seq):
        """ This method is called when using the Huffman Compression button.
        This method launches Huffman compression of DNA or BWT sequence, and
        update the view consequently.

        Parameter
        ---------
        seq : str
            DNA sequence
        """

        self.compression = HuffmanCompression(seq)
        binary_seq = self.compression.binary_seq
        unicode_dict = self.compression.dict_unicode
        self.unicode_seq = self.compression.seq_unicode
        self.view.huffman_page(seq, binary_seq, unicode_dict, self.unicode_seq)

    def print_matrix_bwt_by_step(self):
        """ This method is called when using the Next Step button on BWT page.
        This method allows display Burrows-Weeler transformation step by step.
        """

        if self.step < len(self.bwt.list_step_trans_seq):
            self.view.add_label(self.bwt.list_step_trans_seq[self.step])
            self.step += 1
            self.view.reset_button()
            self.view.button_bwt()
        else:
            self.print_final_matrix_bwt()

    def print_final_matrix_bwt(self):
        """ This method is called when using the View Final Results button on
        BWT page, or when print_matrix_bwt_by_step method is at the last step.
        This method allows display lasts step of Burrows-Weeler transformation
        and BWT sequence. """

        self.view.reset()
        for step in self.bwt.list_el_matrix_final_trans:
            self.view.add_label(step)
        self.view.add_label("BWT sequence : " + self.results_bwt)
        self.view.button_after_bwt()

    def back_to_seq_button(self):
        """ This method is called when using the BWT To Seq button.
         This method launches recontruction of DNA sequence starting from BWT
         sequence, and update the view consequently."""

        self.results_seq = self.bwt.reconstruction_seq(self.results_bwt)
        self.step = 0
        self.view.recon_bwt_page()

    def print_step_recon_bwt(self):
        """ This method is called when using the Next Step button on
        reconstruction BWT page.
        This method allows display recontruction of DNA sequence step by step.
        """

        self.view.reset()
        if self.step < len(self.bwt.list_step_recons_seq)-len(self.results_bwt):
            for line in range(self.step, self.step+len(self.results_bwt), 1):
                self.view.add_label(self.bwt.list_step_recons_seq[line])
            self.step += len(self.results_bwt)
            self.view.reset_button()
            self.view.button_recon_bwt()
        else:
            self.print_matrix_recon_bwt()

    def print_matrix_recon_bwt(self):
        """ This method is called when using the View Final Results button on
        reconstruction BWT page, or when print_step_recon_bwt method is at the
        last step.
        This method allows display lasts step of recontruction of DNA sequence
        and initial DNA sequence. """

        self.view.reset()
        start_last_step = len(self.bwt.list_step_recons_seq)-len(
            self.results_bwt)
        end_last_step = len(self.bwt.list_step_recons_seq)
        for line in range(start_last_step, end_last_step, 1):
            self.view.add_label(self.bwt.list_step_recons_seq[line])
        self.view.add_label("The initial sequence is : " + self.results_seq)

    def decomp_huffman_button(self):
        """ This method is called when using the Huffman Decompression button on
        Huffman Compression page.
        This method launches Huffman decompression of unicode sequence, and
        update the view consequently. """

        len_seq = self.compression.len_binary_seq
        dict_bin_char = self.compression.dict_char
        decomp = HuffmanDecompression(self.unicode_seq, len_seq, dict_bin_char)
        initial_sequence = decomp.initial_seq
        self.view.decomp_huffman_page(self.unicode_seq, decomp.binary_seq,
                                      initial_sequence)

    def huffman_with_bwt_button(self, seq):
        """ This method is called when using the Huffman Compression button on
        BWT page when Burrows-Weeler transformation was made.
        This method launches Huffman compression of BWT sequence, and update the
        view consequently.

        Parameter
        ---------
        seq : str
            BWT sequence
        """

        self.compression = HuffmanCompression(seq)
        binary_seq = self.compression.binary_seq
        unicode_dict = self.compression.dict_unicode
        self.unicode_seq = self.compression.seq_unicode
        self.view.huffman_bwt_page(seq, binary_seq, unicode_dict,
                                   self.unicode_seq)

    def decomp_bwt_huffman_button(self):
        """ This method is called when using the Huffman Decompression button on
        Huffman Compression page when Burrows-Weeler transformation was made
        before Huffman compression.
        This method launches Huffman decompression of unicode sequence, and
        update the view consequently. """

        len_seq = self.compression.len_binary_seq
        dict_bin_char = self.compression.dict_char
        decomp = HuffmanDecompression(self.unicode_seq, len_seq, dict_bin_char)
        pre_initial_seq = decomp.initial_seq
        initial_sequence = ""
        for char in pre_initial_seq:
            if char == 'N':
                initial_sequence += '$'
            else:
                initial_sequence += char
        self.view.decomp_bwt_huffman_page(self.unicode_seq, decomp.binary_seq,
                                          initial_sequence)

    def check_file(self, path):
        """ This method is called when user open file. This method check what
        file is and make action consequently.

        Parameter
        ---------
        path : str
            path of the file that we want to open
        """

        bwt_file = "bwt.txt"
        huff_file = "huffile.txt"
        bwt_huff_file = "dechuffile.txt"

        # If file is a bwt file, display a view which propose to make
        # reconstruction of the initial DNA sequence, or make Huffman
        # compression
        if path[len(path)-len(bwt_file):len(path)] == bwt_file:
            with open('../data/bwt.txt') as f:
                self.results_bwt = f.read()
            self.view.reset()
            self.view.add_label("Your BWT sequence is :")
            self.view.add_label(self.results_bwt)
            self.view.button_after_bwt()

        # If file is a Huffman file, make Huffman decompression
        elif path[len(path)-len(huff_file):len(path)] == huff_file:
            with open('../data/huffile.txt') as f:
                list_huffile_element = f.read().split('\n')

            self.unicode_seq = list_huffile_element[0]
            len_binary_seq = int(list_huffile_element[1])
            dict_bin_char = eval(list_huffile_element[2])
            decomp = HuffmanDecompression(self.unicode_seq, len_binary_seq,
                                          dict_bin_char)
            initial_sequence = decomp.initial_seq

            # Check if sequence obtained is the initial DNA sequence or BWT
            # sequence, then display the initial sequence
            if '$' in initial_sequence:
                self.results_bwt = initial_sequence
                self.results_seq = self.bwt.reconstruction_seq(self.results_bwt)
                self.view.decomp_huffman_page(self.unicode_seq,
                                              decomp.binary_seq,
                                              self.results_seq)
            else:
                self.view.decomp_huffman_page(self.unicode_seq,
                                              decomp.binary_seq,
                                              initial_sequence)

        # If file is a BWT Huffman file, make reconstruction of the initial DNA
        # sequence
        elif path[len(path)-len(bwt_huff_file):len(path)] == bwt_huff_file:
            with open('../data/dechuffile.txt') as f:
                self.results_bwt = f.read()
            self.back_to_seq_button()


if __name__ == "__main__":
    directory = Controller()
    directory.main()
