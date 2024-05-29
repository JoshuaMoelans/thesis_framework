import GameOptimizer
import VisionConeParameters
import nlopt
import subprocess

class VisionConeOptimizer(GameOptimizer):
    def set_parameters(self):
        self.parameters = VisionConeParameters()
    
    def run_subprocess(self):
        # Run the game executable from game_location with the parameters as CL arguments
        # TODO we can parallelize this by running multiple instances of the game with different parameters? not sure if this speeds up learning
        #       -> might give better results to run with same parameters & taking average of multiple (parallel) runs
        subprocess.run([self.game_location,
                        f"ngames={self.ingame_instance_count}",
                        f"timeout={self.timeout}",
                        "visible=false",
                        f"start_minimized=true",  # minimize the game window upon start
                        f"vision_distance={self.parameters.vision_distance}",
                        f"vision_angle={self.parameters.vision_angle}"
                        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) # silence output for now TODO maybe add verbosity parameter/parse into file?) 
