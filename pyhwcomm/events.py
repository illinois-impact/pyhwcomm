""" Functions to help with chrome://tracing """

import ujson as json

from enum import Enum

class Trace(object):
    def __init__(self, path, epsilon=0.99):
        self.outfile = open(path, 'w')
        self.outfile.write("[\n")
        self.epsilon = epsilon

    def close(self):
        # chrome://tracing does not need final ']'
        self.outfile.close()

    def begin_duration(self, name, category, timestamp, pid, tid):
        d = {
            "name": str(name),
            "cat": str(category),
            "ph": "B", # begin
            "ts": float(timestamp),
            "pid": str(pid),
            "tid": str(tid)
        }
        json.dump(d, self.outfile)
        self.outfile.write(",\n")

    def end_duration(self, name, category, timestamp, pid, tid):
        d = {
            "name": str(name),
            "cat": str(category),
            "ph": "E", # end
            "ts": float(timestamp),
            "pid": str(pid),
            "tid": str(tid)
        }
        json.dump(d, self.outfile)
        self.outfile.write(",\n")

    def complete_event(self, component, row, name, category, timestamp, duration_us):
        assert duration_us > 0
        d = {
            "name": str(name),
            "cat": str(category),
            "ph": "X",
            "ts": float(timestamp),
            "dur": float(duration_us) * 0.99, # prevent overlaps
            "pid": str(component),
            "tid": str(row)
        }
        json.dump(d, self.outfile)
        self.outfile.write(",\n")
