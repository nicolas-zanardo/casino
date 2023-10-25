# This is a sample Python script.
import random
from inputimeout import inputimeout, TimeoutOccurred

from InitDatabase import *
from Player import *

level_player = 1
nbrPlayTotalAction = 3
stakeValid = None
error_stake: bool = False
player_stake: int = 0
player: Player | None
quit_game: bool = False
min_range: int = 1
max_range: int | None = None
timer_question = 0


def start():
    global player
    global quit_game
    username = setNamePlayer()
    player = statusPlayer(username)
    if player.getGain() <= 0:
        print("Vous n'avez plus d'agent")
        return
    displayRouleGame()
    while quit_game is not True:
        playGame(level_player)


def playGame(level):
    setMise()
    number = randomNumber(level)
    print(number)
    finSecretNumber(number)


def finSecretNumber(secret_number: int):
    nbr_tentative = 0

    while True:
        question_string = "\t- Je viens de penser à un nombre entre " + str(min_range) + " et " + str(
            max_range) + ". Devinez lequel ?\n"
        try:
            if nbr_tentative <= 3:
                player_response = inputimeout(prompt=question_string, timeout=5)
                if player_response.isdecimal():
                    if secret_number > int(player_response):
                        print("\t- Votre nbre est trop petit !\n")
                        nbr_tentative = nbr_tentative + 1
                        tentative = nbr_tentative - 3
                        print("\t- Il vous reste " + str(tentative * -1) + " essaie(s) !\n")
                        if nbr_tentative > 3:
                            print("Vous avez perdu, vous n'avez plus de tentative")
                            return
                    if secret_number < int(player_response):
                        print("\t- Votre nombre est trop grand !\n")
                        nbr_tentative = nbr_tentative + 1
                        tentative = nbr_tentative - 3
                        print("\t- Il vous reste " + str(tentative * -1) + " essaie(s) !\n")
                        if nbr_tentative > 3:
                            print("Vous avez perdu, vous n'avez plus de tentative")
                            return
                    if secret_number == int(player_response):
                        playerWin(nbr_tentative)
                        return
                    if nbr_tentative >= 3:
                        print("You loose vous avez plus de 3 essaies")
                        stayPlay()
                        return
                else:
                    print("You loose vous avez plus de 3 essaies")
                    stayPlay()
                    return
        except TimeoutOccurred:
            nbr_tentative = nbr_tentative + 1
            print('Vous avez mis plus de 10 seconde pour répondre')
            if nbr_tentative >= 3:
                print("You loose vous avez plus de 3 essaies")
                stayPlay()
                return


def playerWin(nbr_tentative):
    gain = 0
    print(nbr_tentative)
    match nbr_tentative:
        case 0:
            gain = int(player_stake * 2)
            gainUpdateWin(gain, player)
        case 1:
            gain = int(player_stake)
            gainUpdateWin(gain, player)
        case 2:
            gain = int(player_stake / 2)
            gainUpdateWin(gain, player)
    print("\t- Bingo " + str(
        player.getName()) + ", vous avez gagné en " + str(nbr_tentative + 1) + " coup(s) et vous avez emporté " + str(
        gain) + " € !\n")
    stayPlay(True)
    return gain


def stayPlay(player_win: bool = False):
    global quit_game
    global level_player
    while True:
        try:
            player_response = inputimeout(prompt="Voulez vus continuer [o/n]", timeout=60)
            if player_response == "o":
                quit_game = False
                if player_win:
                    level_player = level_player + 1
                    print("Bravo, vous passez au niveau " + str(level_player))
                return
            if player_response == "n":
                quit_game = True
                return
        except TimeoutOccurred:
            quit_game = True
            print("le jeux c'est déconnecté")
            return


def setMise():
    global player_stake
    try:
        response = input("\t- Le jeu commence, entrez votre mise : ?\n")
        player_stake = int(response)
        playerCanBeStake(player_stake)
    except:
        playerCanBeStake(player_stake, True)
    while player_stake < 1:
        if error_stake:
            while player_stake == 0:
                try:
                    response = input(
                        "\t- Le montant saisi n'est pas valide. Entrer SVP un montant entre 1 et " + str(
                            player.getGain()) +
                        "€ : ?\n")
                    player_stake = int(response)
                    playerCanBeStake(player_stake)
                except:
                    playerCanBeStake(player_stake, True)
        return player_stake


def playerCanBeStake(param_player_stake, throw_error: bool = False) -> bool:
    global player_stake
    global error_stake
    is_can_play = param_player_stake <= player.getGain() and not throw_error
    if is_can_play:
        error_stake = 0
        player_stake = param_player_stake
        gainUpdate(param_player_stake, player)
    else:
        error_stake = 1
        player_stake = 0
    return is_can_play


def statusPlayer(username: str) -> Player:
    global player
    player = findPlayer(username)
    if player is None:
        createPlayer(username, 10)
        player = findPlayer(username)
    return player


def setNamePlayer():
    username = input("Je suis Python. Quel est votre pseudo ? ")
    return str(username)


def newPlayer(username: str) -> Player:
    createPlayer(username, 10)
    return findPlayer(username)


def randomNumber(level):
    global max_range
    match level:
        case 1:
            max_range = 10
            return random.randint(1, 10)
        case 2:
            max_range = 20
            return random.randint(1, 10)
        case 3:
            max_range = 30
            return random.randint(1, 10)


def displayRouleGame():
    global player
    # print("-----------------------------------------------------------------------------------------------------------")
    print("\t- Hello " + player.getName() + " , vous avez " + str(
        player.getGain()) + "€, Très bien ! Installez vous SVP à la "
                            "table de pari.\n\t\t\t Je vous expliquerai "
                            "le principe du jeu : \n")
    # print("-----------------------------------------------------------------------------------------------------------")
    # print("\t- Att : vous avez le droit à " + str(nbrPlayTotalAction) + " essais !\n")
    # print("\t- Si vous devinez mon nombre dès le premier coup, vous gagnez le double de votre mise !\n")
    # print("\t- Si vous le devinez au 2è coup, vous gagnez exactement votre mise !\n")
    # print("\t- Si vous le devinez au 3è coup, vous gagnez la moitiè votre mise !\n  ")
    # print(" \t- Si vous ne le devinez pas au 3è coup, vous perdez votre mise")
    # print("\tvous avez le droit : ")
    # print("\t\t- de retenter votre chance avec l'argent qu'il vous reste pour reconquérir le level perdu.")
    # print("\t\t- de quitter le jeu.\n")
    # print("\t- Dès que vous devinez mon nombre : vous avez le droit de quitter le jeu et de partir avec vos gains OU "
    #       "\n\t\tde continuer le jeu en passant au level supérieur.\n  ")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
