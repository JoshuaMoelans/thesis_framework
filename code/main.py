from GameOptimizer import GameOptimizer
from nlopt import LN_COBYLA, GN_MLSL

def test_score_reading(game:GameOptimizer):
    game.store_results()

if __name__ == '__main__':
    game_location = r"./game/game.exe"
    logs_location = r"C:\Users\Joshua\AppData\Roaming\Godot\app_userdata\Godot Exploration - 2d\logs"
    game = GameOptimizer(opt_algo=GN_MLSL, opt_algo_2=LN_COBYLA, game_location=game_location, logs_location=logs_location, ingame_instance_count=16, timeout=40)
    # test_score_reading(game) # TODO restructure this test
    
    game.optimize(delta=0.01)
    game.plot_data()