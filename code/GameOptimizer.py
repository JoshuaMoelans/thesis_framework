import json
import time

from matplotlib import pyplot as plt
from GenericOptimizer import GenericOptimizer
from GameParameters import GameParameters
import numpy as np
import subprocess
import subprocess as sp
import os

import nlopt

class GameOptimizer(GenericOptimizer):
    def __init__(self, opt_algo=nlopt.LN_COBYLA, opt_algo_2 = None, game_location:str = "", logs_location:str = "", ingame_instance_count:int = 4, timeout:int = 60):
        """
        Initializes the GameOptimizer class.

        Parameters:
        - game_location (str): The location of the game executable.
        - input_location (str): The location of input files; used to set parameters for game run.
        - logs_location (str): The location to store logs; used to retrieve data from game run.
        - ingame_instance_count (int): The number of instances of the game to run in parallel.
        - timeout (int): The maximum time (seconds) to wait for a game instance to finish.
        """
        super().__init__(opt_algo, opt_algo_2)
        self.game_location = game_location
        self.logs_location = logs_location
        self.ingame_instance_count = ingame_instance_count # can be used to run multiple instances of the game in parallel;
        self.timeout = timeout
        self.parameters = GameParameters()
        self.paramnames = [key for key in self.parameters.__dict__] # indexable list of parameter names
        # set up data collection
        self.data = [] # keep track of data for graphing; one entry per iteration
        self.parameter_evolution = [] # keep track of parameter values for graphing; one entry per iteration

    def clean_logs(self):
        """cleans out the logs_location directory
        """
        for file in os.listdir(self.logs_location):
            file_path = os.path.join(self.logs_location, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)

    def store_results(self) -> dict:
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
                                results[instance_number] = json.loads(f.read())
        return results

    def run(self) -> float:
        """ runs the game with the stored internal parameters

        Returns:
            float: scoring of the game
        """
        print("Running game...")
        self.clean_logs() # clean out logs_location directory

        # Run the game executable from game_location with the parameters as CL arguments
        # TODO we can parallelize this by running multiple instances of the game with different parameters? not sure if this speeds up learning
        #       -> might give better results to run with same parameters & taking average of multiple (parallel) runs
        subprocess.run([self.game_location,
                        f"ngames={self.ingame_instance_count}",
                        f"timeout={self.timeout}",
                        "visible=false",
                        f"communication_count={self.parameters.communication_count}",
                        f"communication_delay={self.parameters.communication_delay}"
                        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) # silence output for now TODO maybe add verbosity parameter/parse into file?) 
        
        # gather results from logs_location and put in result array
        # loop over files in logs_location
        results = self.store_results()
        return self.score(results)

    def score_game(self, game_results:dict) -> float:
        """scores the results of the game; 
        do this here to more easily change scoring function (instead of baking it into the game)

        the score should be BETTER if LOWER (since we are minimizing the objective function)

        Args:
            game_results (dict): dictionary containing data gathered from game run

        Returns:
            float: scoring of the game for given set of parameters
        """
        score:float = 0.0
        # TODO weighted score of different metrics found in log
        score += game_results["team_damage"]["allies"]
        return score
    
    def score(self, results:dict) -> float:
        """scores the results of the game; 
        do this here to more easily change scoring function (instead of baking it into the game)

        the score should be BETTER if LOWER (since we are minimizing the objective function)

        Args:
            results (dict): dictionary containing data gathered from all game runs

        Returns:
            float: scoring of all the games for given set of parameters
        """
        print("Scoring game...")
        score:float = 0.0

        self.data.append({}) # add empty dict to data array
        # TODO weighted score?
        index = 0
        instance_scores =[]
        for instance_result in results.values():
            instance_score = self.score_game(instance_result)
            instance_scores.append(instance_score)
            self.data[-1][index] = instance_score # store score for this instance
            index += 1
        score = np.mean(np.array(instance_scores))  # return mean score of all instances
        print("score:", score)
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
        self.parameter_evolution.append({})
        for i in range(self.parameters.size()):
            paramval = x[i]
            if self.parameters.get_param_types()[i] == "int":
                paramval = round(paramval)
            print("setting", self.paramnames[i], "to", paramval)
            setattr(self.parameters, self.paramnames[i], paramval)
            self.parameter_evolution[-1][i] = paramval
        return self.run()
    
    # def optimize(self, delta:float = 0.01):
    #     """Optimizes the game by running it multiple times, scoring each run and adjusting the parameters.

    #     Args:
    #         delta (float, optional): Relative tolerance on parameters. Defaults to 0.01.
    #     """
    #     super().optimize(delta) # TODO can we do this, or does nlopt object need additional game-specific setup?

    def plot_data(self):
        """Plots the data stored in self.data
        """
        # scatter plot of team_damage_allies with labels
        plt.xlabel("Iteration")
        plt.ylabel("Average Team Damage per Instance (Allies)")
        avg_team_damage = [np.mean(list(instance.values())) for instance in self.data]
        total_team_damage = [sum(list(instance.values())) for instance in self.data]

        plt.scatter(range(len(avg_team_damage)), avg_team_damage)
        for i, txt in enumerate(avg_team_damage):
            label = "("
            for key in self.parameter_evolution[i]:
                label += str(round(self.parameter_evolution[i][key], 2)) + "," # TODO assuming all parameters are numbers
            label = label[:-1] + ")"
            plt.annotate(label, (i, avg_team_damage[i]))
        plt.show()
        # TODO think of other plots to show; 
        # - parameter evolution over time?
        # - parameter correlation with score? For each parameter? Or 3-D plot of 2 parameters and score?

    def store_data(self):
        """Stores the data in self.data to a file
        """
        os.makedirs('OUTPUT', exist_ok=True)  # Ensure the directory exists
        for iteration, data in enumerate(self.data):
            # add iteration number parameter values to data
            data["parameters"] = self.parameter_evolution[iteration]
            filename = f"OUTPUT/data_{iteration}.json"
            with open(filename, "w") as f:
                f.write(json.dumps(data))
