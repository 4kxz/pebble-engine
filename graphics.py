from .base import Component, System
from .settings import DEBUG, SCALE
from .utils.graphics import Color, PrimitiveType, VertexArray
from .utils.misc import Vector


class Graphics(System):

    update_loop = 'variable'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.render = self.engine.window
        self.color = Color(222, 222, 222)
        self.font = self.engine.loader.font("fontin-regular.ttf")

    def update(self, delta):
        self.render.clear(self.color)
        for comp in self.components:
            comp.update(delta)
        for comp in self.components:
            comp.draw()
        self.render.display()


class GraphicsComponent(Component):

    system_cls = Graphics

    def update(self, delta):
        pass

    def draw(self):
        pass


class Renderer(GraphicsComponent):

    system_cls = Graphics

    def __init__(self, sprite, position, **kwargs):
        super().__init__(**kwargs)
        self.sprite = sprite
        self.sprite.position = position.project(SCALE)

    def draw(self):
        self.system.render.draw(self.sprite)


class MovingRenderer(Renderer):

    def __init__(self, sprite, target, **kwargs):
        super().__init__(sprite, target.position, **kwargs)
        self.target = target

    def update(self, delta):
        self.sprite.position = self.target.position.project(SCALE)

    if DEBUG:
        def draw(self):  # FIXME: Debugging function
            super().draw()
            lines = VertexArray(PrimitiveType.LINES_STRIP, 2)
            lines[0].position = self.target.position.project(SCALE)
            lines[0].color = Color.BLUE
            lines[1].position = (self.target.position + self.target.velocity).project(SCALE)
            lines[1].color = Color.RED
            self.system.render.draw(lines)


class Orientator(GraphicsComponent):

    def __init__(self, sprite, target, **kwargs):
        super().__init__(**kwargs)
        self.sprite = sprite
        self.target = target

    def update(self, delta):
        if self.target.direction == Vector((0, +1)):
            self.sprite.orientation = 0
        if self.target.direction == Vector((-1, 0)):
            self.sprite.orientation = 1
        if self.target.direction == Vector((+1, 0)):
            self.sprite.orientation = 2
        if self.target.direction == Vector((0, -1)):
            self.sprite.orientation = 3
        self.sprite.texture_rectangle = self.sprite.rectangle()


class Animator(GraphicsComponent):

    def __init__(self, sprite, **kwargs):
        super().__init__(**kwargs)
        self.sprite = sprite
        self.cursor = 0
        self.elapsed = 0

    def update(self, delta):
        self.elapsed += delta
        # Advance the cursor when the elapsed time exceeds the frame duration:
        frame = self.sprite.script[self.cursor]
        dirty = False
        while self.elapsed > frame.duration:
            self.cursor += 1
            self.cursor %= len(self.sprite.script)
            self.elapsed -= frame.duration
            frame = self.sprite.script[self.cursor]
            dirty = True
        # Adjust framing if the cursor has advanced:
        if dirty:
            self.sprite.frame = self.cursor
            self.sprite.texture_rectangle = self.sprite.rectangle()


class Tracker(GraphicsComponent):

    def __init__(self, target, margin=0.75, **kwargs):
        super().__init__(**kwargs)
        self.sprite = None
        self.target = target
        self.margin = margin
        self.position = Vector(target.position)

    def update(self, delta):
        # self.system.render.view.center = self.target.position.project(SCALE)
        d = (self.target.position - self.position)
        self.position += d * delta if d.norm() >= self.margin else 0
        self.system.render.view.center = self.position.project(SCALE)
