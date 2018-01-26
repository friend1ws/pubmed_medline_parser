#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys, re


class Pubinfo(object):

    def __init__(self):
        self._author_list = []
        self._title = None
        self._journal_info = None
        self._my_author_order = None
        self._publication_type = None 

    def add_author_list(self, author_name):
        self._author_list.append(author_name)

    @property
    def title(self):
        return self._title
    
    @title.setter   
    def title(self, title):
        self._title = title 

    @property
    def journal_info(self):
        return self._journal_info
    
    @journal_info.setter   
    def journal_info(self, journal_info):
        self._journal_info = journal_info

    @property
    def publication_type(self):
        return self._publication_type

    @publication_type.setter
    def publication_type(self, publication_type):
        self._publication_type = publication_type


    def check_my_author_order(self, my_name):
        return self._author_list.index(my_name) + 1 

    
    def format_journal_info(self):
        journal_info = self._journal_info 
        ind = journal_info.find("[Epub")
        if ind != -1: journal_info = journal_info[:ind]
        
        ind = journal_info.find("doi:")
        if ind != -1: journal_info = journal_info[:ind]
        
        ind = journal_info.find("pii:")
        if ind != -1: journal_info = journal_info[:ind]

        return journal_info.rstrip(' ')



    def print_info(self):
        print ', '.join(self._author_list) + '. ' + self._title + ' ' + self.format_journal_info() + \
              ' (' + str(len(self._author_list)) + "人中" + str(self.check_my_author_order("Shiraishi Y")) + "番目)."



input_file = sys.argv[1]
pubinfo = None
current_prop = None
with open(input_file, 'r') as hin:
    for line in hin:
        line = line.rstrip('\n')

        pind = line.find('-')
        if pind == 4:
            current_prop = line[:pind].rstrip(' ')
        
        current_value = line[6:].rstrip(' ')

        if current_value == "": continue

        if current_prop == "PMID":
            if pubinfo is not None and pubinfo.publication_type != "Published Erratum": 
                pubinfo.print_info()
            pubinfo = Pubinfo()
            temp_prop = "PMID" 

        if current_prop == "TI":
            if pubinfo.title is None:
                pubinfo.title = current_value
            else:
                pubinfo.title = pubinfo.title + ' ' + current_value

        if current_prop == "AU":
            pubinfo.add_author_list(current_value)

        if current_prop == "PT":
            pubinfo.publication_type = current_value

        if current_prop == "SO":
            if pubinfo.journal_info is None:
                pubinfo.journal_info = current_value
            else:
                pubinfo.journal_info = pubinfo.journal_info + ' ' + current_value


"""
    if my_ind == 1:
        print "[" + str(pub_ind) + "] Shiraishi Y, et al. (" + str(num_author) + "人中1番目). " + info_line
    elif k_ind == 0:
        print "[" + str(pub_ind) + "] " + authors[0] + ', ' + "Shiraishi Y, et al. (" + str(num_author) + "人中" + str(my_ind) + "番目). " + info_line
    elif k_ind == 1:
        print "[" + str(pub_ind) + "] Kataoka K, Shiraishi Y. et al. (" + str(num_author) + "人中1番目、" + str(my_ind) + "番目). " + info_line
    elif my_ind < k_ind:
        print "[" + str(pub_ind) + "] " + authors[0] + ', ' + "Shiraishi Y, Kataoka K, et al. (" + str(num_author) + "人中" + str(my_ind) + "番目、" + str(k_ind) + "番目). " + info_line
    else:
        print "[" + str(pub_ind) + "] " + authors[0] + ', ' + "Kataoka K, Shiraishi Y, et al. (" + str(num_author) + "人中" + str(k_ind) + "番目、" + str(my_ind) + "番目). " + info_line

    pub_ind = pub_ind + 1
   
""" 
