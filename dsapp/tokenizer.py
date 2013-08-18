#! /usr/bin/env python
# coding: utf-8

from nltk.tokenize import word_tokenize, sent_tokenize

def tokenize(filename, output = 'output.txt'):
    with open(output, 'w') as f:
        s = open(filename).read()
        tokens = [word_tokenize(t) for t in sent_tokenize(s)]
        for token in tokens:
            f.write(token)
            f.write('\n')

if __name__ == '__main__':
    tokenize('rfc792.txt')
