from Homework_2.MyLotto import Card, User
from pytest import fixture, raises, mark, param
from random import choice


@fixture
def card_instance():
    card = Card()
    return card, card.card_list  # Возвращем экземпляр класса и список


@fixture
def user_instance():
    user = User()
    return user


def exception_list(numb_list):
    """ Возвращает список из чисел, исключая числа из передаваемого списка """
    result_list = []
    for i in range(1, 91):
        if i not in numb_list:
            result_list.append(i)
    return result_list


class TestCard:
    def test_contain(self, card_instance):
        num = choice(card_instance[1])  # Выбираем случайное число из карточки
        assert num in card_instance[0]

    def test_cross_num(self, card_instance):
        num = choice(card_instance[1])
        res = card_instance[0].cross_num(num)
        assert res == -1

    def test_cross_num__raises(self, card_instance):
        except_card_list = exception_list(card_instance[1])
        num = choice(except_card_list)
        with raises(ValueError) as exc_info:
            card_instance[0].cross_num(num)

        assert str(exc_info.value) == f"Номера нет в карточке: {num}"

    def test_closed(self, card_instance):
        for num in card_instance[1]:
            if num != 0:
                card_instance[0].cross_num(num)
        res = card_instance[0].closed()
        assert res


class TestUser:
    @mark.parametrize("amount, expected_value", [param(4, 4, id="amount_id")])
    def test_user_amount(self, user_instance, amount, expected_value):
        user_instance.user_amount = amount
        assert user_instance.user_amount == expected_value

    @mark.parametrize("user_type, expected_value", [param(["Human", "Computer", "Human"],
                                                          ["Human", "Computer", "Human"],
                                                          id="type_id")])
    def test_user_type(self, user_instance, user_type, expected_value):
        user_instance.user_type = user_type
        assert user_instance.user_type == expected_value
