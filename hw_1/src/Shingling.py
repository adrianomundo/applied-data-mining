'''
Shingling Class Methods:
- Load document
- Clean up of the document from useless characters such as parentheses, commas ...
- Building fo the k-shingles from the document
- Compute the hash values for each shingle and order the set of unique shingles

Shingling Class Attributes:
- Document
- Shingles set
- Hashed shingles set

'''

import numpy as np
import re
import random
from collections import OrderedDict


class Shingling:    

    def __init__(self, document_filename):
        self.document_filename = document_filename
        self.document = ""
        self.shingles = None
        self.hashed_shingles = None

    def load_clean_document(self):
        with open(self.document_filename) as file:
            text = file.read()
            text = text.lower()
            text = text.replace("  ", " ")
            cleaned_text = re.sub(r'[^\w\s]','', text)
            cleaned_text = cleaned_text.replace('\n', '')

            self.document  = cleaned_text

    def load_raw_document(self):
        with open(self.document_filename) as file:
            self.document = file.read()
                
    
    def build_shingles(self, k_length):
        shingles = []
        for i in range(0, len(self.document) - k_length):
            shingles.append((self.document[i: i+k_length]))

        #print(len(shingles))    
        self.shingles = list(dict.fromkeys(shingles))
        #print(len(self.shingles))
        #self.shingles = list(set(shingles))

    def hash_shingles(self):

        hashed_shingles = []
        for shingle in self.shingles:
            hashed_shingles.append(self.hash_ascii(shingle))

        self.hashed_shingles = hashed_shingles
    
        #self.hashed_shingles = sorted(hashed_shingles)

    def hash_ascii(self, shingle):

        a = 50
        b = 25

        sum_ascii = 0
        for char in shingle:
            sum_ascii += ord(char)

        hash_val = (a * sum_ascii + b) % (2**32 - 1)
        return hash_val


    
    