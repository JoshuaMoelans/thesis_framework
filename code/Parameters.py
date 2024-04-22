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


class GenericParameters:
    def __init__(self):
        raise NotImplementedError("GenericParameters is an abstract class and cannot be instantiated.")

    def __getattr__(self, name):
        return getattr(self, name).value
    
    def __setattr__(self, name, value):
        if name in self.__dict__:
            getattr(self, name).value = value
        else:
            self.__dict__[name] = value
    
    def size(self):
        return len(self.__dict__)
    
    def get_lower_bounds(self):
        return [getattr(self, key).min for key in self.__dict__]
    
    def get_upper_bounds(self):
        return [getattr(self, key).max for key in self.__dict__]
    
    def get_initial_values(self):
        return [getattr(self, key).value for key in self.__dict__]