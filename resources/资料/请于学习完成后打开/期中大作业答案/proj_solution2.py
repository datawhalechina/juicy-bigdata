from mrjob.job import MRJob
from mrjob.step import MRStep
import re



class proj(MRJob):
    # define your own mapreduce functions

    SORT_VALUES = True

    JOBCONF_1 = {
        'mapreduce.map.output.key.field.separator': ',',
        'partitioner': 'org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner',
        'mapreduce.partition.keypartitioner.options': '-k1,1',
        'mapreduce.job.output.key.comparator.class': 'org.apache.hadoop.mapreduce.lib.partition.KeyFieldBasedComparator',
        'mapreduce.partition.keycomparator.options': '-k1,1 -k2,2'
    }
    JOBCONF_2 = {
        'mapreduce.map.output.key.field.separator': ',',
        'partitioner': 'org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner',
        'mapreduce.partition.keypartitioner.options': '-k1,1',
        'mapreduce.job.output.key.comparator.class': 'org.apache.hadoop.mapreduce.lib.partition.KeyFieldBasedComparator',
        'mapreduce.partition.keycomparator.options': '-k1,1 -k2,2nr -k3,3'
    }

    def steps(self):

        return [
            MRStep(
                mapper=self.mapper_1,
                combiner=self.combiner_1,
                reducer_init=self.reducer_init_1,
                reducer=self.reducer_1,
                jobconf=self.JOBCONF_1
            ),
            MRStep(
                mapper=self.mapper_2,
                reducer=self.reducer_2,
                jobconf=self.JOBCONF_2
            )
        ]

    def mapper_1(self, _, line):
        # yield each user+local and user+* in the line
        words = re.split(",", line.lower())
        yield words[0] + "," + words[1], 1
        yield words[0] + ',*', 1

    def combiner_1(self, key, values):
        # sum the keys we've seen so far
        yield key, sum(values)

    def reducer_init_1(self):
        self.total = {}

    def reducer_1(self, key, values):
        # compute the probability and reform the format
        wi, wj = key.split(",", 1)
        if wj == "*":
            self.total[wi] = sum(values)
        else:
            count = sum(values)
            yield None, wj + ',' + str(count / self.total[wi]) + ',' + wi

    # discard the key; it is just None
    def mapper_2(self, _, value):
        # sort the result
        words = re.split(",", value.lower())
        yield words[0] + ',' + words[1] + ',' + words[2], None

    def reducer_2(self, key, _):
        # reform the format and output the result
        wi, wj, wk = key.split(",")
        yield wi, wk + ',' + wj


if __name__ == '__main__':
    proj.run()
