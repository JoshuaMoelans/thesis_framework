class GenericParameter:
    def __init__(self, type_, min_, max_, value):
        """Sets up the parameter with the given type, min, max, and value.

        Args:
            type_ (_type_): defines the type of the parameter
            min_ (_type_): defines the minimum value of the parameter
            max_ (_type_): defines the maximum value of the parameter
            value (_type_): defines the current value of the parameter
        """
        self.ptype = type_
        self.min = min_
        self.max = max_
        self.value = value

    def __repr__(self):
        return str(self.value)


class Parameters:
    def __init__(self):
        self.communication_count = GenericParameter(type_="int", min_=0, max_=10, value=3)
        self.communication_delay = GenericParameter(type_="float", min_=0.0, max_=5.0, value=0.2)

    def __getattr__(self, name):
        return getattr(self, name).value