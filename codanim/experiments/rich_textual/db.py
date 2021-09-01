import sys
import time
from types import FrameType

from rich import inspect


def my_trace(frame, event, arg):
    print(frame, event, arg)

    def trace_moar(f_frame: FrameType, f_event, f_arg):
        time.sleep(1)
        # inspect(f_frame, all=True)
        print(f_frame.f_lineno)
        print(f_frame.f_locals)

    return trace_moar


def work():
    for i in range(10):
        print(i)


if __name__ == "__main__":
    sys.settrace(my_trace)
    work()
