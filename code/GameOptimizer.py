from GenericOptimizer import GenericOptimizer
import subprocess

class GameOptimizer(GenericOptimizer):
    def __init__(self, game_location:str, input_location:str, logs_location:str):
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
        subprocess.run([self.game_location])
        
        # gather results from logs_location

        result = []
        return self.score(result)

    
    def score(self, results:dict) -> float:
        """scores the results of the game; 
        do this here to more easily change scoring function (instead of baking it into the game)

        Args:
            results (dict): dictionary of data gathered from a game run

        Returns:
            float: scoring of the game
        """
        print("Scoring game...")
        return 0.0

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