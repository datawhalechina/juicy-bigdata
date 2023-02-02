from pyspark import SparkContext, SparkConf
from operator import add
from math import log10
import heapq
import sys

def takeTopK(pairList, k):
    q = []
    for p in pairList:
        if(len(q)<=k):
            q.append(p)
        if len(q)>k:
            q = sorted(q, key = lambda x: (-x[0], x[1]), reverse=False)
            del q[k]
    return q

class Project2:   
        
    def run(self, inputPath, outputPath, stopwords, k):
        conf = SparkConf().setAppName("project2_rdd")
        sc = SparkContext(conf=conf)
        
        filerdd = sc.textFile(inputPath)
        swlist = sc.broadcast(set(sc.textFile(stopwords).collect()))
        headlines = filerdd.map(lambda x: x.split(",", 1)).map(lambda x: (x[0][:4], set(x[1].split(" "))))
        yearwords = headlines.flatMap(lambda x: [((x[0], item), 1) for item in x[1] if item not in swlist.value]).reduceByKey(add)
        TF = yearwords.map(lambda x:(x[0][1], (x[0][0], x[1])))
        totalYear = yearwords.map(lambda x: x[0][0]).distinct().count()
        
        #DF = yearwords.map(lambda x:(x[0][1], x[0][0])).countByKey()
        DF = yearwords.map(lambda x:(x[0][1], x[0][0])).groupByKey().map(lambda x:(x[0], len(x[1])))
        
        TFIDF = TF.join(DF).map(lambda x: (x[1][0][0], (round(x[1][0][1]*log10(totalYear/x[1][1]), 6), x[0])))
        res = TFIDF.groupByKey().map(lambda x:(x[0], list(x[1]))).mapValues(lambda x: takeTopK(x, int(k)))
        res2 = res.coalesce(1).sortByKey().map(lambda x: f'{x[0]}\t{";".join([item[1]+","+str(item[0]) for item in x[1]])}')

        res2.saveAsTextFile(outputPath)
        sc.stop()

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Wrong arguments")
        sys.exit(-1)
    Project2().run(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

