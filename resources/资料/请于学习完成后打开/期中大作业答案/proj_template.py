from mrjob.job import MRJob
from mrjob.step import MRStep

# ---------------------------------!!! Attention Please!!!------------------------------------
# Please add more details to the comments for each function. Clarifying the input 
# and the output format would be better. It's helpful for tutors to review your code.

# Using multiple MRSteps is permitted, please name your functions properly for readability.

# We will test your code with the following comand:
# "python3 project1.py -r hadoop hdfs_input -o hdfs_output --jobconf mapreduce.job.reduces=2"

# Please make sure that your code can be compiled before submission.
# ---------------------------------!!! Attention Please!!!------------------------------------

class proj(MRJob):    

    # define your own mapreduce functions

    SORT_VALUES = True

    JOBCONF = { 
        # add your configurations here
    }

    def steps(self):
        return [
            # you decide the number of steps used
        ]

if __name__ == '__main__':
    proj.run()