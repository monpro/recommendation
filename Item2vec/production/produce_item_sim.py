#-*-coding:utf8-*-
"""
author:monpro
produce item sim file
"""

import os
import numpy as np
import operator
import sys


def load_item_vec(input_file):
    """
    Args:
        input_file: item vec file
    Return:
        dict key:item_id value:np.array([num1, num2....])
    """
    if not os.path.exists(input_file):
        return {}
    line_num = 0
    item_vec = {}
    fp = open(input_file)
    for line in fp:
        if line_num == 0:
            line_num += 1
            continue
        item = line.strip().split()
        if len(item) < 129:
            continue
        item_id = item[0]
        if item_id == "</s>":
            continue
        item_vec[item_id] = np.array([float(ele) for ele in item[1:]])
    fp.close()
    return item_vec


def cal_item_sim(item_vec, item_id, output_file):
    """
    Args
        item_vec:item embedding vector
        item_id:fixed item_id to clac item sim
        output_file: the file to store result
    """
    if item_id not in item_vec:
        return
    score = {}
    topk = 10
    fix_item_vec = item_vec[item_id]
    for tmp_itemid in item_vec:
        if tmp_itemid == item_id:
            continue
        tmp_itemvec = item_vec[tmp_itemid]
        denominator = np.linalg.norm(fix_item_vec) * np.linalg.norm(tmp_itemvec)
        if denominator == 0:
            score[tmp_itemid] = 0
        else:
            score[tmp_itemid] =  round(np.dot(fix_item_vec, tmp_itemvec)/denominator, 3)
    fw = open(output_file, "w+")
    out_str = item_id + "\t"
    tmp_list = []
    for combination in sorted(score.iteritems(), key = operator.itemgetter(1), reverse = True)[:topk]:
        tmp_list.append(combination[0] + "_" + str(combination[1]))
    out_str += ";".join(tmp_list)
    fw.write(out_str + "\n")
    fw.close()


def run_main(input_file, output_file):
    item_vec = load_item_vec(input_file)
    cal_item_sim(item_vec, "27", output_file)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: python xx.py inputFile outputFile")
        sys.exit()
    else:
        inputFile = sys.argv[1]
        outputFile = sys.argv[2]
        run_main(inputFile, outputFile)
        #run_main("../data/item_vec.txt", "../data/sim_result.txt")