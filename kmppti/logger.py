import time
import os
import csv
import psutil


class Logger:
    def __init__(self, log_path, filename, metadata):
        self.log_path = log_path
        self.info = self.get_info(filename) + metadata
        self.start_time = None
        self.end_time = None

    def get_info(self, filename):
        return filename.split("/")[-1].split(".")[0].split("_")[:-1]

    def write(self):
        result = []
        if not os.path.exists(self.log_path):
            result.append(['Data Type', 'Data Size', 'Dim Size', 'k', 'Grid Size', 'TS Start', 'TS End', 'Runtime (S)', 'Mem Usage (MB)'])
        result.append(self.info + [self.get_runtime(), self.get_mem_usage()])
        with open(self.log_path, 'a') as output:
            writer = csv.writer(output, lineterminator='\n')
            for res in result:
                writer.writerow(res)
    
    def start(self):
        self.start_time = time.time()
    
    def end(self):
        self.end_time = time.time()
    
    def get_runtime(self):
        hours, rem = divmod(self.end_time - self.start_time, 3600)
        minutes, seconds = divmod(rem, 60)
        return "{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)
    
    def get_mem_usage(self):
        process = psutil.Process(os.getpid())
        # mem = float(process.memory_info().rss)/1000000.0
        mem = process.memory_info().rss / 1024 ** 2 # MB
        return mem

    