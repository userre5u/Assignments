# Simple UDP chat

## usage (regular chat) ##
	python3 chat.py --ip <local_ip> --port <local_port> --dst <remote_machine_ip>:<remote_machine_port> --user 
    <chat username>

    Example:

    VM A (local ip 192.168.199.150)
    - python3 chat.py --ip 192.168.199.150 --port 4444 --dst 192.168.199.138:4443 --user bob

    VM B (local ip 192.168.199.138)
    - python3 chat.py --ip 192.168.199.138 --port 4443 --dst 192.168.199.150:4444 --user alice



## usage (chat over ICMP) ##
	python3 chat_over_ping.py --target_ip <remote_machine_ip> --user <chat username>

    Example:
    
    VM A (local ip 192.168.199.150)
    - python3 chat_over_ping.py --target_ip 192.168.199.138 --user bob

    VM B (local ip 192.168.199.138)
    - python3 chat_over_ping.py --target_ip 192.168.199.150 --user alice




