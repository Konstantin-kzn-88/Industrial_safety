class Game:
    def __init__(self):
        print("Запуск Tic Tac Toe")
        self.players_sticker = ["X", "O"]  # player №1 always "X", player №2 always "O"
        self.field_play = [
            1, 2, 3,
            4, 5, 6,
            7, 8, 9,
        ]
        self.player_id = 0  # Player №1 (index 0) goes first and he always 'X'
        self.win = False

    def play(self):
        print("Начинаем игру Tic Tac Toe!")
        print("Игрок №1 ходит первым и он всегда 'X'")
        # показать поле
        self.show_field()

        while self.win is False:

            # проверка на ничью
            is_draw = self.draw()
            if is_draw is True:
                print("У нас ничья!")
                break


            # если ничьи нет продолжаем игру
            print("_" * 30)
            print("_" * 30)
            print(f'Ход игрока №{self.player_id + 1}')

            try:

                select_field = int(input("Ведите № поля 1-9 (исключая занятые): "))
                if str(self.field_play[select_field - 1]).isdigit() is False:
                    print("Поле уже занято. Попробуйте еще раз!")
                    continue
                else:
                    self.field_play[select_field - 1] = self.players_sticker[self.player_id]
                    # показать поле
                    self.show_field()
                    # проверка победы
                    self.win = self.winner()
                    if self.win:
                        print(f'Победил игрок №{self.player_id + 1}')
                        break
                    # Смена игрока
                    if self.player_id == 0:
                        self.player_id = 1
                    else:
                        self.player_id = 0

            except:
                print("Что-то не то Вы ввели. Попробуйте еще раз!")
                continue

    def show_field(self):
        "Отобразить текущее положение"
        print("_" * 10, "Диспозиция", "_" * 10)
        print("-" * 13)
        for i in range(3):
            print("|", self.field_play[0 + i * 3], "|", self.field_play[1 + i * 3], "|",
                  self.field_play[2 + i * 3], "|")
            print("-" * 13)
        print("_" * 10, "Диспозиция", "_" * 10)

    def winner(self):
        "Победа"
        win_coord = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
        for each in win_coord:
            if self.field_play[each[0]] == self.field_play[each[1]] == self.field_play[each[2]]:
                return True
        return False

    def draw(self):
        "Остались ли на поле числа? Если нет то ничья"
        for each in self.field_play:
            if str(each).isdigit():
                return False
        return True


if __name__ == '__main__':
    game = Game().play()
