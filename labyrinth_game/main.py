# labyrinth_game/main.py
from labyrinth_game.utils import describe_current_room, solve_puzzle, attempt_open_treasure
from labyrinth_game.player_actions import show_inventory, get_input, move_player, take_item, use_item

def process_command(game_state, command):
    parts = command.split()
    if not parts:
        return

    action = parts[0]
    arg = " ".join(parts[1:]) if len(parts) > 1 else ""

    match action:
        case "look" | "осмотреться":
            describe_current_room(game_state)
        case "inventory" | "инвентарь":
            show_inventory(game_state)
        case "go" | "идти":
            if arg:
                move_player(game_state, arg)
            else:
                print("Укажите направление.")
        case "take" | "взять":
            if arg == "treasure_chest":
                print("Вы не можете поднять сундук, он слишком тяжелый.")
            elif arg:
                take_item(game_state, arg)
            else:
                print("Укажите предмет.")
        case "use" | "использовать":
            if arg:
                use_item(game_state, arg)
            else:
                print("Укажите предмет.")
        case "solve":
            if game_state['current_room'] == 'treasure_room':
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)
        case "quit" | "exit":
            print("Вы вышли из игры.")
            game_state['game_over'] = True
        case _:
            print("Команда не распознана. Доступные команды: look, inventory, go, take, use, solve, quit")

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
        command = get_input("> ").lower()
        process_command(game_state, command)

if __name__ == "__main__":
    main()
