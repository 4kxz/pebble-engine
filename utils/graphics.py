import collections

from sfml.graphics import *


class TiledSprite(Sprite):
    """
    Same as the SFML class, but with the center in actual the center.
    FIXME:
    Remember that the engine measures distance in tiles and sfml in pixels,
    and they are not equivalent. By default 1 tile = 32 pixels, project()
    scales the units accordingly. This should eventually be automatic.
    """

    def __init__(self, texture, offset, size):
        self.size = size
        self.offset = offset
        super().__init__(texture, self.rectangle())
        self.origin = size[0] / 2, size[1]/ 2

    def rectangle(self):
        x, y = self.offset
        w, h = self.size
        return x, y, w, h


class OrientedSprite(TiledSprite):
    """
    All frames should have the same size.
    """
    def __init__(self, texture, offset, size, atlas):
        self.atlas = atlas
        self.orientation = 0
        super().__init__(texture, offset, size)

    def rectangle(self):
        x, y, w, h = super().rectangle()
        a, b = self.atlas[self.orientation]
        return x + a, y + b, w, h


Frame = collections.namedtuple('Frame', ['framing', 'duration'])


class AnimatedSprite(TiledSprite):
    """
    All frames in the `script` should have the same size.
    """

    def __init__(self, texture, offset, size, script):
        self.script = script
        self.frame = 0
        super().__init__(texture, offset, size)

    def rectangle(self):
        x, y, w, h = super().rectangle()
        a, b = self.script[self.frame].framing
        return x + a, y + b, w, h
