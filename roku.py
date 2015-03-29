import requests
import curses
import socket
import re

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
    request_url = url + '/keypress/' + key
    # requests.post()
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
    # response_text = find_roku()
    # response = HTTPResponse(response_text)
    # location = response.headers['location']

    test  = 'Host: 192.168.1.247:8060'
    r = re.search('(?:[0-9]{1,3}\.){3}[0-9]{1,3}', test)
    host = r.group(0)
    r = re.search('(?<=:)[0-9]{4}', test)
    port = r.group(0)
    assert host == '192.168.1.247'
    assert port == '8060'
    command = 'up'
    url = 'http://{}:{}'.format(host, port)
    print keypress(url, command)

    # stdscr = curses.initscr()
    # stdscr.keypad(1)
    # 
    # stdscr.addstr(0,10,"Hit 'q' to quit")
    # stdscr.refresh()
    # 
    # key = ''
    # while key != ord('q'):
    #     key = stdscr.getch()
    #     stdscr.refresh()
    #     if key == curses.KEY_UP: 
    #         stdscr.addstr(2, 20, "Up")
    #     elif key == curses.KEY_DOWN: 
    #         stdscr.addstr(3, 20, "Down")
    # 
    # curses.endwin()


if __name__ == '__main__':
    main()
