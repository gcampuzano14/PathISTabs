import re
import os
import csv
from nltk import *
from nltk.tag import *
from nltk.chunk import *
from nltk.corpus import treebank

# input: TABDELIMITED FILE WITH ROWS BY CASE NUMBER
# output: CSV FILE WITH LIST OF CASES


def main():
    dxlist = []
    data = csv.DictReader(open('full_mds_tab.txt', 'r'), delimiter="\t")
    output_file =  'out.csv'
    with open(output_file, 'wb') as csvfile:
        result_writer = csv.writer(csvfile)
        for element in data:
            dxstr = element['DIAGNOSIS'].lower()
            all_instances = re.findall('[^\.!?:;]*myelodysplastic\s+syndrome[^\.!?:;]*[\.!?:;]', dxstr, re.S)
            outdxstr = "__________".join(all_instances)
            punc = re.compile("[,\.\/;'!\?&\-_]")
            strp = punc.sub(" ", outdxstr)
            dxlist.append(strp)
            outdxlist = [element['SURGINAL_NUMBER'],element['ACCESS_DATE'],outdxstr]
            result_writer.writerow(outdxlist)
    return dxlist


dxlist = main()

for e in dxlist:
    tokens = word_tokenize(str(e))
    print(tokens)
    tagged = pos_tag(tokens)
    entities = chunk.ne_chunk(tagged)
    print(entities)
    t = treebank.parsed_sents(entities)[0]
    t.draw()
