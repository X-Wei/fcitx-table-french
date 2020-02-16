#!/usr/bin/env python3
#coding: utf-8
'''
This script contains some code to convert a wordlist into a table for fcitx. 

The wordlists are in the folder `wordlists/`, in one wordlist(a .txt file), 
there's one word per line, for example: "École".

The output will be a table for fcitx, that is, a text file in which each line 
is a code and the corresponding word, separated by a space, for example: 
"Ecole École".

The output file can then be transmitted into a .mb file using the command 
`txt2mb` (need to install `fcitx-tools`).

@author: xwei
'''
from __future__ import print_function
import unicodedata, os, numpy

# dic={u'æ':'ae',u'œ':'oe'}#becasue cannot correctly convert 2 chars...
u8 = 'utf8'  # encoding for my files...
uesp = 'unicode-escape'  # encoding for the initial file lesmotfrancais.txt ==>ISO-8859-1


def make_table(folder='wordlists', outfn='fr_table.txt', remove_prime=False):
  outlst = []

  for fn in sorted(os.listdir(folder)):
    print(f'Processing wordlist {fn}...')
    with open(folder + os.sep + fn) as f:
      lst = [wd.strip() for wd in f]
      for word in lst:
        code = unicodedata.normalize('NFD', word.replace('ß', 'ss')).encode(
            'ascii',
            'ignore')  # convert accented word into non-accented word (code)
        strout = f'{code.decode()} {word}'
        print(strout)
        outlst.append(strout)
        if code.decode()[0].islower():
          caped_strout = f'{code.capitalize().decode()} {word.capitalize()}'
          outlst.append(caped_strout)
        if remove_prime and "'" in code.decode():
          strout = (code.decode().replace("'", '') + ' ' + word)
          outlst.append(strout)
          caped_strout = (code.decode().replace("'", '').capitalize() + ' ' +
                          word.capitalize())
          outlst.append(caped_strout)

  with open(outfn, 'w') as outf:
    headers = open('header.txt', 'r').readlines()
    outf.writelines(headers)
    idx = numpy.unique(numpy.array(outlst), return_index=True)[1]
    # Get the unique, unsorted list.
    uniquelst = [outlst[i] for i in sorted(idx)]
    outf.write("\n".join(uniquelst))
    print(len(outlst), len(uniquelst))
  print('fini! %d mots convertis!' % len(uniquelst))


if __name__ == '__main__':
  # make_table(remove_prime=True)
  make_table(folder='wordlists-de', outfn='de-table.txt', remove_prime=True)
