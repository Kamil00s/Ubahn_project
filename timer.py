import threading
from functools import wraps
import time

def timer(func):
    #counts time from a start of a method
    @wraps(func)
    def wrapper(self,*args,**kwargs):
        self.status = "searching"
        def timeout():
            self.status = "stopped"
            
        t = threading.Timer(self.max_time,timeout)
        t.daemon = True
        start = time.perf_counter()
        t.start()
        try:
            return func(self, *args,**kwargs)
        finally:
            self.run_time = time.perf_counter() - start
            t.cancel()
            if self.status == "searching":
                self.status = "finished"
    return wrapper
        