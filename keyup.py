import curses
stdscr = curses.initscr()
stdscr.keypad(1)

stdscr.addstr(0,10,"Hit 'q' to quit")
stdscr.refresh()

key = ''
while key != ord('q'):
    key = stdscr.getch()
    stdscr.refresh()
    if key == curses.KEY_UP: 
        stdscr.addstr(2, 20, "Up")
    elif key == curses.KEY_DOWN: 
        stdscr.addstr(3, 20, "Down")

curses.endwin()
