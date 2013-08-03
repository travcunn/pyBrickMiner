from hashmap import HashMap


class Environment(object):
    def __init__(self):
        self.__objects = [] # World objects
        self.__hashmap = HashMap()

    def addObject(self, object):
        """
        Add an object to the environment
        """
        object.setEnvironment(self)
        self.__objects.append(object)

    def removeObject(self, object):
        """
        Remove an object from the environment
        """
        self.__objects.remove(object)

    def step(self, time):
        """
        Step forward with controllers attached to each object
        """
        for object in self.__objects:
            object.processControllers(time)

        # After processing the controllers, check for collisions
        self.checkCollisions()

    def inputStep(self, mouse_x, mouse_y):
        """
        Pass inputs to the objects
        """
        for object in self.__objects:
            object.mouseEvent(mouse_x, mouse_y)
            #TODO: Add a keyboard event here

    def addBlock(self, x, y):
        self.__hashmap.insert((x, y))

    def clearMap(self):
        self.__hashmap.clear()

    def checkCollisions(self):
        position = self.__objects[0].getPosition()
        print "Character position: ", position.x, position.y
        print "Hash output: ", self.__hashmap.get((position.x, position.y))
        if self.__hashmap.get((position.x, position.y)):
            print "collision!"
            self.__objects[0].gravity.stop()
            self.__objects[0].gravity.reset()

            self.__objects[0].jump.stop()
        else:
            self.__objects[0].gravity.start()


class Position(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class BaseObject(object):
    def __init__(self, x, y):
        self._position = Position(x, y)

    def getPosition(self):
        return self._position


class Object(BaseObject):
    def __init__(self, x, y):
        BaseObject.__init__(self, x, y)
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
        self.controllerEvent(self.x, self.y)
        self.reset()

    def controllerEvent(self, x, y):
        """
        Override this function to receive changes from the controllers
        """
        pass

    def mouseEvent(self, x, y):
        """
        Override this function to watch the mouse
        """
        pass

    def reset(self):
        self.x = 0
        self.y = 0

    def destroy(self):
        if self.__environment is not None:
            self.__environment.removeBody(self)


class Controller(object):
    #TODO: have the controllers set velocities instead of x and y coordinates
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

