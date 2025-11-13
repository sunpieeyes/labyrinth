# labyrinth_game/player_actions.py
from .constants import ROOMS
from .utils import describe_current_room


def show_inventory(game_state):
    inventory = game_state['player_inventory']
    if inventory:
        print("Ваш инвентарь:", ", ".join(inventory))
    else:
        print("Инвентарь пуст.")

def get_input(prompt="> "):
    try:
        return input(prompt).strip()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"

def move_player(game_state, direction):
    current_room = game_state['current_room']
    exits = ROOMS[current_room]['exits']

    if direction in exits:
        new_room = exits[direction]
        game_state['current_room'] = new_room
        game_state['steps_taken'] += 1
        print(f"Вы переместились в {direction.upper()}.\n")
        describe_current_room(game_state)
    else:
        print("Нельзя пойти в этом направлении.")

def take_item(game_state, item_name):
    current_room = game_state['current_room']
    room_items = ROOMS[current_room]['items']

    if item_name in room_items:
        game_state['player_inventory'].append(item_name)
        room_items.remove(item_name)
        print(f"Вы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")

def use_item(game_state, item_name):
    if item_name not in game_state['player_inventory']:
        print("У вас нет такого предмета.")
        return

    if item_name == 'torch':
        print("Вы зажгли факел. Стало светлее.")
    elif item_name == 'sword':
        print("Вы держите меч уверенно в руках. Чувствуете силу.")
    elif item_name == 'bronze_box':
        if 'rusty_key' not in game_state['player_inventory']:
            game_state['player_inventory'].append('rusty_key')
            print("Вы открыли бронзовую шкатулку и нашли ржавый ключ!")
        else:
            print("Бронзовая шкатулка пустая.")
    else:
        print(f"Вы не знаете, как использовать {item_name}.")
