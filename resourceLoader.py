import os
import pygame

# this provides resource caching

__blockImages = {}

def loadBlockImage(name):
    name = "%s.jpg" % name
    fullname = os.path.join('blocks', name)
    if name not in __blockImages.keys():
        try:
            image = pygame.image.load(fullname)
        except pygame.error:
            print "Error loading %s" % name
        __blockImages[name] = image
    else:
        image = __blockImages[name]
    return image, image.get_rect()