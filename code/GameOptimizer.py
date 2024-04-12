from GenericOptimizer import GenericOptimizer

class GameOptimizer(GenericOptimizer):
    def __init__(self): # TODO temp init, to be replaced!
        """
        Initializes the GameOptimizer class
        TODO initialize with: 
        - game .exe file path
        """
        super().__init__()
        print("Game optimizer created!")

    def run(self, parameters:dict) -> float:
        """ runs the game with the given parameters

        Args:
            parameters (dict): list of parameters to run the game with

        Returns:
            float: scoring of the game
        """
        print("Running game...")
        result = []
        return self.score(result)

    
    def score(self, results:dict) -> float:
        """scores the results of the game

        Args:
            results (dict): dictionary of data gathered from a game run

        Returns:
            float: scoring of the game
        """
        print("Scoring game...")

    def optimize(self):
        print("Optimizing game...")
        # Do some optimization here
        print("Game optimized!")