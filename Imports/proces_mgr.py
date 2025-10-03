from multiprocessing import Queue
from multiprocessing.connection import PipeConnection


class ProcessManager:
    def __init__(self, handle_pipe = None, ret_pipe: PipeConnection=None):
        self.processes = {}
        self.queues = {}
        self.handle_pipe = handle_pipe
        self.ret_pipe = ret_pipe
        self.i_queue: dict[int,Queue] = {}

    def add_process(self, process):
        self.processes.append(process)

    def remove_process(self, process):
        if process in self.processes:
            self.processes.remove(process)

    def list_processes(self):
        return self.processes

    def start_process(self, file:str, args):
        with open(file, "r") as f:
            # Run Type
            f.readline()
            # Includes
            f.readline()
            # Exports
            f.readline()
            # Process Name
            proc_name = f.readline().strip()
        
        if file.endswith(".mpy"):
            self._start_mpy_proc(file, args, proc_name)
            return
        pass

    def _start_mpy_proc(self,file:str, args, proc_name:str):
        import multiprocessing
        from .mpy_runtime import MPY_RunTime as mpy_runtime
        self.handle_pipe.send(("GET_NEW_PID", proc_name))
        def start_code(code: str, args, pid, sys_queue : Queue, ret_queue:Queue):
            mpy_runtime(code,args,pid,sys_queue,ret_queue, run=True)

        
        with open(file, "r") as f :
            code = f.read()
        
        pid: int = self.ret_pipe.recv(1024)
        
        in_queue = multiprocessing.Queue()
        out_queue = multiprocessing.Queue()



        multiprocessing.Process(target=start_code,args=(code,args,pid,out_queue,in_queue))
        