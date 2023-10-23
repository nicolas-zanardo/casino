# This is a sample Python script.
import random

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pymysql.cursors

# Connect to the database
from InitDatabase import *
from random import randint

niv = 1


def start():
    print("start casino")
    username = setNamePlayer()
    player = findPlayer(username)
    if player is None:
        createPlayer(username, 10)
        player = findPlayer(username)


def setNamePlayer():
    username = input("Je suis Python. Quel est votre pseudo ?")
    return str(username)


def newPlayer(username):
    createPlayer(username, 10)
    return findPlayer(username)


def randomNumber(niv):
    match niv:
        case 1:
            random.randint(0, 10)
        case 2:
            random.randint(0, 20)
        case 3:
            random.randint(0, 30)
        case _:
            random.randint(0, 9999999)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
