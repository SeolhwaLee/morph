from konlpy.tag import Komoran
import pandas as pd
import regex
import os
import subprocess

komoran = Komoran()


# print(len(contents))

lst = []
lst2 = []

count = 0
file_path = "./input/"
num_line = subprocess.Popen(['wc', '-l', file_path + 'wiki_ko_preprocess.txt'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

with open(file_path + 'wiki_ko_preprocess.txt','r') as fr:
    with open("pos_wiki_ko.txt",'w',encoding='utf-8') as fw:
        for lines in fr.readlines():
            count += 1
            pos = komoran.pos(lines)
            fw.write("%s\n" % (pos))
            if count % 1000 == 0:
                print("------progress bar  (", count, ",", num_line, ")")
        print("POS tagging finished")


with open("pos_wiki_ko.txt",'r') as fr:
    with open("tagging_remove_wiki_ko.txt",'w',encoding='utf-8') as fw:
        for lines in fr.readlines():
            # print(lines)
            # break
            lst = []
            for i in range(0,len(lines)):
                try:
                    first = lines.split(', ')[i*2].rstrip().strip('"\'')
                    # print(first)
                    second = lines.split(', ')[i*2+1].rstrip().strip('"\'')
                    # print(second)
                    # print(first + '/' + second)
                    non_symbol = str(first).replace('(','').replace(')','').replace('"','').strip('"\'')
                    lst.append(non_symbol)
                except:
                    pass
            result = " ".join(lst)
            non_symbol_result = result.replace("[",'').replace("]",'').strip('"\'')
            fw.write("%s\n" % (non_symbol_result))






