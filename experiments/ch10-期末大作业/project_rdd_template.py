from pyspark import SparkContext, SparkConf
from operator import add
from math import log10
import heapq
import sys


def takeTopK(pairList, k):
    #填入获得前k个排名的函数


class Project2:

    def run(self, inputPath, outputPath, stopwords, k):
        conf = SparkConf().setAppName("project2_rdd")
        sc = SparkContext(conf=conf)

        # 填入以下两个函数的参数
        filerdd = sc.textFile()
        swlist = sc.broadcast()

        #写出以下标题、年度词、TF、总年计算的函数
        headlines =
        yearwords =
        TF =
        totalYear =

        # DF = yearwords.map(lambda x:(x[0][1], x[0][0])).countByKey()
        DF = yearwords.map(lambda x: (x[0][1], x[0][0])).groupByKey().map(lambda x: (x[0], len(x[1])))

        TFIDF = TF.join(DF).map(lambda x: (x[1][0][0], (round(x[1][0][1] * log10(totalYear / x[1][1]), 6), x[0])))
        res = TFIDF.groupByKey().map(lambda x: (x[0], list(x[1]))).mapValues(lambda x: takeTopK(x, int(k)))
        res2 = res.coalesce(1).sortByKey().map(
            lambda x: f'{x[0]}\t{";".join([item[1] + "," + str(item[0]) for item in x[1]])}')

        res2.saveAsTextFile(outputPath)
        sc.stop()


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Wrong arguments")
        sys.exit(-1)
    Project2().run(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

