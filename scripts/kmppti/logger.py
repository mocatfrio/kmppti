import datetime, os

class Logger:
    def __init__(self, log_path):
        self.path = self.__set_dir(log_path)
        self.filename = self.__set_filename()
        self.ts = None
        self.event = None
        self.action = None

    def __set_dir(self, log_path):
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        return log_path
    
    def __set_filename(self):
        now = datetime.datetime.now()
        return self.path + now.strftime("%Y-%m-%d %H:%M:%S") + ".txt"

    def set_ts(self, ts):
        self.ts = ts
        self.write()

    def set_event(self, obj_name, obj_act, obj_pos):
        act_name = "in" if obj_act == 0 else "out"
        self.event = " ".join([obj_name, act_name, str(obj_pos)])
    
    def set_action(self, action):
        self.action = "["+ action +"]"

    def write(self, text=None):
        with open(self.filename, mode="a") as file:
            if not text:
                text = "===================================================="
            elif isinstance(text, list):
                text = [self.ts, "\t", self.event, "\t", self.action, "\t"] + text
                text = " ".join(str(e) for e in text)
            file.write("{}\n".format(text))

    



    