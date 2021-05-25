import os
import time


def get_file_type(path):
    return os.path.splitext(path)[1]


def get_file_name(path):
    return os.path.basename(path)[:-4]


def get_size(path):
    return os.stat(path).st_size

def timed_exec(fun, args):
    t1 = time.time()
    ret_val = fun(*args)
    t2 = time.time()

    return ret_val, t2-t1

class Data:
    def __init__(self, p_max=os.cpu_count(), p_min=1, path=None):
        self.path = path
        self.p_max = p_max
        self.p_min = p_min
        self.times = {x: 0 for x in range(p_min, p_max+1)}

    def run_multi(self, fun, args):
        ret_val = None
        args = list(args)
        args.append(0)

        for i in range(self.p_min, self.p_max + 1):
            args[-1] = i
            ret_val, t = timed_exec(fun, args)
            self.times[i] += t

        return ret_val
