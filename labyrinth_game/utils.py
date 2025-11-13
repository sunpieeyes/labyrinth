# labyrinth_game/utils.py
import math

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

def pseudo_random(seed, modulo):
    x = math.sin(seed * 12.9898) * 43758.5453
    x = x - math.floor(x)
    return int(x * modulo)

def trigger_trap(game_state):
    print("Ловушка активирована! Пол стал дрожать...")
    inventory = game_state['player_inventory']
    if inventory:
        idx = pseudo_random(game_state['steps_taken'], len(inventory))
        lost_item = inventory.pop(idx)
        print(f"Вы потеряли предмет: {lost_item}")
    else:
        dmg = pseudo_random(game_state['steps_taken'], 10)
        if dmg < 3:
            print("Ловушка смертельна! Вы проиграли...")
            game_state['game_over'] = True
        else:
            print("Вы уцелели, но испугались...")

def random_event(game_state):
    if pseudo_random(game_state['steps_taken'], 10) != 0:
        return  # событие не произошло

    event_type = pseudo_random(game_state['steps_taken'], 3)
    current_room = game_state['current_room']
    room_data = ROOMS[current_room]

    if event_type == 0:
        print("На полу вы находите монетку!")
        room_data['items'].append("coin")
    elif event_type == 1:
        print("Вы слышите странный шорох...")
        if "sword" in game_state['player_inventory']:
            print("Вы отпугнули существо своим мечом.")
    elif event_type == 2:
        if current_room == "trap_room" and \
            "torch" not in game_state['player_inventory']:
            print("Опасность! Ловушка может сработать!")
            trigger_trap(game_state)

def solve_puzzle(game_state):
    current_room = game_state['current_room']
    room_data = ROOMS[current_room]

    if not room_data['puzzle']:
        print("Загадок здесь нет.")
        return

    question, answer = room_data['puzzle']
    print(question)
    user_answer = get_input("Ваш ответ: ").strip().lower()

    # Альтернативные варианты ответа
    correct_answers = [answer.lower()]
    if answer == "10":
        correct_answers.append("десять")

    if user_answer in correct_answers:
        print("Верно! Загадка решена.")
        room_data['puzzle'] = None
        if current_room == "treasure_room":
            game_state['player_inventory'].append("treasure_key")
            print("Вы получили treasure_key!")
    else:
        print("Неверно. Попробуйте снова.")
        if current_room == "trap_room":
            trigger_trap(game_state)

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

    use_code = get_input(
        "Сундук заперт. Хотите попробовать ввести код? (да/нет) "
    ).strip().lower()
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

def show_help(commands):
    print("\nДоступные команды:")
    for cmd, desc in commands.items():
        print(f"{cmd:<16} - {desc}")
