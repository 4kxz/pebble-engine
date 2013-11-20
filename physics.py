from .base import Component, System
from .utils.misc import Vector
from .utils.noise import scaled_octave_noise_2d


DRAG_COEF = -Vector(10)


class Physics(System):

    update_loop = 'fixed'

    def __init__(self, width, height, **kwargs):
        super().__init__(**kwargs)
        self.level = Level(width, height)

    def update(self, delta):
        vdelta = Vector(delta)
        for comp in self.components:
            comp.update(vdelta)
        # FIXME: This is obviously inneficient.
        for i, a in enumerate(self.components):
            for j, b in enumerate(self.components[i+1:]):
                difference = a.position - b.position
                distance = difference.norm()
                maximum = (a.radius + b.radius) / 2
                # TODO: Should probably consider fixing the overlap...
                if distance <= maximum:
                    normal = difference.unit()
                    collision = normal.perpendicular()
                    velocity = a.velocity - b.velocity
                    if Vector.dot(normal, velocity.unit()) < 0:
                        av_n = Vector.dot(a.velocity, normal)
                        bv_n = Vector.dot(b.velocity, normal)
                        av_c = Vector.dot(a.velocity, collision)
                        bv_c = Vector.dot(b.velocity, collision)
                        av_p = av_n * (a.mass - b.mass) + 2 * b.mass * bv_n
                        bv_p = bv_n * (b.mass - a.mass) + 2 * a.mass * av_n
                        av_p /= a.mass + b.mass
                        bv_p /= b.mass + a.mass
                        a.velocity = normal * av_p + collision * av_c
                        b.velocity = normal * bv_p + collision * bv_c


class Body(Component):

    system_cls = Physics

    def __init__(self, position, radius, mass=1.0, **kwargs):
        super().__init__(**kwargs)
        if self.system.level[position] is None:
            raise ValueError("Invalid position {}.".format(position))
        if radius <= 0:
            raise ValueError("Invalid radius {}.".format(radius))
        if mass <= 0:
            raise ValueError("Invalid mass {}.".format(mass))
        self.radius = radius
        self.mass = mass
        self.position = Vector(position)
        self.velocity = Vector(0.0)
        self.force = Vector(0.0)

    def update(self, vdelta):
        pass


class FixedBody(Body):

    pass


class DynamicBody(Body):

    def update(self, vdelta):
        forces = DRAG_COEF * self.velocity + self.force
        acceleration = forces / self.mass
        self.velocity += acceleration * vdelta
        if not self.velocity == Vector(0.0):
            next_position = self.position + self.velocity * vdelta
            h_tile = self.system.level[next_position.x, self.position.y]
            v_tile = self.system.level[self.position.x, next_position.y]
            if h_tile is not None and not h_tile.solid:
                self.position.x = next_position.x
            if v_tile is not None and not v_tile.solid:
                self.position.y = next_position.y


class KineticBody(Body):

    pass


class Level:

    def __init__(self, width, height, **kwargs):
        super().__init__(**kwargs)
        self.width = int(width)
        self.height = int(height)
        self._grid = [None] * height
        for i in range(height):
            self._grid[i] = [None] * width
            for j in range(width):
                height = scaled_octave_noise_2d(3, .3, .05, 0, 1, j, i)
                self._grid[i][j] = Tile(j, i, height)

    def __iter__(self):
        for row in self._grid:
            for tile in row:
                yield tile
        raise StopIteration

    def __getitem__(self, position):
        x, y = position
        x, y = round(x), round(y)
        if not 0 <= x < self.width or not 0 <= y < self.height:
            return None
        else:
            return self._grid[y][x]

    @property
    def size(self):
        return self.width, self.height


class Tile:

    def __init__(self, x, y, height):
        self.x = x
        self.y = y
        self.height = height

    @property
    def position(self):
        return Vector((self.x, self.y))

    @property
    def solid(self):
        return not 0.25 < self.height < 0.75
