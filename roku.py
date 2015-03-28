import socket

# host = '192.168.1.247'
# port = 8060

DISCOVER_GROUP = ('239.255.255.250', 1900)

DISCOVER_MESSAGE = '''\
M-SEARCH * HTTP/1.1\r\n\
Host: %s:%s\r\n\
Man: "ssdp:discover"\r\n\
ST: roku:ecp\r\n\r\n\
''' % DISCOVER_GROUP

print DISCOVER_MESSAGE

def find_roku():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(DISCOVER_MESSAGE, DISCOVER_GROUP)
    data = s.recv(1024)
    return data

def press(sock, key):
    message = "POST /keypress/home HTTP/1.1\r\nHost: 192.168.1.247:8060\r\n\r\n"
    print message
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.sendall(message)

print find_roku()
