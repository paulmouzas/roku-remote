import requests
import curses
import socket
import string

KEYPRESS_MAP = {}

for char in string.ascii_lowercase + string.ascii_uppercase:
    KEYPRESS_MAP[ord(char)] = char.lower()

KEYPRESS_MAP.update({
        9: 'back',
        10: 'select',
        32: '#20',
        96: 'home',
        258: 'down',
        259: 'up',
        260: 'left',
        261: 'right',
        263: 'backspace'
    })

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
    if key in string.ascii_lowercase + '%20':
        key = 'lit_' + key
    request_url = url + 'keypress/' + key
    requests.post(request_url)
    return request_url

class HTTPResponse(dict):
    def __init__(self, response_text):

        response = response_text.split('\r\n')
        status_line = response[0].split()

        self.http_version = status_line[0]
        self.status_code = status_line[1]
        self.status = status_line[2]
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
        
        stdscr.addstr(0,0, 'Connected to %s!' % location)
        stdscr.addstr(1,0, 'escape: quit')
        stdscr.addstr(2,0, 'arrow keys: move cursor')
        stdscr.addstr(3,0, 'enter: select')
        stdscr.addstr(4,0, 'tab: go back')
        stdscr.refresh()
        
        key = ''
        while key != 27: # escape key
            key = stdscr.getch()
            stdscr.refresh()
            if key: 
                command = KEYPRESS_MAP.get(key, '')
                http = keypress(location, command)
    finally:
        curses.endwin()


if __name__ == '__main__':
    main()
