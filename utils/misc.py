import math
import numbers
import random

E = 0.0001

class Vector:

    @classmethod
    def random(cls):
        return cls((random.random(), random.random()))

    @classmethod
    def dot(cls, u, v):
        return u.x * v.x + u.y * v.y

    @classmethod
    def distance(cls, u, v):
        return (u - v).norm()

    @classmethod
    def distance2(cls, u, v):
        d = u - v
        return d.x ** 2 + d.y ** 2

    @classmethod
    def manhattan(cls, u, v):
        return abs(u.x - v.x) + abs(u.y - v.y)

    def __init__(self, v=0.0):
        if isinstance(v, numbers.Number):
            self.x, self.y = float(v), float(v)
        else:
            self.x, self.y = v

    # TODO: Remove this.
    def project(self, scale=1):
        return int(self.x * scale), int(self.y * scale)

    def perpendicular(self):
        return Vector((-self.y, self.x))

    def unit(self):
        return self / self.norm() if self != Vector(0.0) else Vector(0.0)

    def norm(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __neg__(self):
        return Vector((-self.x, -self.y))

    def __eq__(self, other):
        return -E < self.x - other.x < E and -E < self.y - other.y < E

    def __add__(self, other):
        try:
            return Vector((self.x + other.x, self.y + other.y))
        except:
            return self + Vector(other)

    __radd__ = __add__

    def __iadd__(self, other):
        try:
            self.x += other.x
            self.y += other.y
        except:
            other = Vector(other)
            self.x += other.x
            self.y += other.y
        return self

    def __sub__(self, other):
        try:
            return Vector((self.x - other.x, self.y - other.y))
        except:
            return self - Vector(other)

    __rsub__ = __sub__

    def __isub__(self, other):
        try:
            self.x -= other.x
            self.y -= other.y
        except:
            other = Vector(other)
            self.x -= other.x
            self.y -= other.y
        return self

    def __mul__(self, other):
        try:
            return Vector((self.x * other.x, self.y * other.y))
        except:
            return self * Vector(other)

    __rmul__ = __mul__

    def __imul__(self, other):
        try:
            self.x *= other.x
            self.y *= other.y
        except:
            other = Vector(other)
            self.x *= other.x
            self.y *= other.y
        return self

    def __truediv__(self, other):
        try:
            return Vector((self.x / other.x, self.y / other.y))
        except:
            return self / Vector(other)

    __rtruediv__ = __truediv__

    def __itruediv__(self, other):
        try:
            self.x /= other.x
            self.y /= other.y
        except:
            other = Vector(other)
            self.x /= other.x
            self.y /= other.y
        return self

    def __floordiv__(self, other):
        try:
            return Vector((self.x // other.x, self.y // other.y))
        except:
            return self // Vector(other)

    __rfloordiv__ = __floordiv__

    def __ifloordiv__(self, other):
        try:
            self.x //= other.x
            self.y //= other.y
        except:
            other = Vector(other)
            self.x //= other.x
            self.y //= other.y
        return self

    def __iter__(self):
        yield self.x
        yield self.y
        raise StopIteration

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def __repr__(self):
        return "Vector(x={}, y={})".format(self.x, self.y)
