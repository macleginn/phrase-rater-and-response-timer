# Automatically generates a report from output 
# files in the same or some other directory.

# phrase_ratings_Mon_Jun_30_00-46-11_2014

# Phrase: Cé acu atá níos sine?, processing_time: 2.26, rating: 2.
# Phrase: Thuigeas é go maith., processing_time: 1.11, rating: 1.
# Phrase: Tá mo mhac sa scoil anois., processing_time: 1.38, rating: None.

import sys
import os
import os.path
from time import ctime

# files = sys.argv[1:]
dirname = "."
if len(sys.argv) > 1:
    dirname = sys.argv[1]
files = [item for item in os.listdir(dirname) if item.startswith("phrase_ratings")]
reportDic = {}
for name in files:
    with open(os.path.join(dirname, name), 'r', encoding = 'utf-8') as inp:
        for line in inp:
            tail = line.split("Phrase: ")[1]
            words = tail.split(", processing_time: ")[0]
            tail = tail.split(" processing_time: ")[1]
            pTime = float(tail.split(", rating: ")[0])
            tail = tail.split(", rating: ")[1]
            rating = int(tail[:-2]) if (tail[:-2] != 'None' and tail[:-2] != '') else -1
            reportDic[words] = reportDic.get(words, []) + [(name, pTime, rating)]
with open('phrase_rater_report.txt', 'w') as out:
    keys = sorted(reportDic.keys())
    for key in keys:
        out.write(key + ": ")
        outStr = ("; ".join('%s: %.2f, %d' % (pair[0], pair[1], pair[2]) for pair in reportDic[key]) + '\n').replace("-1", "None")
        out.write(outStr)