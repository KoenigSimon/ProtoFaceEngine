class Vector:
    x: float
    y: float

    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y

    def __mul__(self, other):
        result = Vector()
        result.x = self.x * other.x
        result.y = self.y * other.y
        return result

    def __sub__(self, other):
        result = Vector()
        result.x = self.x - other.x
        result.y = self.y - other.y
        return result

    def __add__(self, other):
        result = Vector()
        result.x = self.x + other.x
        result.y = self.y + other.y
        return result

    def __divmod__(self, other):
        result = Vector()
        result.x = self.x / other.x
        result.y = self.y / other.y
        return result

    def toArray(self):
        return [self.x, self.y]