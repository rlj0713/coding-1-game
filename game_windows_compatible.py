import os
import msvcrt  # For real-time keypress detection on Windows

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

# Unicode icons (all double-width)
TURTLE = "\U0001F422"   # 🐢
ROCK = "\U0001FAA8 "     # 🪨
LEAF = "\U0001F343"     # 🍃
EMPTY = "\u2B1B"        # ⬛

# Draw the board
def draw_board():
    os.system("cls")  # Clear the terminal (Windows)
    for y in range(HEIGHT):
        row = ""
        for x in range(WIDTH):
            if player["x"] == x and player["y"] == y:
                row += TURTLE
            elif any(o["x"] == x and o["y"] == y for o in obstacles):
                row += ROCK
            elif any(c["x"] == x and c["y"] == y and not c["collected"] for c in collectibles):
                row += LEAF
            else:
                row += EMPTY
        print(row)
    print(f"Score: {player['score']}")
    print("Move with W/A/S/D, Q to quit")

# Check collectibles
def check_collectibles():
    for c in collectibles:
        if not c["collected"] and player["x"] == c["x"] and player["y"] == c["y"]:
            c["collected"] = True
            player["score"] += 1
            print("You collected a leaf!")

# Move player
def move_player(key):
    key = key.lower()
    if key == "w" and player["y"] > 0:
        if not any(o["x"] == player["x"] and o["y"] == player["y"]-1 for o in obstacles):
            player["y"] -= 1
    elif key == "s" and player["y"] < HEIGHT-1:
        if not any(o["x"] == player["x"] and o["y"] == player["y"]+1 for o in obstacles):
            player["y"] += 1
    elif key == "a" and player["x"] > 0:
        if not any(o["x"] == player["x"]-1 and o["y"] == player["y"] for o in obstacles):
            player["x"] -= 1
    elif key == "d" and player["x"] < WIDTH-1:
        if not any(o["x"] == player["x"]+1 and o["y"] == player["y"] for o in obstacles):
            player["x"] += 1

# Main game loop
draw_board()
while True:
    if msvcrt.kbhit():
        key = msvcrt.getch().decode("utf-8")
        if key.lower() == "q":
            print("Thanks for playing!")
            break
        move_player(key)
        check_collectibles()
        draw_board()
