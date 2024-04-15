from GenericOptimizer import GenericOptimizer
import subprocess

class GameOptimizer(GenericOptimizer):
    def __init__(self, game_location:str, input_location:str, logs_location:str, ingame_instance_count:int = 4):
        """
        Initializes the GameOptimizer class.

        Parameters:
        - game_location (str): The location of the game executable.
        - input_location (str): The location of input files; used to set parameters for game run.
        - logs_location (str): The location to store logs; used to retrieve data from game run.
        """
        super().__init__()
        self.game_location = game_location
        self.input_location = input_location
        self.logs_location = logs_location
        self.ingame_instance_count = ingame_instance_count # can be used to run multiple instances of the game in parallel;
        # TODO check https://forum.godotengine.org/t/how-can-i-run-my-game-with-parameters-command-line-arguments/23263/2 to dynamically set parameters in Godot

    def run(self, parameters:dict) -> float:
        """ runs the game with the given parameters

        Args:
            parameters (dict): list of parameters to run the game with

        Returns:
            float: scoring of the game
        """
        print("Running game...")
        # set the parameters in the input_location


        # Run the game executable from game_location with the parameters
        # TODO use self.ingame_instance_count to run multiple instances of the game in parallel (using CL arguments)
        subprocess.run([self.game_location]) # TODO we can parallelize this by running multiple instances of the game with different parameters?
        # TODO think about when to stop the game? can use _on_time_out_timeout() in Godot to get_tree().quit()
        # + write final results for each instance to logs_location  (in Godot)
        
        # gather results from logs_location and put in result array

        result = []
        return self.score(result)


    def score_game(self, game_results:dict) -> float:
        """scores the results of the game; 
        do this here to more easily change scoring function (instead of baking it into the game)

        Args:
            game_results (dict): dictionary containing data gathered from game run

        Returns:
            float: scoring of the game for given set of parameters
        """
        print("Scoring game...")
        score:float = 0.0
        # TODO weighted score of different metrics found in log
        return score
    
    def score(self, results: list[dict]) -> float:
        """scores the results of the game; 
        do this here to more easily change scoring function (instead of baking it into the game)

        Args:
            results (list[dict]): list of dictionaries containing data gathered from all game runs

        Returns:
            float: scoring of all the games for given set of parameters
        """
        print("Scoring game...")
        score:float = 0.0
        # TODO weighted score?
        for instance_result in results:
            score += self.score_game(instance_result)
        return score

    def optimize(self, delta:float = 0.1):
        """optimizes the game by running it multiple times, scoring each run and adjusting the parameters.
        goes until change in scoring is less than delta

        Args:
            delta (float, optional): minimal change required to keep adjusting parameters. Defaults to 0.1.
        """
        print("Optimizing game...")
        # Do some optimization here
        self.run({})
        print("Game optimized!")