import subprocess
from GameOptimizer import GameOptimizer
from nlopt import LN_COBYLA, GN_MLSL

def test_score_reading(game:GameOptimizer):
    game.store_results()

def test_run_game(game_loc, inst_count, timeout, comm_count, comm_delay):
    subprocess.run([game_loc,
                f"ngames={inst_count}",
                f"timeout={timeout}",
                "visible=false",
                f"start_minimized=true",  # minimize the game window upon start
                f"communication_count={comm_count}",
                f"communication_delay={comm_delay}"
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) # silence output for now TODO maybe add verbosity parameter/parse into file?) 
        

if __name__ == '__main__':
    game_location = r"./game/game.exe"
    logs_location = r"C:\Users\Joshua\AppData\Roaming\Godot\app_userdata\Godot Exploration - 2d\logs" # desktop
    # logs_location = r"C:\Users\user\AppData\Roaming\Godot\app_userdata\Godot Exploration - 2d\logs" # laptop
    game = GameOptimizer(opt_algo=GN_MLSL, opt_algo_2=LN_COBYLA, game_location=game_location, logs_location=logs_location, ingame_instance_count=25, timeout=45)
    # game = GameOptimizer(opt_algo=LN_COBYLA, game_location=game_location, logs_location=logs_location, ingame_instance_count=16, timeout=35)
    # test_score_reading(game) # TODO restructure this test
    
    game.optimize(xtol_rel=0.1, ftol_rel=0.1, maxeval=30)
    game.plot_data()
    game.store_data()