from multiprocessing import Process, Pipe

def start_remote_terminal():
    parent_conn, child_conn = Pipe()
    rt_process = Process(target=RemoteTerminal, args=(child_conn,))
    rt_process.start()
    return parent_conn, rt_process
    
# Runs as a separate process
class RemoteTerminal:
    def __init__(self, piprecv, port = 8932):
        self.port = port
        self.piprecv = piprecv
        self.loop()
    def loop(self):
        import socket
        import os
        import subprocess

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('localhost', self.port))

        s.listen(1)
        conn, addr = s.accept()
        print('Connection from:', addr)
        conn.send(b'Welcome to Remote Terminal\r\n')
        conn.send(b'Type "exit" to close the connection.\r\n')
        conn.send(b'> ')

        while True:
            data = conn.recv(1024)
            if not data:
                break
            command = data.decode().strip()
            if command.lower() == 'exit':
                conn.send(b'Goodbye!\r\n')
                break
            elif command.isspace() or command == '' or command == '\n':
                conn.send(b'> ')
                continue
            else:
                ret = self.execute_command(command, conn)
                conn.send(ret + b'\r\n> ')
            conn.send(b'> ')

        conn.close()
        s.close()
        os._exit(0)
    def execute_command(self, command, conn):
        match command.split()[0]:
            case "start_process":
                self.piprecv.send(("start_process", command[len(command.split()[0])+1:]))
                return b'Process start requested.'
            case "sp":
                self.piprecv.send(("start_process", command[len(command.split()[0])+1:]))
                return b'Process start requested.'
            case "kill_process":
                self.piprecv.send(("kill_process", command[len(command.split()[0])+1:]))
                return b'Process kill requested.'
            case "kp":
                self.piprecv.send(("kill_process", command[len(command.split()[0])+1:]))
                return b'Process kill requested.'
            case "list_processes":
                self.piprecv.send(("list_processes", ""))
                ret = self.piprecv.recv() # Wait for acknowledgement
                return str(f'Process list requested.{ret}').encode()
            case "lp":
                self.piprecv.send(("list_processes", ""))
                ret = self.piprecv.recv() # Wait for acknowledgement
                return str(f'Process list requested.{ret}').encode()
            case _:
                return b'Unknown command.'

        
        