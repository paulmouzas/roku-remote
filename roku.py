import requests
import curses
import socket
import re
import string

KEYPRESS_MAP = {}

for char in string.ascii_lowercase + string.ascii_uppercase:
    KEYPRESS_MAP[ord(char)] = char.lower()

KEYPRESS_MAP[9] = 'back'
KEYPRESS_MAP[10] = 'select'
KEYPRESS_MAP[32] = '%20'
KEYPRESS_MAP[96] = 'home'
KEYPRESS_MAP[258] = 'down'
KEYPRESS_MAP[259] = 'up'
KEYPRESS_MAP[260] = 'left'
KEYPRESS_MAP[261] = 'right'
KEYPRESS_MAP[263] = 'backspace'

DISCOVER_GROUP = ('239.255.255.250', 1900)

DISCOVER_MESSAGE = '''\
M-SEARCH * HTTP/1.1\r\n\
Host: %s:%s\r\n\
Man: "ssdp:discover"\r\n\
ST: roku:ecp\r\n\r\n\
''' % DISCOVER_GROUP

def find_roku():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(DISCOVER_MESSAGE, DISCOVER_GROUP)
    data = s.recv(1024)
    return data

def keypress(url, key):
    if key in string.ascii_lowercase:
        key = 'lit_' + key
    request_url = url + 'keypress/' + key
    requests.post(request_url)
    return request_url

class HTTPResponse(dict):
    def __init__(self, response_text):

        response = response_text.split('\r\n')
        status_line = response[0]

        self.http_version, self.status_code, self.status = status_line.split()
        self.headers = {}

        for line in response[1:]:
            line = line.split()
            if len(line) == 2:
                header_name = line[0][:-1]
                header_value = line[1]
                self.headers[header_name.lower()] = header_value.lower()


def main():
    print 'Searching for a Roku device...'
    response_text = find_roku()
    response = HTTPResponse(response_text)
    location = response.headers['location']

    try:
        stdscr = curses.initscr()
        stdscr.keypad(1)
        
        stdscr.addstr(0,0, 'Found one at %s!' % location)
        stdscr.addstr(1,0,"Press escape to quit")
        stdscr.addstr(2,0, 'Use the arrow keys to move the cursor and press Enter to select')
        stdscr.refresh()
        
        key = ''
        while key != 27: # escape key
            key = stdscr.getch()
            stdscr.refresh()
            if key: 
                stdscr.addstr(0,10, str(key))
                command = KEYPRESS_MAP.get(key, '')
                keypress(location, command)
    finally:
        curses.endwin()


if __name__ == '__main__': main()
