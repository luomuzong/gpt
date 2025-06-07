import curses
import random


def main(stdscr):
    # Turn off cursor
    curses.curs_set(0)
    # Colors
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

    sh, sw = stdscr.getmaxyx()
    box = [[3, 3], [sh-3, sw-3]]

    # Draw border
    for x in range(box[0][1], box[1][1]):
        stdscr.addch(box[0][0], x, '#')
        stdscr.addch(box[1][0], x, '#')
    for y in range(box[0][0], box[1][0]):
        stdscr.addch(y, box[0][1], '#')
        stdscr.addch(y, box[1][1], '#')

    snake = [
        [sh//2, sw//2 + 1],
        [sh//2, sw//2],
        [sh//2, sw//2 - 1]
    ]
    direction = curses.KEY_RIGHT

    # Place first food
    food = [
        random.randint(box[0][0]+1, box[1][0]-1),
        random.randint(box[0][1]+1, box[1][1]-1)
    ]
    stdscr.addch(food[0], food[1], '*', curses.color_pair(1))

    score = 0
    stdscr.nodelay(True)

    while True:
        next_key = stdscr.getch()
        direction = direction if next_key == -1 else next_key

        head = snake[0].copy()
        if direction == curses.KEY_UP:
            head[0] -= 1
        elif direction == curses.KEY_DOWN:
            head[0] += 1
        elif direction == curses.KEY_LEFT:
            head[1] -= 1
        elif direction == curses.KEY_RIGHT:
            head[1] += 1
        else:
            continue

        # Check for collision with border
        if (head[0] in [box[0][0], box[1][0]] or
                head[1] in [box[0][1], box[1][1]] or
                head in snake):
            msg = f"Game Over! Score: {score}"
            stdscr.addstr(sh//2, sw//2 - len(msg)//2, msg)
            stdscr.nodelay(False)
            stdscr.getch()
            break

        snake.insert(0, head)
        if head == food:
            score += 1
            food = None
            while food is None:
                nf = [
                    random.randint(box[0][0]+1, box[1][0]-1),
                    random.randint(box[0][1]+1, box[1][1]-1)
                ]
                if nf not in snake:
                    food = nf
            stdscr.addch(food[0], food[1], '*', curses.color_pair(1))
        else:
            tail = snake.pop()
            stdscr.addch(tail[0], tail[1], ' ')

        stdscr.addch(head[0], head[1], '#')
        stdscr.refresh()
        curses.napms(100)


if __name__ == "__main__":
    curses.wrapper(main)

