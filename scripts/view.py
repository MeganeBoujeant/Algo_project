#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Mégane Boujeant"
__version__ = "1.0.0"
__license__ = "MIT"
__copyright__ = "Copyright 2021, @MeganeBoujeant"


from tkinter import Tk, Label, Entry, Button
from tkinter import Menu
from tkinter import filedialog
import os


class View(Tk):
    """ Class of the Graphical User Interface (GUI). """

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.fic = ""

    def main(self):
        """This method allows initializes the main window of the GUI."""

        self.geometry('600x300')
        self.title("Algo")
        self.create_menu()
        self.main_page()
        self.mainloop()

    def create_menu(self):
        """This method creates a menu bar that contains several tabs, each
        tab gives access to a feature of the GUI. """

        menu_bar = Menu(self)

        menu_file = Menu(menu_bar, tearoff=0)
        menu_file.add_command(label="Quit", command=self.quit,
                              accelerator="Ctrl+q")
        menu_bar.add_cascade(label="File", menu=menu_file)

        menu_home = Menu(menu_bar, tearoff=0)
        menu_home.add_command(label="Home Page", command=self.main_page)
        menu_bar.add_cascade(label="BackToHome", menu=menu_home)

        menu_to_seq = Menu(menu_bar, tearoff=0)
        menu_to_seq.add_command(label="Open File To Seq",
                                command=self.open_file, accelerator="Ctrl+o")
        menu_bar.add_cascade(label="ToSeq", menu=menu_to_seq)

        self.bind_all("<Control-q>", lambda e: self.quit)
        self.bind_all("<Control-o>", lambda e: self.open_file())

        self.config(menu=menu_bar)

    def open_file(self):
        """ This method open a selected file to process it according to its
        contents. """

        self.fic = filedialog.askopenfilename(title="Select open file :",
                                              initialdir=os.getcwd()+"/data",
                                              filetypes=(("Text Files",
                                                          "*.txt"), ))

        if len(self.fic) > 0:
            self.controller.check_file(self.fic)

    def main_page(self):
        """ This method create the main page of the GUI.
        This page allows to make a Burrows-Weeler transformation or a Huffman
        compression. """

        self.reset()

        text_seq = Label(self, text="Enter DNA sequence:", font=("courier", 18))
        text_seq.pack()

        entry_seq = Entry(self, width=40, font=("courier", 18))
        entry_seq.pack()

        button_bwt = Button(self, text="BWT", font=("courier", 18),
                            command=lambda:
                            self.controller.bwt_button(entry_seq.get()))
        button_bwt.pack(side='left', padx=80)

        button_huffman = Button(self, text="Huffman compression",
                                font=("courier", 18), command=lambda:
                                self.controller.huffman_button(entry_seq.get()))
        button_huffman.pack(side='right', padx=70)

    def reset(self):
        """This method allows widget reset, except the widget of the menu bar.
        This function is particularly useful when user changes tabs,
        or also if user clicks on the tab again. """

        for widget in self.winfo_children():
            if "button" in str(widget):
                widget.destroy()
            if "label" in str(widget):
                widget.destroy()
            if "entry" in str(widget):
                widget.destroy()

    def reset_button(self):
        """ This method allows button widget reset. """

        for widget in self.winfo_children():
            if "button" in str(widget):
                widget.destroy()

    def add_label(self, text_add: str):
        """ This method allows add Label widget.

        Parameter
        ---------
        text_add : str
            text that we want to add in Label widget
        """

        add_label = Label(self, text=text_add, font=("courier", 16))
        add_label.pack()

    def bwt_page(self):
        """ This method create the BWT page. """

        self.reset()
        self.button_bwt()

    def huffman_page(self, seq, binary_seq, unicode_dict, seq_unicode):
        """ This method create the Huffman compression page.

        Parameters
        ----------
        seq : str
            DNA sequence that you have enter in previous page
        binary_seq : str
            binary sequence corresponding to the initial DNA sequence
        unicode_dict : dict
            dictionary with key = binary byte and value = unicode corresponding
        seq_unicode : str
            unicode sequence corresponding to the initial sequence
        """

        self.reset()

        self.geometry('600x500')

        self.add_label("Your sequence is :")
        self.add_label(seq)
        self.add_label('')

        self.add_label("Corresponding binary sequence :")
        self.add_label(binary_seq)
        self.add_label('')

        self.add_label("Characters which correspond to binary byte are :")
        for key, value in unicode_dict.items():
            self.add_label("{} = {}".format(key, value))
        self.add_label('')

        self.add_label("Corresponding sequence with special characters :")
        self.add_label(seq_unicode)
        self.add_label('')

        button_huffman = Button(self, text="Huffman decompression",
                                font=("courier", 16), command=lambda:
                                self.controller.decomp_huffman_button())
        button_huffman.pack()

    def button_bwt(self):
        """ This method create buttons of the BWT pages. """

        next_step_button = Button(self, text="Next Step", font=("courier", 16),
                                  command=lambda:
                                  self.controller.print_matrix_bwt_by_step())
        next_step_button.pack(side="left")

        final_matrix_button = Button(self, text="View final results",
                                     font=("courier", 16), command=lambda:
                                     self.controller.print_final_matrix_bwt())
        final_matrix_button.pack(side="right")

    def button_after_bwt(self):
        """ This method create button of the final BWT page. """

        button_huffman = Button(self, text="Huffman compression",
                                font=("courier", 16), command=lambda:
                                self.controller.huffman_with_bwt_button(
                                    self.controller.results_bwt))
        button_huffman.pack(side='left')

        button_bwt_to_seq = Button(self, text="BWT To Seq",
                                   font=("courier", 16), command=lambda:
                                   self.controller.back_to_seq_button())
        button_bwt_to_seq.pack(side='right')

    def recon_bwt_page(self):
        """ This method create the BWT sequence to reconstruction DNA sequence
        page. """

        self.reset()
        self.button_recon_bwt()

    def button_recon_bwt(self):
        """ This method create button of the BWT sequence to reconstruction DNA
        sequence page. """

        next_step_button = Button(self, text="Next Step", font=("courier", 16),
                                  command=lambda:
                                  self.controller.print_step_recon_bwt())
        next_step_button.pack(side="left")

        final_matrix_button = Button(self, text="View final results",
                                     font=("courier", 16), command=lambda:
                                     self.controller.print_matrix_recon_bwt())
        final_matrix_button.pack(side="right")

    def huffman_bwt_page(self, seq, binary_seq, unicode_dict, seq_unicode):
        """ This method create the BWT to Huffman compression page.

        Parameters
        ----------
        seq : str
            BWT sequence
        binary_seq : str
            binary sequence corresponding to the BWT sequence
        unicode_dict : dict
            dictionary with key = binary byte and value = unicode corresponding
        seq_unicode : str
            unicode sequence corresponding to the BWT sequence
        """

        self.reset()

        self.geometry('600x500')

        self.add_label("Your bwt sequence is :")
        self.add_label(seq)
        self.add_label('')

        self.add_label("Corresponding binary sequence :")
        self.add_label(binary_seq)
        self.add_label('')

        self.add_label("Characters which correspond to binary byte are :")
        for key, value in unicode_dict.items():
            self.add_label("{} = {}".format(key, value))
        self.add_label('')

        self.add_label("Corresponding sequence with special characters :")
        self.add_label(seq_unicode)
        self.add_label('')

        button_huffman = Button(self, text="Huffman decompression",
                                font=("courier", 16), command=lambda:
                                self.controller.decomp_bwt_huffman_button())
        button_huffman.pack()

    def decomp_huffman_page(self, unicode_seq, binary_seq, initial_sequence):
        """ This method create the Huffman decompression page.

        Parameters
        ----------
        unicode_seq : str
            unicode sequence
        binary_seq : str
            binary sequence corresponding to the initial DNA sequence
        initial_sequence : str
            DNA initial sequence
        """

        self.reset()

        self.add_label("Your unicode sequence is :")
        self.add_label(unicode_seq)
        self.add_label('')

        self.add_label("The corresponding binary sequence is :")
        self.add_label(binary_seq)
        self.add_label('')

        self.add_label("Your initial sequence is :")
        self.add_label(initial_sequence)
        self.add_label('')

    def decomp_bwt_huffman_page(self, unicode_seq, binary_seq, initial_seq):
        """ This method create the Huffman decompression to bwt sequence page.

        Parameters
        ----------
        unicode_seq : str
            unicode sequence
        binary_seq : str
            binary sequence corresponding to the BWT sequence
        initial_seq : str
            BWT sequence
        """

        self.reset()

        self.add_label("Your unicode sequence is :")
        self.add_label(unicode_seq)
        self.add_label('')

        self.add_label("The corresponding binary sequence is :")
        self.add_label(binary_seq)
        self.add_label('')

        self.add_label("Your initial bwt sequence is :")
        self.add_label(initial_seq)
        self.add_label('')

        button_bwt_to_seq = Button(self, text="BWT To Seq",
                                   font=("courier", 16), command=lambda:
                                   self.controller.back_to_seq_button())
        button_bwt_to_seq.pack()
