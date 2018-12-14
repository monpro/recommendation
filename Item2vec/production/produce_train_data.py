#-*-coding:utf8-*-
"""
author:monpro
produce train data for item2vec
"""

import os
import sys


def produce_train_data(input_file, out_file):
    """
    Args:
        input_file:user behavior file
        out_file: output file
    """
    if not os.path.exists(input_file):
        return
    record = {}
    line_num = 0
    score_thr = 4.0
    fp = open(input_file)
    for line in fp:
        if line_num==0:
            line_num += 1
            continue
        item = line.strip().split(',')
        if len(item) < 4:
            continue
        user_id, item_id, rating = item[0], item[1], float(item[2])
        if rating < score_thr:
            continue
        if user_id not in record:
            record[user_id] = []
        record[user_id].append(item_id)
    fp.close()
    fw = open(out_file, 'w+')
    for user_id in record:
        fw.write(" ".join(record[user_id]) + "\n")
    fw.close()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: python xx.py inputFile outputFile")
        sys.exit()
    else:
        inputFile = sys.argv[1]
        outputFile = sys.argv[2]
        produce_train_data(inputFile, outputFile)
        #produce_train_data("../data/ratings.txt", "../data/train_data.txt")
