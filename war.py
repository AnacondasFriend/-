import random
import copy

class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску!"


class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"


class BoardWrongShipException(BoardException):
    pass


class Dot:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Dot({self.x}, {self.y})"


class Ship:

    def __init__(self, length, nose, direct):
        self.length = length
        self.nose = nose
        self.direct = direct
        self.lives = length

    @property
    def dots(self):
        dots_list = []
        start_nose_x = self.nose.x
        start_nose_y = self.nose.y

        for i in range(self.length):
            if self.direct == "left":
                start_nose = start_nose_x - i
                dots_list.append(Dot(start_nose, start_nose_y))
            elif self.direct == "right":
                start_nose = start_nose_x + i
                dots_list.append(Dot(start_nose, start_nose_y))
            elif self.direct == "top":
                start_nose = start_nose_y - i
                dots_list.append(Dot(start_nose_x, start_nose))
            elif self.direct == "bottom":
                start_nose = start_nose_y + i
                dots_list.append(Dot(start_nose_x, start_nose))
        return dots_list


class Board:

    def __init__(self, hid=False):
        self.hid = hid
        self.ships_list = []
        self.matrix = [["▫" for self.x in range(6)] for self.y in range(6)]
        self.busy = []
        self.shooten = []
        self.killed_dots_counter = 0
    def show_matrix(self):
        if self.hid:
            mtrx = copy.deepcopy(self.matrix)
            for i in range(6):
                for j in range(6):
                    if mtrx[i][j] == '■':
                        mtrx[i][j]=mtrx[i][j].replace('■', "▫")
                    elif mtrx[i][j] == '.':
                        mtrx[i][j]=mtrx[i][j].replace('.', "▫")
            print("  1|2|3|4|5|6")
            for i in range(6):
                print(i + 1, '|'.join(mtrx[i]))
        else:
            print("  1|2|3|4|5|6")
            for i in range(6):
                print(i + 1, '|'.join(self.matrix[i]))

       # return self


    def add_ship(self, lng):

        i = 0
        orientation = {1: 'left', 2: 'right', 3: 'top', 4: 'bottom'}
        while not i:
            d = random.randint(1, 4)  # выбираем рандомное направление
            d_key = orientation.get(d)
            dot = Dot(random.randint(0, 5), random.randint(0, 5))  # генерируем рандомную начальную точку
            ship = Ship(lng, dot, d_key)
            list_with_dots = []  # список для координат
            j = 0
            for j in range(lng):
                dot = ship.dots[j]
                #print(dot)
                if not self.out(dot) and dot not in self.busy:
                    list_with_dots.append(dot)
                else:
                    list_with_dots.clear()

            #print(list_with_dots)
            if len(list_with_dots) == lng:
               # print('lng',lng)
                for k in range(lng):
                   # print('nk',k)
                    dot = list_with_dots[k]
                    self.matrix[dot.x][dot.y] = '■'
                    self.busy.append(dot)
            if len(list_with_dots) == lng:
                self.contour(ship)
                i = 1

    def out(self, dot):

        if dot.x > 5 or dot.x < 0 or dot.y > 5 or dot.y < 0:
            return True
        else:
            return False

    def contour(self, ship):
        start_dot = ship.dots[0]
        start_x = start_dot.x
        start_y = start_dot.y
        finish_dot = ship.dots[-1]
        finish_x = finish_dot.x
        finish_y = finish_dot.y

        list_with_near_dots = [Dot(start_x + 1, start_y + 1), Dot(start_x + 1, start_y - 1), Dot(start_x + 1, start_y),
                               Dot(start_x - 1, start_y + 1), Dot(start_x - 1, start_y - 1), Dot(start_x - 1, start_y),
                               Dot(finish_x + 1, finish_y + 1), Dot(finish_x + 1, finish_y - 1), Dot(finish_x + 1, finish_y),
                               Dot(finish_x - 1, finish_y + 1), Dot(finish_x - 1, finish_y - 1), Dot(finish_x - 1, finish_y),
                               Dot(finish_x, finish_y + 1), Dot(finish_x, finish_y - 1),
                               Dot(start_x, start_y + 1), Dot(start_x, start_y - 1)
                               ]
        list_l = len(list_with_near_dots)

        for i in range(0, list_l):
            dot = list_with_near_dots[i]
            if not self.out(dot) and dot not in self.busy:
                self.matrix[dot.x][dot.y] = '.'
                self.busy.append(dot)

    def shot(self, x, y):

        if self.out(Dot(x,y)) or Dot(x,y) in self.shooten:
            print("В эту точку нельзя стрелять")
            return True
        else:
            if self.matrix[x][y] == '■':
                self.matrix[x][y] = 'x'
                self.shooten.append(Dot(x,y))
                print('Есть пробитие!')
                print(self.show_matrix())
                self.killed_dots_counter +=1
                return True
            elif self.matrix[x][y] != '■':
                self.matrix[x][y] = 'т'
                print('Промах!')
                print(self.show_matrix())
                return False


class Player:
    def __init__(self, my, his):
        self.my = my
        self.his = his

    def ask(self):
        return 0

    def move(self):
        while True:
            dot = self.ask()
            self.his.shot(dot.x, dot.y)
            return True


class AI(Player):

    def ask(self):
        print('Ходит компьютер:')
        dot = Dot(random.randint(0, 5), random.randint(0, 5))
        return dot


class User(Player):

    def ask(self):
        x = int(input('Введите номер строки:'))
        y = int(input('Введите номер столбца:'))
        dot = Dot(x - 1, y - 1)
        return dot


class Game:

    def __init__(self):
        self.user_board = self.random_board()
        self.ai_board = self.random_board()
        self.ai_board.hid = True
        self.user = User(self.user_board, self.ai_board)
        self.ai = AI(self.ai_board, self.user_board)

    def random_board(self):
        try:
            board = Board()
            l_list = [3, 2, 2, 1, 1, 1]
            for i in range(len(l_list)):
                l_i = l_list[i]
                #print(l_i)
                board.add_ship(l_i)
        except IndexError:
            board.add_ship(l_i)


        return board

    def greet(self):
        print('Йохохо добро пожаловать в игру, капитан!')
        print('Сегодня вам предстоит сойтись якорями с одним искусственным интелектом. \nНо хочу вас заверить что от интелекта там одно слово: эта портовая крыса шмаляет неглядя направо и налево.')
        print('Правила простые: вводите координаты, а всю грязную работенку мы сделаем за вас.')
        print('Ну чтож, корабли уже расставлены. Пора начинать бой.')
        print('Ваша доска:')
        print(self.user_board.show_matrix())

        print('Доска врага:')
        print(self.ai_board.show_matrix())

    def loop(self):
        while True:
            self.user.move()
            if self.user_board.killed_dots_counter == 10:
                print('Человек победил!!!')
            self.ai.move()
            if self.ai_board.killed_dots_counter == 10:
                print('Буууу искуственный интеллект!!!')
    def start(self):
        self.greet()
        self.loop()


a = Game()
a.start()