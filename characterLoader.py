import os
import pygame

# this provides resource caching

__characterImages = {}

def loadCharacterImage(name):
    name = "%s.png" % name
    fullname = os.path.join('characters', name)
    if name not in __characterImages.keys():
        try:
            image = pygame.image.load(fullname)
        except pygame.error:
            print "Error loading %s" % name
        __characterImages[name] = image
    else:
        image = __characterImages[name]
    return image, image.get_rect()
