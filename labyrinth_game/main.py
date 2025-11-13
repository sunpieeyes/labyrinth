# labyrinth_game/main.py
from labyrinth_game.utils import describe_current_room, solve_puzzle, attempt_open_treasure, show_help, random_event
from labyrinth_game.player_actions import show_inventory, get_input, move_player, take_item, use_item
from labyrinth_game.constants import COMMANDS

def process_command(game_state, command_line):
    parts = command_line.strip().lower().split(maxsplit=1)
    command = parts[0]
    arg = parts[1] if len(parts) > 1 else ""

    directions = ["north", "south", "east", "west"]

    # Движение односложными командами
    if command in directions:
        move_player(game_state, command)
        return

    match command:
        case "go":
            if arg in directions:
                move_player(game_state, arg)
            else:
                print("Неверное направление. Используйте north, south, east или west.")
        case "look" | "осмотреться":
            describe_current_room(game_state)
        case "inventory" | "инвентарь":
            show_inventory(game_state)
        case "take":
            if arg:
                take_item(game_state, arg)
            else:
                print("Укажите предмет, который хотите взять.")
        case "use":
            if arg:
                use_item(game_state, arg)
            else:
                print("Укажите предмет, который хотите использовать.")
        case "solve":
            if game_state['current_room'] == 'treasure_room':
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)
        case "help":
            show_help(COMMANDS)
        case "quit" | "exit":
            print("Вы вышли из игры.")
            game_state['game_over'] = True
        case _:
            print("Команда не распознана. Доступные команды:", ", ".join(COMMANDS.keys()))

def main():
    game_state = {
        'player_inventory': [],
        'current_room': 'entrance',
        'game_over': False,
        'steps_taken': 0
    }

    print("Добро пожаловать в Лабиринт сокровищ!")
    describe_current_room(game_state)

    while not game_state['game_over']:
        command = get_input("> ")
        process_command(game_state, command)

if __name__ == "__main__":
    main()
