import curses
import time
from datetime import datetime
import math

def draw_clock(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)

    max_y, max_x = stdscr.getmaxyx()
    center_y, center_x = max_y // 2, max_x // 2
    radius_x, radius_y = min(20, max_x // 3), min(10, max_y // 3)

    while True:
        stdscr.clear()
        now = datetime.now()
        hour, minute, second = now.hour, now.minute, now.second

        for angle in range(0, 360, 6):
            x = center_x + int(radius_x * math.cos(math.radians(angle)))
            y = center_y + int(radius_y * math.sin(math.radians(angle)))
            if 0 <= x < max_x and 0 <= y < max_y:
                stdscr.addch(y, x, '*')

        hour_positions = {
            12: (center_x, center_y - radius_y + 2),
            1: (center_x + radius_x // 2, center_y - radius_y + 2),
            2: (center_x + radius_x - 4, center_y - radius_y // 2),
            3: (center_x + radius_x - 2, center_y),
            4: (center_x + radius_x - 4, center_y + radius_y // 2),
            5: (center_x + radius_x // 2, center_y + radius_y - 2),
            6: (center_x, center_y + radius_y - 2),
            7: (center_x - radius_x // 2, center_y + radius_y - 2),
            8: (center_x - radius_x + 3, center_y + radius_y // 2),
            9: (center_x - radius_x + 2, center_y),
            10: (center_x - radius_x + 4, center_y - radius_y // 2),
            11: (center_x - radius_x // 2, center_y - radius_y + 2),
        }
        
        for i, (hx, hy) in hour_positions.items():
            label = str(i)
            if 0 <= hx < max_x and 0 <= hy < max_y:
                stdscr.addstr(hy, hx - len(label) // 2, label, curses.color_pair(1))

        hour_angle = math.radians((hour % 12) * 30 + (minute / 2) - 90)
        minute_angle = math.radians(minute * 6 - 90)
        second_angle = math.radians(second * 6 - 90)

        def get_arrowhead_symbol(angle):
            if -math.pi / 4 <= angle < math.pi / 4:
                return '>'
            elif math.pi / 4 <= angle < 3 * math.pi / 4:
                return 'v'
            elif -3 * math.pi / 4 <= angle < -math.pi / 4:
                return '^'
            else:
                return '<'

        def draw_hand(angle, max_length, symbol, color_pair):
            for i in range(1, max_length):
                x = center_x + int(i * math.cos(angle))
                y = center_y + int(i * math.sin(angle))
                if abs(x - center_x) < radius_x - 2 and abs(y - center_y) < radius_y - 2:
                    stdscr.addch(y, x, symbol, color_pair)
                else:
                    break

            x_end = center_x + int((max_length - 1) * math.cos(angle))
            y_end = center_y + int((max_length - 1) * math.sin(angle))
            if abs(x_end - center_x) < radius_x - 2 and abs(y_end - center_y) < radius_y - 2:
                stdscr.addch(y_end, x_end, get_arrowhead_symbol(angle), color_pair)

        draw_hand(hour_angle, radius_x - 6, '-', curses.color_pair(2))
        draw_hand(minute_angle, radius_x - 4, '-', curses.color_pair(3))
        draw_hand(second_angle, radius_x - 3, '-', curses.color_pair(4))

        time_str = now.strftime("%H:%M:%S")
        time_y, time_x = center_y + radius_y + 2, center_x - len(time_str) // 2
        if 0 <= time_x < max_x and 0 <= time_y < max_y:
            stdscr.addstr(time_y, time_x, time_str)

        stdscr.refresh()
        time.sleep(1)

curses.wrapper(draw_clock)