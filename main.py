import sqlite3

# подключаем бд
conn = sqlite3.connect('players.db')
# создаем курсор
cursor = conn.cursor()

def abeme(win, lose):
    return 0

def end_game(name, result):
    global conn, cursor

    # вариант проигрыша
    if result < 0:
        print("Вы проиграли! с вас", abs(result), "мирасиков. Оплаченные за игру мирасики не учтены в этом числе.")
        cursor.execute("""
            UPDATE player
                SET lose = lose + 1
            WHERE name = '{}';
        """.format(name))
    else: # вариант выигрыша
        print("Вы выиграли", result, "мирасиков.")
        cursor.execute("""
            UPDATE player
                SET win = win + 1
            WHERE name = '{}';
        """.format(name))

    # измняем общую статистику выигрыша/проигрыша
    cursor.execute("""
        UPDATE player
            SET list = list + ({})
        WHERE name = '{}';
    """.format(result, name))

    # отправляем измененные данные
    conn.commit()


    return play_game()


def play_game():
    global conn, cursor

    question = input("Введите никнейм: ")

    # проверка на существование игрока
    cursor.execute \
    ("""SELECT * FROM player 
    WHERE "name" = '{}';""".format(question))
    result = cursor.fetchall()

    # регистрация если такого нет
    if len(result) > 0:
        name = question
    else:
        name = user_registration(question)

    # вывод всех игр
    for i in range(len(play_list)):
        print(i, "-", play_list[i][0], "ЦЕНА", play_list[i][2], "МИРАСИКОВ")

    # игрок вводит номер игры, если ввел не номер, то пускаем play_game заново
    try:
        question = int(input("Введите номер игры: "))

        # собираем инфу о игроке
        cursor.execute("""
            SELECT * FROM player WHERE name = '{}';
        """.format(name))

        player_data = cursor.fetchall()

        # играем игру и возвращаем после сообщение об окончании
        end_game(name, play_list[question][1](player_data[0][2], player_data[0][3]))
    except BaseException:
        print("Произошла ошибка игры или ваш номер игры был не верным. Вы можете вернуть деньги за выбранную игру")
        return play_game()

def init():
    global conn, cursor
    # подключаем бд
    conn = sqlite3.connect('players.db')
    # создаем курсор
    cursor = conn.cursor()

    # накатываем миграции, если их нет
    cursor.execute\
    ("""CREATE TABLE IF NOT EXISTS player(
        id INT PRIMARY KEY,
        "name" TEXT,
        win INT,
        lose INT,
        list INT);
    """)
    conn.commit()

    # запускаем игры
    play_game()

def user_registration(name):
    global conn, cursor

    # создаем пользователя
    cursor.execute("""
        INSERT INTO player("name", win, lose, list) VALUES ('{}', 0, 0, 0);
    """.format(name))

    conn.commit()

    return name

# список игр
play_list = [("АБЭМКА", abeme, 50)]

# запускаем игру
if __name__ == '__main__':
    init()
