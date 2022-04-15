import time
from random import randint


class Barrel:
    """ Возвращает случайный индекс, имитирующий случайную бочку в мешке """
    def __init__(self, min_index=0, max_index=89):
        self._barrel = randint(min_index, max_index)

    @property
    def barrel(self):
        return self._barrel


class Bag:
    """ Возвращает список с числами от 1 до 90, имитирующий мешок в лото """
    def __init__(self):
        bag = []
        for numb in range(1, 91):
            bag.append(numb)
        self._bag = bag

    @property
    def bag(self):
        return self._bag

    def __str__(self):
        return f"{self._bag!r}"


class Card:
    """ Формирование карточки игрока """
    _rows = 3               # Количество строк в карточке
    _columns = 9            # Количество столбцов в карточке
    _numb_in_rows = 5       # Количество чисел в строке
    _empty_column = 0       # Значение для определения пустого столбца
    _crossed_numb = -1      # Значение для определения зачёркнутого числа

    def __init__(self):
        numb_amount = self._numb_in_rows * self._rows
        _numb_in_rows = self.generate_numbs(numb_amount)

        self.card_list = []
        for i in range(0, self._rows):
            next_row = sorted(_numb_in_rows[self._numb_in_rows * i:self._numb_in_rows * (i+1)])  # Формирование строки по 5 чисел в порядке возрастания
            empty__columns = self._columns - self._numb_in_rows     # Количество пустых столбцов
            for j in range(0, empty__columns):
                index = randint(1, len(next_row))
                next_row.insert(index, self._empty_column)   # Случайное размещение пустых столбцов в строке
            self.card_list += next_row     # Список со всеми строками карточки

    def __str__(self):
        close_str = "--------------------------"
        next_row = ""
        for index, numb in enumerate(self.card_list):
            if numb == self._empty_column:
                next_row += "   "
            elif numb == self._crossed_numb:
                next_row += " - "
            elif numb < 10:
                next_row += f" {str(numb)} "
            else:
                next_row += f"{str(numb)} "

            if (index + 1) % self._columns == 0:
                next_row += "\n"

        return next_row + close_str

    def __contains__(self, numb):
        return numb in self.card_list

    def cross_num(self, num):
        """ Замещает зачёркнутое число соответствующим значением переменной класса """
        for index, item in enumerate(self.card_list):
            if item == num:
                self.card_list[index] = self._crossed_numb
                return
        raise ValueError(f"Номера нет в карточке: {num}")

    def closed(self) -> bool:
        """ Возвращает истину, если все числа в карточке зачёркнуты """
        return set(self.card_list) == {self._empty_column, self._crossed_numb}

    @staticmethod
    def generate_numbs(numb_amount, min_value=1, max_value=90):
        """ Формирует случайные числа в заданном количестве и диапазоне без повторений """
        numb_list = []
        while len(numb_list) < numb_amount:
            next_number = randint(min_value, max_value)
            if next_number not in numb_list:
                numb_list.append(next_number)
        return numb_list


class User:
    """ Определяет количество и тип игроков """
    def __init__(self):
        self._user_amount = 2
        self._user_type = ["Human", "Computer"]

    @property
    def user_amount(self):
        return self._user_amount

    @property
    def user_type(self):
        return self._user_type

    @user_amount.setter
    def user_amount(self, value: int):
        self._user_amount = value

    @user_type.setter
    def user_type(self, value: list):
        self._user_type = value


class Lotto:
    """ Класс для создания экземпляра игры лото """
    def __init__(self):
        self._user_amount = User().user_amount
        self._user_type = User().user_type
        self._bag = Bag().bag
        self._user_cards = []
        user_amount = int(input("Введите количество игроков: "))
        if user_amount > 1:
            self._user_amount = user_amount
        _user_type = list(input("Введите тип игроков через пробел (Human or Computer): ").split())
        if _user_type != self._user_type:
            self._user_type = _user_type
        for i in range(self._user_amount):
            self._user_card = Card()
            self._user_cards.append(self._user_card)

    def play(self) -> tuple:
        """ Реализует логику игры лото
         0, i: Проигрыш
         1, i: Выигрыш """
        max_index = len(self._bag) - 1
        barrel = Barrel(max_index=max_index).barrel
        barrel_numb = self._bag[barrel]
        self._bag.pop(barrel)
        print(f"Новый бочонок: {barrel_numb} (осталось {len(self._bag)})")
        human_count = self._user_type.count("Human")     # Количество людей в игре
        comp_count = self._user_type.count("Computer")  # Количество компьютеров в игре
        for i in range(len(self._user_cards)):
            if i < human_count:      # Сначала выводим все карточки людей
                if human_count == 1:
                    print(f"------ Ваша карточка -----\n{self._user_cards[i]}")
                else:
                    print(f"---- Карточка игрока {i+1} ---\n{self._user_cards[i]}")
            else:
                if comp_count == 1:
                    print(f"-- Карточка компьютера ---\n{self._user_cards[i]}")
                else:
                    i_tmp = i - human_count
                    print(f"-- Карточка компьютера {i_tmp+1} -\n{self._user_cards[i]}")

        for i in range(len(self._user_cards)):
            if i < human_count:     # Сначала опрашиваем людей
                if human_count == 1:
                    user_answer = input("Зачеркнуть цифру? (y/n) ")
                else:
                    user_answer = input(f"Игрок {i+1}, зачеркнуть цифру? (y/n) ")
                if user_answer == 'y' and barrel_numb not in self._user_cards[i] or \
                        user_answer != 'y' and barrel_numb in self._user_cards[i]:
                    return 0, i

                if barrel_numb in self._user_cards[i]:
                    self._user_cards[i].cross_num(barrel_numb)
                    if self._user_cards[i].closed():
                        return 1, i
            else:
                if barrel_numb in self._user_cards[i]:
                    self._user_cards[i].cross_num(barrel_numb)
                    if self._user_cards[i].closed():
                        return 0, i

    @property
    def user_type(self):
        return self._user_type


def main():
    lotto = Lotto()
    human_count = lotto.user_type.count("Human")
    while True:
        score = lotto.play()
        try:
            if score[0] == 1:
                if human_count == 1:
                    print("Вы выиграли")
                else:
                    print(f"Выиграл Игрок {score[1]+1}")
                break
            elif score[0] == 0:
                if human_count == 1:
                    print("Вы проиграли")
                elif human_count == 0:
                    print(f"Выиграл компьютер {score[1]+1}")
                else:
                    print(f"Проиграл Игрок {score[1]+1}")
                break
        except TypeError:
            print("Следующий ход")
            time.sleep(1)


if __name__ == '__main__':
    main()
