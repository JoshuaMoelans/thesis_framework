from GameOptimizer import GameOptimizer

if __name__ == '__main__':
    game_location = "./game/game.exe"
    input_location = "C:\Users\Joshua\AppData\Roaming\Godot\app_userdata\Godot Exploration - 2d\input"
    logs_location = "C:\Users\Joshua\AppData\Roaming\Godot\app_userdata\Godot Exploration - 2d\logs"
    game = GameOptimizer(game_location, input_location, logs_location)
    game.optimize()