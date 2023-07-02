import random

class Ship:
    def __init__(self, points):
        self.points = points

class Board:
    def __init__(self, ships, size):
        self.ships = ships
        self.size = size
        self.board = [['О' for _ in range(self.size)] for _ in range(self.size)]
        self.hits = set()

    def place_ships(self):
        for ship in self.ships:
            for point in ship.points:
                row, col = point
                self.board[row][col] = '■'

    def print_board(self, hide_ships=True):
        print("   ", end="")
        for col in range(self.size):
            print(f"| {col + 1} ", end="")
        print("|")
        print("-----" * self.size)

        for row in range(self.size):
            print(f"{row + 1:2} |", end="")
            for col in range(self.size):
                if hide_ships and self.board[row][col] == '■':
                    print(" О ", end=" ")
                else:
                    print(f" {self.board[row][col]} ", end=" ")
            print("|")

        print("-----" * self.size)

    def receive_attack(self, row, col):
        if (row, col) in self.hits:
            raise ValueError("Эта клетка уже выбрана!")

        self.hits.add((row, col))

        if self.board[row][col] == '■':
            self.board[row][col] = 'X'
            print("Попадание!")
            return True
        else:
            self.board[row][col] = 'T'
            print("Промах!")
            return False

    def game_over(self):
        for row in self.board:
            if '■' in row:
                return False
        return True

class Game:
    def __init__(self, size):
        self.size = size
        self.player_board = None
        self.computer_board = None

    def setup(self):
        # Создаем корабли для игрока
        player_ship1 = Ship([(0, 0), (0, 1), (0, 2)])  # 3-палубный корабль
        player_ship2 = Ship([(1, 4), (1, 5)])  # 2-палубный корабль
        player_ship3 = Ship([(3, 0), (3, 2), (3, 4), (3, 5)])  # 4-палубный корабль
        player_ship4 = Ship([(4, 4)])  # 1-палубный корабль
        player_ship5 = Ship([(5, 1), (5, 3)])  # 2-палубный корабль
        player_ship6 = Ship([(6, 0), (6, 2), (6, 4), (6, 5)])  # 4-палубный корабль

        # Создаем корабли для компьютера
        computer_ship1 = Ship([(0, 0), (1, 0), (2, 0)])  # 3-палубный корабль
        computer_ship2 = Ship([(4, 1), (4, 2)])  # 2-палубный корабль
        computer_ship3 = Ship([(0, 3), (1, 3), (2, 3), (3, 3)])  # 4-прядный корабль
        computer_ship4 = Ship([(2, 5)]) # 1-палубный корабль
        computer_ship5 = Ship([(4, 4), (5, 4)]) # 2-палубный корабль
        computer_ship6 = Ship([(0, 6), (1, 6), (2, 6), (3, 6)]) # 4-палубный корабль
        # Создаем игровые доски
        self.player_board = Board([player_ship1, player_ship2, player_ship3, player_ship4, player_ship5, player_ship6],
                                  self.size)
        self.computer_board = Board(
            [computer_ship1, computer_ship2, computer_ship3, computer_ship4, computer_ship5, computer_ship6], self.size)
        # Размещаем корабли на досках
        self.player_board.place_ships()
        self.computer_board.place_ships()

    def player_turn(self):
        print("Ваша очередь!")
        row = int(input("Введите номер строки: ")) - 1
        col = int(input("Введите номер столбца: ")) - 1

        try:
            hit = self.computer_board.receive_attack(row, col)
            self.computer_board.print_board()
            if hit:
                print("Вы попали по кораблю противника!")
                if self.computer_board.game_over():
                    print("Поздравляем! Вы победили!")
                    return False
            else:
                print("Вы промахнулись.")

            return True
        except ValueError as e:
            print(e)
            return self.player_turn()

    def computer_turn(self):
        print("Ход компьютера:")
        row = random.randint(0, self.size - 1)
        col = random.randint(0, self.size - 1)

        try:
            hit = self.player_board.receive_attack(row, col)
            self.player_board.print_board()
            if hit:
                print("Компьютер попал по вашему кораблю!")
                if self.player_board.game_over():
                    print("К сожалению, вы проиграли.")
                    return False
            else:
                print("Компьютер промахнулся.")

            return True
        except ValueError as e:
            return self.computer_turn()

    def play_game(self):
        print("Добро пожаловать в Морской Бой!")
        self.setup()

        while True:
            if not self.player_turn():
                break
            if not self.computer_turn():
                break

        print("Игра завершена.")
game = Game(7)
game.setup()
game.play_game()