from network import Network
import pickle
import time

def print_moves(game, p):
    move1 = game.get_player_move(0)
    move2 = game.get_player_move(1)

    if not game.p1Went and not game.p2Went:
        print("Your move: Waiting")
        print("Opponent move: Waiting")
    if p == 0:
        if game.p1Went and not game.p2Went:
            print("Your move: ", move1)
            print("Opponent move: Waiting")
        elif game.p2Went and not game.p1Went:
            print("Your move: Waiting")
            print("Opponent move: Locked in")
        elif game.p1Went and game.p2Went:
            print("Your move: ", move1)
            print("Opponent move: ", move2)
    else:
        if game.p2Went and not game.p1Went:
            print("Your move: ", move2)
            print("Opponent move: Waiting ")
        elif game.p1Went and not game.p2Went:
            print("Your move: Waiting")
            print("Opponent move: Locked in")
        elif game.p1Went and game.p2Went:
            print("Your move: ", move2)
            print("Opponent move: ", move1)


choices = ["Rock", "Scissors", "Paper"]
def main():
    run = True

    n = Network()
    player = int(n.getP())
    print("You are player", player)

    while run:
        try:
            game = n.send("get")
        except:
            print("Couldn't get game")
            break

        if not game.connected():
            print("Waiting for a Player")
            time.sleep(1)
            continue

        print_moves(game, player)

        if game.bothWent():
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                print("You won!")
            elif game.winner() == -1:
                print("Tie Game!")
            else:
                print("You lost...")

            try:
                time.sleep(4)
                game = n.send("reset")
            except:
                print("Couldn't get game")
                break

        if game.connected():
            print("1 for rock\n2 for scissors\n3 for paper\nq for quit")
            choice = input()
            if choice == "":
                continue
            if player == 0 and not game.p1Went:
                n.send(choices[int(choice) - 1])
            elif player == 1 and not game.p2Went:
                n.send(choices[int(choice) - 1])

def menu_screen():
    run = False
    while run:
        choice = input("Type y to play\n")
        if choice == "y":
            run = False
    main()

while True:
    menu_screen()
