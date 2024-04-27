from Parameters import GenericParameters, GenericParameter
class GameParameters(GenericParameters):
    def __init__(self):
        self.communication_count = GenericParameter(type_="int", min_=0, max_=5, value=3)
        self.communication_delay = GenericParameter(type_="float", min_=0.0, max_=5.0, value=1.5)