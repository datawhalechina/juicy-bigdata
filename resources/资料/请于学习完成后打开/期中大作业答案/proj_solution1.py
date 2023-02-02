from mrjob.job import MRJob
from mrjob.step import MRStep

class Project1(MRJob):
    def mapper(self, _, line):
        userID, locID, time = line.split(",") 
        yield userID + "," + locID, 1
        yield userID + ",*", 1
        
    def combiner(self, key, values):
        yield key, sum(values)

    def reducer_init(self):
        self.Nuj = 0    
        
    def reducer(self, key, values):
        userID, locID = key.split(",")
        
        if locID == "*":
            self.Nuj = sum(values)
        else:
            v = str(sum(values) / self.Nuj)
            yield f'{userID}#{locID}#{v}', ""             
        
    def reducer_sort(self, key, _):        
        userID, locID, v = key.split("#")
        yield locID, f'{userID},{v}' 
    
    SORT_VALUES = True 
    def steps(self):        
        JOBCONF1 = {
            'mapreduce.map.output.key.field.separator':',',
            'mapreduce.partition.keypartitioner.options':'-k1,1',
            #Below is not necessary, but you can still do it
            #'mapreduce.job.output.key.comparator.class':'org.apache.hadoop.mapreduce.lib.partition.KeyFieldBasedComparator',
            #'mapreduce.partition.keycomparator.options':'-k1,1 -k2,2',
        }
        JOBCONF2 = {
            'mapreduce.map.output.key.field.separator':'#',
            'mapreduce.partition.keypartitioner.options':'-k2,2',
            'mapreduce.job.output.key.comparator.class':'org.apache.hadoop.mapreduce.lib.partition.KeyFieldBasedComparator',
            'mapreduce.partition.keycomparator.options':'-k2,2 -k3,3nr -k1,1'
        }
        return [
            MRStep(jobconf=JOBCONF1, mapper=self.mapper, combiner=self.combiner, reducer_init=self.reducer_init, reducer=self.reducer),
            MRStep(jobconf=JOBCONF2, reducer=self.reducer_sort)
        ]

if __name__ == '__main__':
    Project1.run()
