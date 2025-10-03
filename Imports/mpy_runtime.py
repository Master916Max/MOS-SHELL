import multiprocessing
import threading

class MPY_RunTime:
    def __init__(self,code: str, args, pid, sys_queue_out : multiprocessing.Queue,sys_queue_in : multiprocessing.Queue, run=False):
        self.code = code
        self.args = args
        self.pid = pid
        self.sys_o = sys_queue_out
        self.sys_i = sys_queue_in
        self.in_q = multiprocessing.Queue()
        self.out_q = multiprocessing.Queue()
        if run:
            self.run()

    def run(self):
        th1 = threading.Thread(target=self.c_run, args=(self,self.code), daemon=True)
        th1.run()
        while th1.is_alive():
            cmd = self.out_q.get()
            ret = self.handle_cmd()
            print(cmd)
            self.in_q.put((0,1))
        
    def c_run(self,code):
        eval(code)
        entry(self.args, self.out_q, self.in_q, self.pid)

    def handle_cmd():
        return ""

    