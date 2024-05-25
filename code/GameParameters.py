from Parameters import GenericParameters, GenericParameter
class GameParameters(GenericParameters):
    def __init__(self):
        self.communication_count = GenericParameter(type_="int", min_=0, max_=4, value=0, step_size=1)
        self.communication_delay = GenericParameter(type_="float", min_=0.0, max_=1.0, value=0.2, step_size=0.1)