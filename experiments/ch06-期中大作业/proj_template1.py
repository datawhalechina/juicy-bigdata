from mrjob.job import MRJob
from mrjob.step import MRStep


class Project1(MRJob):
    def mapper(self, _, line):
        userID, locID, time = line.split(",")
        #填入mapper的具体步骤


    def combiner(self, key, values):
        #填入combiner的具体步骤


    def reducer_init(self):
        # 填入reducer_init的具体步骤


    def reducer(self, key, values):
        userID, locID = key.split(",")
        # 填入reducer的具体步骤


    def reducer_sort(self, key, _):
        userID, locID, v = key.split("#")
        yield locID, f'{userID},{v}'

    SORT_VALUES = True

    def steps(self):
        #填入配置参数
        JOBCONF1 = {
            'mapreduce.map.output.key.field.separator':
            'mapreduce.partition.keypartitioner.options':
            # Below is not necessary, but you can still do it
            # 'mapreduce.job.output.key.comparator.class':'org.apache.hadoop.mapreduce.lib.partition.KeyFieldBasedComparator',
            # 'mapreduce.partition.keycomparator.options':'-k1,1 -k2,2',
        }
        # 填入配置参数
        JOBCONF2 = {
            'mapreduce.map.output.key.field.separator':
            'mapreduce.partition.keypartitioner.options':
            'mapreduce.job.output.key.comparator.class':
            'mapreduce.partition.keycomparator.options':
        }
        return [
            MRStep(jobconf=JOBCONF1, mapper=self.mapper, combiner=self.combiner, reducer_init=self.reducer_init,
                   reducer=self.reducer),
            MRStep(jobconf=JOBCONF2, reducer=self.reducer_sort)
        ]


if __name__ == '__main__':
    Project1.run()
