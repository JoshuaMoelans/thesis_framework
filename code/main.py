from GameOptimizer import GameOptimizer

if __name__ == '__main__':
    game_location = r"./game/game.exe"
    input_location = r"C:\Users\Joshua\AppData\Roaming\Godot\app_userdata\Godot Exploration - 2d\input"
    logs_location = r"C:\Users\Joshua\AppData\Roaming\Godot\app_userdata\Godot Exploration - 2d\logs"
    game = GameOptimizer(game_location, input_location, logs_location, 9)
    game.optimize()