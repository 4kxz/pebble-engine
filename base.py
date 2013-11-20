import collections

from .settings import WIDTH, HEIGHT, TITLE, DELTA
from .utils.graphics import RenderWindow
from .utils.system import Clock
from .utils.window import VideoMode


class Engine:

    def __init__(self, loader):
        self.loader = loader
        self.systems = {}
        self.fixed = []
        self.variable = []
        self.is_running = False
        self.window = RenderWindow(VideoMode(WIDTH, HEIGHT), TITLE)
        self.window.vertical_synchronization = True
        self.events = collections.deque()
        self.fps_delta = 1/60

    def start(self):
        acum = DELTA
        clock = Clock()
        self.is_running = True
        while self.is_running:
            acum += min(clock.elapsed_time.seconds, 1)
            clock.restart()
            delta = 0
            while acum >= DELTA:
                acum -= DELTA
                delta += DELTA
                for system in self.fixed:
                    system.update(DELTA)
            for system in self.variable:
                system.update(delta)
            self.fps_delta = self.fps_delta * 0.99 + delta * 0.01

    def stop(self):
        self.framerate()
        self.is_running = False
        self.window.close()

    def framerate(self):
        print(1 / self.fps_delta if self.fps_delta else None)

    def attach(self, system_cls, *args, **kwargs):
        """
        Adds a system to the engine.
        """
        system = system_cls(engine=self, *args, **kwargs)
        if system.update_loop == 'fixed':
            self.fixed.append(system)
        elif system.update_loop == 'variable':
            self.variable.append(system)
        else:
            raise ValueError("Loop must be fixed or variable.")
        self.systems[system_cls] = system
        return system

    def new(self, entity_cls=None, *args, **kwargs):
        """
        Instantiates an entity.
        """
        if entity_cls is None:
            entity = Entity(engine=self)
        else:
            entity = entity_cls(engine=self, *args, **kwargs)
        return entity


class System:

    loop = None

    def __init__(self, engine):
        self.engine = engine
        self.components = []

    def add(self, component):
        self.components.append(component)

    def update(self, delta):
        raise NotImplementedError


class Component:

    system_cls = None

    def __init__(self, entity):
        self.entity = entity
        self.engine = entity.engine
        self.system = entity.engine.systems[self.system_cls]
        self.system.add(self)


class Entity:

    def __init__(self, engine):
        self.engine = engine
        self.components = {}

    def attach(self, component_cls, *args, **kwargs):
        component = component_cls(entity=self, *args, **kwargs)
        self.components[component_cls] = component
        return component

    def __getitem__(self, component_cls):
        return self.components.get(component_cls)

    def __contains__(self, component_cls):
        return component_cls in self.components
