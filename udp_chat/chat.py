import socket
import select
import argparse
import sys



MAX_BYTES = 1024


def handle_connection(udp_socket, target_ip, target_port, username):
    try:
        while True:
            ready_read, _, _ = select.select([udp_socket, sys.stdin], [], [], 0)
            if ready_read:
                for read_buffer in ready_read:
                    if read_buffer is not udp_socket:
                        text = read_buffer.readline()
                        udp_socket.sendto(F"--> {username}: {text}".encode(), (target_ip, target_port))
                        continue
                    data = udp_socket.recv(MAX_BYTES).decode()
                    print(F"\t\t\t\t{data}")

    except KeyboardInterrupt:
        print("\nChat closed")



def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', type=str, required=True)
    parser.add_argument('--port', type=int, required=True)
    parser.add_argument('--dst', type=str, required=True)
    parser.add_argument('--user', type=str, required=True)
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    ip, port, dst, user = args.ip, args.port, args.dst, args.user
    target_ip, target_port = dst.split(":")
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp_socket.bind((ip, port))
    handle_connection(udp_socket, target_ip, int(target_port), user)
    udp_socket.close()

main()

