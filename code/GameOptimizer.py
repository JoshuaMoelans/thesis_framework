from GenericOptimizer import GenericOptimizer
import subprocess
import os

class GameOptimizer(GenericOptimizer):
    def __init__(self, game_location:str, logs_location:str, ingame_instance_count:int = 4):
        """
        Initializes the GameOptimizer class.

        Parameters:
        - game_location (str): The location of the game executable.
        - input_location (str): The location of input files; used to set parameters for game run.
        - logs_location (str): The location to store logs; used to retrieve data from game run.
        """
        super().__init__()
        self.game_location = game_location
        self.logs_location = logs_location
        self.ingame_instance_count = ingame_instance_count # can be used to run multiple instances of the game in parallel;
        self.parameters = { # TODO define more parameters
            "communication_count" : { # the number of 'close' units an attack is communicated to
                "type" : "int",
                "min" : 0,
                "max" : 10,
                "value" : 1
            },
            "communication_delay" : { # the delay in seconds before an attack is communicated to 'close' units
                "type" : "float",
                "min" : 0.0,
                "max" : 5.0,
                "value" : 1.5
            },
        }

    def clean_logs(self):
        """cleans out the logs_location directory
        """
        for file in os.listdir(self.logs_location):
            file_path = os.path.join(self.logs_location, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)

    def run(self, parameters:dict) -> float:
        """ runs the game with the given parameters

        Args:
            parameters (dict): list of parameters to run the game with

        Returns:
            float: scoring of the game
        """
        print("Running game...")
        self.clean_logs() # clean out logs_location directory

        # Run the game executable from game_location with the parameters as CL arguments
        subprocess.run([self.game_location, f"-ngames={self.ingame_instance_count}", "-visible=false"]) # TODO we can parallelize this by running multiple instances of the game with different parameters?
        # TODO think about when to stop the game? can use _on_time_out_timeout() in Godot to get_tree().quit()
        
        # + write final results for each instance to logs_location  (in Godot)
        
        # gather results from logs_location and put in result array
        # loop over files in logs_location
        results = []
        for file in os.listdir(self.logs_location):
            file_path = os.path.join(self.logs_location, file)
            if os.path.isfile(file_path):
                # TODO check file name to find final results for each instance (e.g. "instance_1_results.txt")
                with open(file_path, "r") as f:
                    # TODO read the file and put in result array
                    pass
        return self.score(results)


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
        score:float = 0.0
        while True:
            # Do some optimization here
            new_score = self.run({}) # TODO pass (updated) parameters
            if abs(new_score - score) < delta: # TODO make sure this is a good stopping criterion
                break
            score = new_score
        print("Game optimized!")