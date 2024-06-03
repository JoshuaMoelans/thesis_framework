from GameOptimizer import GameOptimizer
from VisionConeParameters import VisionConeParameters
import nlopt
import subprocess

class VisionConeOptimizer(GameOptimizer):
    def set_parameters(self):
        self.parameters = VisionConeParameters()
    
    def run_subprocess(self):
        # Run the game executable from game_location with the parameters as CL arguments
        subprocess.run([self.game_location,
                        f"ngames={self.ingame_instance_count}",
                        f"timeout={self.timeout}",
                        "visible=false",
                        f"start_minimized=true",  # minimize the game window upon start
                        f"vision_distance={self.parameters.vision_distance}",
                        f"vision_angle={self.parameters.vision_angle}"
                        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) 
