from Parameters import GenericParameters
from abc import ABC, abstractmethod
import time
import nlopt

class GenericOptimizer(ABC):
    @abstractmethod
    def __init__(self) -> None:
        self.parameters = GenericParameters()
        return NotImplementedError
    
    @abstractmethod
    def obj_func(self):
        """objective function for optimization

        Returns:
            float: scoring of the game
        """
        return NotImplementedError

    NLopt_return_codes = {
        1: "success",
        2: "stopval reached",
        3: "ftol reached",
        4: "xtol reached",
        5: "maxeval reached",
        6: "maxtime reached",
        -1: "failure",
        -2: "invalid args",
        -3: "out of memory",
        -4: "roundoff limited",
        -5: "forced stop",
    }

    def optimize(self, delta:float) -> None:
        """optimizes the game by running it multiple times, scoring each run and adjusting the parameters.
        goes until change in scoring is less than delta

        Args:
            delta (float, optional): minimal change required to keep adjusting parameters. Defaults to 0.1.
        """
        # start timer
        start_time = time.time()
        # NLopt setup
        opt = nlopt.opt(nlopt.LN_COBYLA, self.parameters.size()) # TODO parameterize Opt. algorithm
        # TODO set nonlinear constraints for parameter types (https://nlopt.readthedocs.io/en/latest/NLopt_Python_Reference/#nonlinear-constraints)
        opt.set_lower_bounds(self.parameters.get_lower_bounds())
        opt.set_upper_bounds(self.parameters.get_upper_bounds())
        opt.set_max_objective(self.obj_func)
        opt.set_xtol_rel(delta) # relative tolerance on parameters

        # NLopt optimization
        x = opt.optimize(self.parameters.get_initial_values())
        minf = opt.last_optimum_value()
        print("---------------------------------------------------------------------")
        print("Optimization complete!")
        elapsed_time = time.time() - start_time
        print(f"Elapsed time: {elapsed_time:.3f} seconds")
        print(f"Ran {opt.get_numevals()} evaluations")
        print("optimal parameter values:")
        for i in range(self.parameters.size()):
            print(f"\t{self.paramnames[i]} = {x[i]}")
        print(f"minimum value = {minf}")
        print(f"result code = {opt.last_optimize_result()}")
        print(f"result code = {self.NLopt_return_codes[opt.last_optimize_result()]}")