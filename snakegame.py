from pynput import keyboard
import random
import time
import os


# Base to generate new body nodes
class Node:

    def __init__(self, y, x):
        self.y = y
        self.x = x


# Class used to generate new random positions as necessary
class Food:
    @staticmethod
    def pop():
        poppos = [0, 0]
        poppos[0] = random.randint(0, len(game_map) - 1)
        poppos[1] = random.randint(0, len(game_map[0]) - 1)
        return poppos


# Base for movement control
class Move:
    pos = [3, 3]
    right = [0, 1]
    left = [0, -1]
    up = [-1, 0]
    down = [1, 0]
    direction = down
    thread = 0


# Where the real movement control happens
def press(key):
    if key == keyboard.Key.left:
        Move.direction = Move.left
    elif key == keyboard.Key.right:
        Move.direction = Move.right
    elif key == keyboard.Key.up:
        Move.direction = Move.up
    elif key == keyboard.Key.down:
        Move.direction = Move.down


def release(key):
    Move.thread = 0
    return False


# base map of the game. Obs: you can modify it as you please. Only pay attention to ratio
game_map = [['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-']]

# List used to show the game map
frame = []

# The var that keeps the food position
food = [1, 3]

# This var is where are generated body nodes
body = []

inic = input("Snake Game\nPressione enter para iniciar")
# The game happens inside this while loop
while True:
    # Makes threads so that listen to user' keyboard(movement control) in a non-blocking way
    listener = keyboard.Listener(on_press=press, on_release=release)
    if Move.thread == 0:
        listener.start()
        Move.thread = 1

    # Animation effect
    os.system("cls")
    # Generates the map actually used in the game
    for row in game_map:
        frame.append(row[:])

    # Makes the "food" pop up in the generated map
    frame[food[0]][food[1]] = '+'

    # Manages all the body nodes, and makes them follow the head
    if len(body) > 0:
        if len(body) > 1:
            for i in range(len(body) - 1, 0, -1):
                body[i].y = body[i - 1].y
                body[i].x = body[i - 1].x
                frame[body[i].y][body[i].x] = '*'

        body[0].y = Move.pos[0]
        body[0].x = Move.pos[1]
        frame[body[0].y][body[0].x] = '*'

    # Computes movement, and also it manages the endless map effect
    Move.pos[0] += Move.direction[0]
    Move.pos[1] += Move.direction[1]
    if Move.pos[0] > len(frame) - 1:
        Move.pos[0] = 0
    if Move.pos[0] < 0:
        Move.pos[0] = len(frame) - 1
    if Move.pos[1] > len(frame[0]) - 1:
        Move.pos[1] = 0
    if Move.pos[1] < 0:
        Move.pos[1] = len(frame[0]) - 1
    # "You crashed, game over!", it breaks the loop
    if frame[Move.pos[0]][Move.pos[1]] == "*":
        break

    # Generates a new position for "food" whenever you get the food, and also generates
    # a new body node(it's-growing-up effect)
    if frame[Move.pos[0]][Move.pos[1]] == "+":
        if len(body) > 0:
            body.append(Node(body[-1].y - 1, body[-1].x - 1))
        else:
            body.append(Node(Move.pos[0] - 1, Move.pos[1] - 1))
        food = Food.pop()

    # Here, the actual movement is make
    frame[Move.pos[0]][Move.pos[1]] = '*'

    # Shows the frame created
    for g in frame:
        for i in g:
            print(i, end=" ")
        print("\n")
    # Reuse the same list while program is running
    frame.clear()
    # Animation speed
    time.sleep(1)
# the loop breaks and the game ends
print("Game Over!")
