class Game:
    def __init__(self, id):
        self.p1Went = False
        self.p2Went = False
        self.ready = False
        self.id = id
        self.moves = [None, None]
        self.wins = [0,0]
        self.ties = 0

    def get_player_move(self, p):
        """
        :param p: [0,1]
        :return: Move
        """
        return self.moves[p]

    def play(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True

    def connected(self):
        return self.ready

    def bothWent(self):
        return self.p1Went and self.p2Went

    def winner(self):
        data = dict()
        data['R'] = 0
        data['P'] = 1
        data['S'] = 2

        p1 = self.moves[0].upper()[0]
        p2 = self.moves[1].upper()[0]

        if p1 == p2:
            return -1

        if (((data[p1] | 1 << (2)) - (data[p2] | 0 << (2))) % 3):
            return 0
        return 1

    def resetWent(self):
        self.p1Went = False
        self.p2Went = False
