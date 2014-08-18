#coding: utf-8
'''
This script contains some code to convert a wordlist into a table for fcitx. 

The wordlists are in the folder `wordlists/`, in one wordlist(a .txt file), there's one word per line, for example: "École".

The output will be a table for fcitx, that is, a text file in which each line is a code and the corresponding word, separated by a space, for example: "Ecole École".

The output file can then be transmitted into a .mb file using the command `txt2mb` (need to install `fcitx-tools`)

@author: xwei
'''
import unicodedata, os, numpy



# dic={u'æ':'ae',u'œ':'oe'}#becasue cannot correctly convert 2 chars...
u8 = 'utf8' # encoding for my files...
uesp = 'unicode-escape' # encoding for the initial file lesmotfrancais.txt ==>ISO-8859-1



def make_table(folder = 'wordlists',outfn='fr_table.txt',remove_prime=False):
    outlst = []
    
    fns = os.listdir(folder)
    for fn in sorted(fns):
        lst = [wd.strip().decode('utf8') for wd in open(folder + os.sep + fn)]
        for word in lst:
            code = unicodedata.normalize('NFD', word).encode('ascii', 'ignore') # convert accented word into non-accented word (code)
            strout = (code + ' ' + word).encode('utf8')
            print strout
            outlst.append(strout)
            caped_strout = (code.capitalize() + ' ' + word.capitalize()).encode('utf8')
            outlst.append(caped_strout)
            if remove_prime and "'" in code:
                strout = (code.replace("'",'') + ' ' + word).encode('utf8')
                outlst.append(strout)
                caped_strout = (code.replace("'",'').capitalize() + ' ' + word.capitalize()).encode('utf8')
                outlst.append(caped_strout)
    
    with open(outfn,'w') as outf:
        headers = open('header.txt','r').readlines()
        outf.writelines(headers)
        idx = numpy.unique( numpy.array(outlst), return_index=True )[1]
        uniquelst = [ outlst[i] for i in sorted(idx) ]#we need to do so to get the unique, unsorted list...
        outf.write( "\n".join(uniquelst) )
        print len(outlst), len(uniquelst)
    print 'fini! %d mots convertis!' % len(uniquelst)



if __name__ == '__main__':
    make_table(remove_prime=True)





