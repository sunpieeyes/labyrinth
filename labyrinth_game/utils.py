# labyrinth_game/utils.py
from labyrinth_game.constants import ROOMS
from labyrinth_game.player_actions import get_input

def describe_current_room(game_state):
    current_room = game_state['current_room']
    room_data = ROOMS[current_room]

    print(f"\n== {current_room.upper()} ==")
    print(room_data['description'])

    if room_data['items']:
        print("Заметные предметы:", ", ".join(room_data['items']))
    
    print("Выходы:", ", ".join(room_data['exits'].keys()))

    if room_data['puzzle']:
        print("Кажется, здесь есть загадка (используйте команду solve).")

def solve_puzzle(game_state):
    current_room = game_state['current_room']
    room_data = ROOMS[current_room]

    if not room_data['puzzle']:
        print("Загадок здесь нет.")
        return

    question, answer = room_data['puzzle']
    print(question)
    user_answer = get_input("Ваш ответ: ").strip().lower()

    if user_answer == answer.lower():
        print("Верно! Загадка решена.")
        room_data['puzzle'] = None
        if current_room == "treasure_room":
            game_state['player_inventory'].append("treasure_key")
            print("Вы получили treasure_key!")
    else:
        print("Неверно. Попробуйте снова.")

def attempt_open_treasure(game_state):
    current_room = game_state['current_room']
    room_data = ROOMS[current_room]

    if 'treasure_chest' not in room_data['items']:
        print("Сундука здесь нет.")
        return

    if 'treasure_key' in game_state['player_inventory']:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        room_data['items'].remove('treasure_chest')
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
        return

    use_code = get_input("Сундук заперт. Хотите попробовать ввести код? (да/нет) ").strip().lower()
    if use_code != "да":
        print("Вы отступаете от сундука.")
        return

    if room_data['puzzle']:
        _, correct_code = room_data['puzzle']
        user_code = get_input("Введите код: ").strip()
        if user_code == correct_code:
            print("Код верный! Сундук открыт!")
            room_data['items'].remove('treasure_chest')
            print("В сундуке сокровище! Вы победили!")
            game_state['game_over'] = True
        else:
            print("Неверный код.")
    else:
        print("Сундук невозможно открыть кодом.")

def show_help():
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
