# labyrinth_game/player_actions.py

from labyrinth_game.constants import ROOMS


def get_input(prompt="> "):
    try:
        return input(prompt).strip()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def move_player(game_state, direction):
    from labyrinth_game.utils import describe_current_room, random_event

    current_room = game_state['current_room']
    room_data = ROOMS[current_room]

    if direction not in room_data['exits']:
        print("Нельзя идти в этом направлении.")
        return

    next_room = room_data['exits'][direction]

    # Проверка ключа для treasure_room
    if next_room == "treasure_room" and \
    "rusty_key" not in game_state['player_inventory']:
        print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
        return
    elif next_room == "treasure_room":
        print("Вы используете найденный ключ, чтобы открыть путь в комнату сокровищ.")

    game_state['current_room'] = next_room
    print(f"Вы переместились в {next_room.upper()}.")

    describe_current_room(game_state)
    random_event(game_state)


def take_item(game_state, item_name):
    current_room = game_state['current_room']
    room_data = ROOMS[current_room]

    if item_name in room_data['items']:
        game_state['player_inventory'].append(item_name)
        room_data['items'].remove(item_name)
        print(f"Вы подняли {item_name}.")
    else:
        print("Такого предмета здесь нет.")


def use_item(game_state, item_name):
    if item_name not in game_state['player_inventory']:
        print("У вас нет такого предмета.")
        return

    print(f"Вы использовали {item_name}.")


def show_inventory(game_state):
    inventory = game_state['player_inventory']
    if inventory:
        print("Ваш инвентарь:", ", ".join(inventory))
    else:
        print("Инвентарь пуст.")
