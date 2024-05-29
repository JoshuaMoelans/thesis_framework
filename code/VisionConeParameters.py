from Parameters import GenericParameters, GenericParameter
class VisionConeParameters(GenericParameters):
    def __init__(self):
        self.vision_distance = GenericParameter(type_="float", min_=100, max_=600, value=300, step_size=50)
        self.vision_angle = GenericParameter(type_="float", min_=10, max_=220, value=60, step_size=15)