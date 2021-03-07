import datetime, os, csv, psutil

class Logger:
    def __init__(self, log_path, filename, approach, grid_size, k, ts_start, ts_end):
        self.log_path = log_path
        self.info = self.get_info(filename) + [approach.__name__, grid_size, k, ts_start, ts_end]
        self.start_time = None
        self.end_time = None

    def get_info(self, filename):
        return filename.split("/")[-1].split(".")[0].split("_")[1:]

    def write(self):
        result = []
        if not os.path.exists(self.log_path):
            result.append(['Data Type', 'Data Size', 'Dim Size', 'Approach', 'Grid Size', 'k', 'TS Start', 'TS End', 'Runtime (S)', 'Mem Usage (MB)'])
        result.append(self.info + [self.get_runtime(), self.get_mem_usage()])
        with open(self.log_path, 'a') as output:
            writer = csv.writer(output, lineterminator='\n')
            for res in result:
                writer.writerow(res)
    
    def start(self):
        self.start_time = datetime.datetime.now()
    
    def end(self):
        self.end_time = datetime.datetime.now()
    
    def get_runtime(self):
        return (self.end_time - self.start_time).total_seconds()
    
    def get_mem_usage(self):
        process = psutil.Process(os.getpid())
        # mem = float(process.memory_info().rss)/1000000.0
        mem = process.memory_info().rss / 1024 ** 2 # MB
        return mem
    