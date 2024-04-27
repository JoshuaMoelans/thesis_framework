import json
import time
from GenericOptimizer import GenericOptimizer
from GameParameters import GameParameters
from numpy import *
import subprocess
import os

import nlopt

class GameOptimizer(GenericOptimizer):
    def __init__(self, game_location:str, logs_location:str, ingame_instance_count:int = 4, timeout:int = 60):
        """
        Initializes the GameOptimizer class.

        Parameters:
        - game_location (str): The location of the game executable.
        - input_location (str): The location of input files; used to set parameters for game run.
        - logs_location (str): The location to store logs; used to retrieve data from game run.
        - ingame_instance_count (int): The number of instances of the game to run in parallel.
        - timeout (int): The maximum time (seconds) to wait for a game instance to finish.
        """
        self.game_location = game_location
        self.logs_location = logs_location
        self.ingame_instance_count = ingame_instance_count # can be used to run multiple instances of the game in parallel;
        self.timeout = timeout
        self.parameters = GameParameters() # TODO think about setting up parameters? Is it OK to do this in Parameters.py?
        self.paramnames = [key for key in self.parameters.__dict__] # indexable list of parameter names

    def clean_logs(self):
        """cleans out the logs_location directory
        """
        for file in os.listdir(self.logs_location):
            file_path = os.path.join(self.logs_location, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)

    def run(self) -> float:
        """ runs the game with the stored internal parameters

        Returns:
            float: scoring of the game
        """
        print("Running game...")
        # self.clean_logs() # clean out logs_location directory

        # Run the game executable from game_location with the parameters as CL arguments
        # TODO we can parallelize this by running multiple instances of the game with different parameters? not sure if this speeds up learning
        # subprocess.run([self.game_location,
        #                  f"ngames={self.ingame_instance_count}",
        #                  f"timeout={self.timeout}",
        #                   "visible=true", # TODO make this parameter? think in training can be false
        #                 f"communication_count={self.parameters.communication_count}",
        #                 f"communication_delay={self.parameters.communication_delay}"
        #                 ])
        
        # gather results from logs_location and put in result array
        # loop over files in logs_location
        results = {}
        for file in sorted(os.listdir(self.logs_location)):
            file_path = os.path.join(self.logs_location, file)
            if os.path.isfile(file_path):
                if "TIMEOUT" in file or "GAMEOVER" in file: # check if file is a game result
                    instance_number = file.split('_')[2]  # Extract instance number from file name
                    if instance_number in results:
                        continue  # Skip this file if its instance has been processed (alphabetically; GAMEOVER has priority over TIMEOUT)
                    print("file_path:", file_path)
                    with open(file_path, "r") as f:
                        results[instance_number] = self.string_to_json(f.read())
        return self.score(results)

    def string_to_json(self, string:str) -> dict:
        """converts a string to a json object

        Args:
            string (str): string to convert

        Returns:
            dict: json object
        """
        return json.loads(string)

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
    
    def obj_func(self, x, grad):
        """objective function to minimize

        Args:
            x (_type_): current iteration parameter values
            grad (_type_): gradient (expected None! gradientless optimization)

        Returns:
            _type_: scoring of the current iteration
        """
        # update self.parameters with x
        # TODO measure iteration times to show data on graph?
        # TODO do we need to match parameter types? (e.g. int, float) can use rounding OR penalty function
        for i in range(self.parameters.size()):
            print("setting", self.paramnames[i], "to", x[i])
            setattr(self.parameters, self.paramnames[i], x[i])
        return self.run()
    
    def optimize(self, delta:float = 0.01):
        """Optimizes the game by running it multiple times, scoring each run and adjusting the parameters.

        Args:
            delta (float, optional): Relative tolerance on parameters. Defaults to 0.01.
        """
        super().optimize(delta) # TODO can we do this, or does nlopt object need additional game-specific setup?
        
