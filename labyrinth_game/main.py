# labyrinth_game/main.py

from labyrinth_game.constants import COMMANDS
from labyrinth_game.player_actions import (
    get_input,
    move_player,
    show_inventory,
    take_item,
    use_item,
)
from labyrinth_game.utils import (
    attempt_open_treasure,
    describe_current_room,
    show_help,
    solve_puzzle,
)


def process_command(game_state, command_line):
    parts = command_line.strip().lower().split()
    if not parts:
        return

    command = parts[0]
    arg = parts[1] if len(parts) > 1 else None

    match command:
        case "quit" | "exit":
            print("Вы вышли из игры.")
            game_state['game_over'] = True
        case "look" | "осмотреться":
            describe_current_room(game_state)
        case "inventory" | "инвентарь":
            show_inventory(game_state)
        case "go":
            if arg:
                move_player(game_state, arg)
            else:
                print("Укажите направление.")
        case "north" | "south" | "east" | "west":
            move_player(game_state, command)
        case "take":
            if arg:
                take_item(game_state, arg)
            else:
                print("Укажите предмет для взятия.")
        case "use":
            if arg:
                use_item(game_state, arg)
            else:
                print("Укажите предмет для использования.")
        case "solve":
            if game_state['current_room'] == "treasure_room":
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)
        case "help":
            show_help(COMMANDS)
        case _:
            print("Команда не распознана. Доступные команды:")
            for cmd, desc in COMMANDS.items():
                print(f"{cmd:<16} - {desc}")


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
