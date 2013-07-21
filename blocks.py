import math
import sys
import pygame
from pygame.locals import *

from  controllers import *
import resourceLoader
import characterLoader
import physics


class Block(pygame.sprite.Sprite):
    def __init__(self, blocktype, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.blocktype = blocktype
        self.image, self.rect = resourceLoader.loadBlockImage(blocktype)
        self.rect.topleft = x, y

    def move(self, x, y):
        self.rect.topleft = x, y

    def getPosition(self):
        return self.rect.topleft[0], self.rect.topleft[1]

    def update(self):
        pass

    def destroy(self):
        #destroys the object
        self.kill()


class Character(physics.Object, pygame.sprite.Sprite):
    def __init__(self, character, x, y):
        physics.Object.__init__(self, (x, y))
        pygame.sprite.Sprite.__init__(self)

        self.image, self.rect = characterLoader.loadCharacterImage(character)
        self.rect.topleft = x, y

        # Character attributes
        self._spriteSheet = []
        self._items = []
        self._health = 100

        # Character sprite forward/backward, 0 - left, 1 - right
        self._facing = 1
        self.__isFlipped = False

        gravity = Gravity()
        #gravity.start()

        self.jump = Jump()

        self.addController(gravity)
        self.addController(self.jump)

    def move(self, x, y):
        self.rect.topleft = x, y

    def jumpAction(self):
        self.jump.start()

    def updateDirection(self):
        if self._facing == 0 and not self.__isFlipped:
            self.image = pygame.transform.flip(self.image, True, False)
            self.__isFlipped = True
        elif self._facing == 1 and self.__isFlipped:
            self.image = pygame.transform.flip(self.image, True, False)
            self.__isFlipped = False

    def update(self):
        pass

    def controllerEvent(self, x, y):
        self.rect.topleft = self.rect.topleft[0] + x, self.rect.topleft[1] + y

    def mouseEvent(self, mouse_x, mouse_y):
        if mouse_x < self.rect.center[0]:
            self._facing = 0
        else:
            self._facing = 1

        self.updateDirection()

    def destroy(self):
        self.kill()


class Sky(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = resourceLoader.loadBlockImage("sky")
        self.rect.topleft = x, y

    def update(self):
        pass

    def destroy(self):
        self.kill() # dude. youre destroying the sky. this about this.


class World(physics.Environment):
    def __init__(self):
        physics.Environment.__init__(self)
        pygame.init()
        pygame.display.set_caption("pyBricks")
        pygame.mouse.set_visible(1)

        #self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((1000, 700))
        self.clock = pygame.time.Clock()

        self.visibleObjects = pygame.sprite.Group()
        self.visibleCharacters = pygame.sprite.Group()

        self.mouse_x = 0
        self.mouse_y = 0

        self.leftKeyPressed = False
        self.rightKeyPressed = False
        self.upKeyPressed = False
        self.downKeyPressed = False

        self.mouseLeftPressed = False
        self.spaceKeyPressed = False

        #color at the top of the gradient: (hex: 1a3258)
        #self.setBackground(26, 50, 88)
        #color of the bottom of the gradient: (hex: 94a7b6)
        self.setBackground(148, 167, 182)
        self.buildWorld()
        self.setupCharacter()
        self.setupGroups()
        self.mainLoop()

    def setBackground(self, r, g, b):
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((r, g, b))

        #change the screen background
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

    def buildWorld(self):
        #generate the blocks, then add them to the render group
        for x in range(50):
            xPos = x * 48
            for y in range(50):
                yPos = y * 48
                if y is 0:
                    block = Block("grass", xPos, yPos)
                else:
                    block = Block("dirt", xPos, yPos)
                self.visibleObjects.add(block)
        #generate the sky. fix this later.
        sky = Sky(0, -500)
        self.visibleObjects.add(sky)
        sky = Sky(500, -500)
        self.visibleObjects.add(sky)
        sky = Sky(1000, -500)
        self.visibleObjects.add(sky)
        sky = Sky(1500, -500)
        self.visibleObjects.add(sky)

    def setupCharacter(self):
        self.character = Character("character", 500, -400)
        self.addObject(self.character)
        self.visibleCharacters.add(self.character)

    def setupGroups(self):
        self.allsprites = pygame.sprite.RenderPlain(self.visibleObjects)
        self.allcharacters = pygame.sprite.RenderPlain(self.visibleCharacters)

    def moveCamera(self, x, y):
        """
        Moves the block grid an amount of pixels from the current position
        """
        for sprite in self.visibleObjects:
            sprite.rect.topleft = sprite.rect.topleft[0] + x, sprite.rect.topleft[1] + y
        for character in self.visibleCharacters:
            character.rect.topleft = character.rect.topleft[0] + x, character.rect.topleft[1] + y
        self.allsprites.update()

    def moveCharacter(self, x, y):
        """
        Moves the character an amount of pixels from the current position
        """
        self.character.rect.topleft = (self.character.rect.topleft[0] + x,
                                        self.character.rect.topleft[1] + y)
        self.allcharacters.update()

    def checkCameraPosition(self):
        """
        Checks the character against the camera position and moves it
        accordingly
        """
        threshold = 0.3 # Defines the boundaries as a percentage of screensize

        w, h = self.screen.get_size()
        character_x, character_y = self.character.rect.center
        x_threshold = (w * threshold, w - w * threshold) # left and right
        y_threshold = (h * threshold, h - h * threshold) # top and bottom

        #TODO: Move the camera with the player, instead of 10 pixels
        if x_threshold[0] > character_x:
            self.moveCamera(10, 0) # Move the camera to the left
        if x_threshold[1] < character_x:
            self.moveCamera(-10, 0) # Move the camera to the right
        if y_threshold[0] > character_y:
            self.moveCamera(0, 10) # Move the camera up
        if y_threshold[1] < character_y:
            self.moveCamera(0, -10) # Move the camera down

    def eventHandler(self):
        """
        Updates the key pressed variables based upon their status
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        self.resetInput()

        key = pygame.key.get_pressed()
        if key[K_LEFT]:
            self.leftKeyPressed = True
        if key[K_RIGHT]:
            self.rightKeyPressed = True
        if key[K_UP]:
            self.upKeyPressed = True
        if key[K_DOWN]:
            self.downKeyPressed = True
        if key[K_SPACE]:
            self.spaceKeyPressed = True

        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

        mouse = pygame.mouse.get_pressed()
        if mouse[0]:
            self.mouseLeftPressed = True

    def resetInput(self):
        self.leftKeyPressed = False
        self.rightKeyPressed = False
        self.upKeyPressed = False
        self.downKeyPressed = False

        self.mouseLeftPressed = False

        self.spaceKeyPressed = False

    def mainLoop(self):
        fps = 30 # Define the frames per second
        simulationTime = 1.0/fps # Defines the time for each environment step
        self.moveCamera(0, 500) # Initially, move the camera to this point

        while 1:
            pygame.display.set_caption("[FPS]: %.2f blocks: %i" % (self.clock.get_fps(), len(self.visibleObjects)))

            self.eventHandler()
            self.checkCameraPosition()

            if self.leftKeyPressed:
                self.moveCharacter(-10, 0)
            if self.rightKeyPressed:
                self.moveCharacter(10, 0)
            if self.upKeyPressed:
                self.moveCharacter(0, -10)
            if self.downKeyPressed:
                self.moveCharacter(0, 10)

            if self.mouseLeftPressed:
                for item in self.visibleObjects:
                    x, y = item.rect.topleft
                    xMouse, yMouse = pygame.mouse.get_pos()
                    if xMouse >= x and xMouse < x + 50:
                        if yMouse >= y and yMouse < y + 50:
                            item.destroy()

            if self.spaceKeyPressed:
                self.character.jumpAction()

            self.screen.blit(self.background, (0, 0))
            self.allsprites.draw(self.screen)
            self.allcharacters.draw(self.screen)
            pygame.display.flip()

            # simulate a step in the virtual environment
            self.step(simulationTime)

            # pass mouse coordinates to the environment
            self.inputStep(self.mouse_x, self.mouse_y)

            # have pyGame keep the framerate
            self.clock.tick(fps)

World()
