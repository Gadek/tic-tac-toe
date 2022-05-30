from network import Network
import time

def print_moves(game, p):
    move1 = game.get_player_move(0)
    move2 = game.get_player_move(1)
    player_nickname_1 = game.names[0]
    player_nickname_2 = game.names[1]
    if p == 0:
        if game.p1Went and not game.p2Went:
            print("[{}] Your move: {}".format(player_nickname_1,move1))
            print("[{}] Opponent move: Waiting".format(player_nickname_2))
        elif game.p2Went and not game.p1Went:
            print("[{}] Your move: Waiting".format(player_nickname_1))
            print("[{}] Opponent move: Locked in".format(player_nickname_2))
        elif game.p1Went and game.p2Went:
            print("[{}] Your move: {}".format(player_nickname_1,move1))
            print("[{}] Opponent move: {}".format(player_nickname_2,move2))
        else:
            print("[{}] Your move: Waiting".format(player_nickname_1))
            print("[{}] Opponent move: Waiting".format(player_nickname_2))
    else:
        if game.p2Went and not game.p1Went:
            print("[{}] Your move: {}".format(player_nickname_2,move2))
            print("[{}] Opponent move: Waiting ".format(player_nickname_1))
        elif game.p1Went and not game.p2Went:
            print("[{}] Your move: Waiting".format(player_nickname_2))
            print("[{}] Opponent move: Locked in".format(player_nickname_1))
        elif game.p1Went and game.p2Went:
            print("[{}] Your move: {}".format(player_nickname_2, move2))
            print("[{}] Opponent move: {}".format(player_nickname_1, move1))
        else:
            print("[{}] Your move: Waiting".format(player_nickname_2))
            print("[{}] Opponent move: Waiting".format(player_nickname_1))

choices = ["Rock", "Scissors", "Paper"]
def main():
    name = input("Enter your nickname: ")
    n = Network()

    n.send("nick{}".format(name))
    player = int(n.getP())
    print("You are player", player)
    choice_made = False
    print("Waiting for your opponent")
    while True:
        try:
            game = n.send("get")
        except:
            print("Couldn't get game")
            break

        if not game.connected():
            continue

        if game.bothWent():
            print_moves(game, player)
            winner = game.winner()
            if (winner == 1 and player == 1) or (winner == 0 and player == 0):
                print("You won!\n")
            elif winner == -1:
                print("Tie Game!\n")
            else:
                print("You lost...\n")
            print("Ties: {}\n{} wins:{}\n{} wins:{}".format(game.ties,game.names[0],game.wins[0],game.names[1],game.wins[1]))
            try:
                time.sleep(3)
                game = n.send("reset")
                choice_made = False
            except:
                print("Couldn't reset game")
                break

        if game.connected() and not choice_made:
            try:
                game = n.send("get")
            except:
                print("Couldn't get game")
                break
            print_moves(game, player)
            print("1 for rock\n2 for scissors\n3 for paper")
            choice = input()
            if choice not in ["1","2","3"]:
                continue
            if player == 0 and not game.p1Went:
                n.send(choices[int(choice) - 1])
                choice_made = True
            elif player == 1 and not game.p2Went:
                n.send(choices[int(choice) - 1])
                choice_made = True
            try:
                game = n.send("get")
            except:
                print("Couldn't get game")
                break
            print_moves(game, player)
            print("----------------")

while True:
    main()
