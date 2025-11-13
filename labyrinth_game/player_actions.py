# labyrinth_game/player_actions.py
from labyrinth_game.constants import ROOMS

def get_input(prompt="> "):
    try:
        return input(prompt).strip()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"

def show_inventory(game_state):
    inventory = game_state['player_inventory']
    if inventory:
        print("Инвентарь:", ", ".join(inventory))
    else:
        print("Инвентарь пуст.")

def move_player(game_state, direction):
    from labyrinth_game.utils import describe_current_room, random_event  # импорт внутри функции
    current_room = game_state['current_room']
    room_data = ROOMS[current_room]

    if direction in room_data['exits']:
        next_room = room_data['exits'][direction]

        # Проверка ключа для treasure_room
        if next_room == "treasure_room" and "rusty_key" not in game_state['player_inventory']:
            print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
            return
        elif next_room == "treasure_room":
            print("Вы используете найденный ключ, чтобы открыть путь в комнату сокровищ.")

        game_state['current_room'] = next_room
        game_state['steps_taken'] += 1
        print(f"Вы переместились в {next_room.upper()}.")
        describe_current_room(game_state)
        random_event(game_state)
    else:
        print("Нельзя пойти в этом направлении.")

def take_item(game_state, item_name):
    current_room = game_state['current_room']
    room_data = ROOMS[current_room]

    if item_name in room_data['items']:
        game_state['player_inventory'].append(item_name)
        room_data['items'].remove(item_name)
        print(f"Вы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")

def use_item(game_state, item_name):
    current_room = game_state['current_room']
    if item_name not in game_state['player_inventory']:
        print("У вас нет такого предмета.")
        return

    if item_name == "torch":
        print("Вы зажгли факел. Стало светлее.")
    elif item_name == "sword":
        print("Вы держите меч уверенно.")
    elif item_name == "bronze_box":
        print("Вы открыли бронзовую шкатулку.")
        if "rusty_key" not in game_state['player_inventory']:
            game_state['player_inventory'].append("rusty_key")
            print("Вы нашли rusty_key внутри шкатулки!")
    else:
        print("Вы не знаете, как использовать этот предмет.")
