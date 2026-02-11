import curses
import time

# Board setup
WIDTH, HEIGHT = 5, 5
player = {"x": 0, "y": 0, "score": 0}
collectibles = [
    {"x": 2, "y": 1, "collected": False},
    {"x": 4, "y": 3, "collected": False}
]
obstacles = [
    {"x": 1, "y": 2},
    {"x": 3, "y": 1}
]

# ASCII icons
PLAYER = "\U0001F422"     # 🐢
OBSTACLE = "\U0001FAA8 "   # 🪨 + space for alignment
LEAF = "\U0001F343"       # 🍃
EMPTY = ".."

# Draw the board
def draw_board(stdscr):
    stdscr.clear()
    for y in range(HEIGHT):
        row = ""
        for x in range(WIDTH):
            if player["x"] == x and player["y"] == y:
                row += PLAYER
            elif any(o["x"] == x and o["y"] == y for o in obstacles):
                row += OBSTACLE
            elif any(c["x"] == x and c["y"] == y and not c["collected"] for c in collectibles):
                row += LEAF
            else:
                row += EMPTY
        stdscr.addstr(y, 0, row)
    stdscr.addstr(HEIGHT + 1, 0, f"Score: {player['score']}")
    stdscr.addstr(HEIGHT + 2, 0, "Move with W/A/S/D, Q to quit")
    stdscr.refresh()

# Check collectibles
def check_collectibles():
    for c in collectibles:
        if not c["collected"] and player["x"] == c["x"] and player["y"] == c["y"]:
            c["collected"] = True
            player["score"] += 1

# Move player
def move_player(key):
    key = key.lower()
    if key == "w" and player["y"] > 0:
        if not any(o["x"] == player["x"] and o["y"] == player["y"]-1 for o in obstacles):
            player["y"] -= 1
    elif key == "s" and player["y"] < HEIGHT - 1:
        if not any(o["x"] == player["x"] and o["y"] == player["y"]+1 for o in obstacles):
            player["y"] += 1
    elif key == "a" and player["x"] > 0:
        if not any(o["x"] == player["x"]-1 and o["y"] == player["y"] for o in obstacles):
            player["x"] -= 1
    elif key == "d" and player["x"] < WIDTH - 1:
        if not any(o["x"] == player["x"]+1 and o["y"] == player["y"] for o in obstacles):
            player["x"] += 1

# Main function
def main(stdscr):
    curses.curs_set(0)        # Hide cursor
    stdscr.nodelay(True)      # Non-blocking input
    draw_board(stdscr)

    while True:
        try:
            key = stdscr.getkey()
        except:
            key = None  # No key pressed

        if key:
            if key.lower() == "q":
                break
            move_player(key)
            check_collectibles()
            draw_board(stdscr)

        time.sleep(0.05)  # small delay for CPU friendliness

curses.wrapper(main)
