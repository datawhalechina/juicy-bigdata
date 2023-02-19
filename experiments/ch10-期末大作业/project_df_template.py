from pyspark.sql.session import SparkSession
from pyspark.sql.functions import *
import sys


def takeTopK(pairList, k):
    #填入获得前k个排名的函数

class Project2:

    def run(self, inputPath, outputPath, stopwords, k):
        spark = SparkSession.builder.master("local").appName("project2_df").getOrCreate()

        #填入以下两个函数的参数
        fileDF = spark.read.text()
        swlist = spark.sparkContext.broadcast()


        headlineDF = fileDF.select(split(fileDF['value'], ',').getItem(0).substr(0, 4).alias('year'),
                                   split(fileDF['value'], ',').getItem(1).alias('headline'))
        headlineDF = headlineDF.withColumn('word', split('headline', ' '))
        headlineDF2 = headlineDF.select('year', array_distinct(headlineDF.word).alias('word'))
        headlineDF3 = headlineDF2.withColumn('word', explode('word'))

        yearwordsDF = headlineDF3[~headlineDF3.word.isin(swlist.value)]
        #写出TF计算的函数
        TF =
        totalYear = yearwordsDF.select('year').distinct().count()
        #写出DF计算的函数
        DF =
        TFIDF = TF.join(DF, TF.word == DF.word).select(TF.year, TF.word, TF.TF, DF.DF)

        weightDF = TFIDF.withColumn('weight', round(TFIDF.TF * log10(totalYear / TFIDF.DF), 6)).select('year', 'word',
                                                                                                       'weight')
        groupDF = weightDF.groupBy('year').agg(collect_list(struct('word', 'weight')).alias('pair'))
        topkUDF = udf(lambda z, k: takeTopK(z, k))
        res = groupDF.withColumn('pair', topkUDF('pair', lit(int(k)))).orderBy('year')
        res2 = res.coalesce(1).orderBy('year').withColumn('result', concat_ws('\t', 'year', 'pair')).select('result')
        res2.write.text(outputPath)
        spark.stop()


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Wrong arguments")
        sys.exit(-1)
    Project2().run(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

