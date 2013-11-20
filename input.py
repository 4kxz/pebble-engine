from .base import Component, System
from .utils.misc import Vector
from .utils.window import CloseEvent, Keyboard, KeyEvent


class Action:
    attack = 0
    defend = 1


class Input(System):

    update_loop = 'variable'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.input = self.engine.window

    def update(self, delta):
        actions = set()
        for event in self.input.events:
            if event == CloseEvent:
                self.stop()
            elif event == KeyEvent and event.pressed:
                if event.code == Keyboard.ESCAPE:
                    self.engine.stop()
                if event.code == Keyboard.L_CONTROL:
                    self.engine.framerate()
                if event.code == Keyboard.SPACE:
                    actions.add(Action.attack)
                if event.code == Keyboard.L_SHIFT:
                    actions.add(Action.defend)
        # FIXME: Movement code is here for now.
        # Map input to axis:
        axis = Vector(0.0)
        if Keyboard.is_key_pressed(Keyboard.W):
            axis -= (0, 1)
        if Keyboard.is_key_pressed(Keyboard.D):
            axis += (1, 0)
        if Keyboard.is_key_pressed(Keyboard.S):
            axis += (0, 1)
        if Keyboard.is_key_pressed(Keyboard.A):
            axis -= (1, 0)
        # Update instances:
        axis = axis.unit()
        force = axis * Vector(40.0)
        for comp in self.components:
            comp.body.force = force
            comp.direction = axis if axis != Vector(0.0) else comp.direction
            comp.update(actions)


class BodyController(Component):

    system_cls = Input

    def __init__(self, body, **kwargs):
        super().__init__(**kwargs)
        self.body = body
        self.direction = Vector(0.0)

    def update(self, actions):
        for action in actions:
            if action is Action.defend:
                self.body.velocity += self.direction * 20
