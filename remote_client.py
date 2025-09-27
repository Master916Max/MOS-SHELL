import socket

def remote_terminal_client(host='localhost', port=8932):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        while True:
            data = s.recv(4096)
            print(data.decode(), end='')
            cmd = input()
            s.send(cmd.encode())
            if cmd.strip().lower() == 'exit':
                break

if __name__ == "__main__":
    remote_terminal_client()