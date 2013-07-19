class Environment(object):
    def __init__(self):
        self.__objects = [] # Array of objects in the world

    def addObject(self, object):
        object.setEnvironment(self)
        self.__objects.append(object)

    def removeObject(self, object):
        self.__objects.remove(object)

    def step(self, time):
        for object in self.__objects:
            object.processControllers(time)


class Object(object):
    def __init__(self, initialPosition):
        self.__environment = None # Define which environment the object is in
        self.__controllers = [] # Array of controllers of the object

        # Properties to be set by the controller (reset each step)
        self.x = 0
        self.y = 0

    def setEnvironment(self, environment):
        self.__environment = environment

    def addController(self, controller):
        controller.setParent(self)
        self.__controllers.append(controller)

    def removeController(self, controller):
        self.__controllers.remove(controller)

    def processControllers(self, time):
        for controller in self.__controllers:
            controller.step(time)
        self.controllerUpdate(self.x, self.y)
        self.reset()

    def controllerUpdate(self, x, y):
        raise NotImplementedError

    def reset(self):
        self.x = 0
        self.y = 0

    def destroy(self):
        if self.__environment is not None:
            self.__environment.removeBody(self)


class Controller(object):
    def __init__(self):
        self.parent = None # None until it gets set by the object
        self._running = False
        self.time = 0

    def setParent(self, parent):
        self.parent = parent

    def start(self):
        self._running = True

    def stop(self):
        self._running = False

    def reset(self):
        self.time = 0

    def isRunning(self):
        return self._running

    def step(self, time):
        if self.isRunning():
            self.time = self.time + time
            self.update(self.time)

    def update(self, time):
        raise NotImplementedError

