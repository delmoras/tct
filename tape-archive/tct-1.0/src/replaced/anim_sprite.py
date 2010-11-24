# -*- coding: utf-8 -*-

#    Game's Linear Sprite Animation Utils.
#
#    This file is part of The Crime Tracer.
#
#    Copyright (C) 2009 Efstathios Xatzikiriakidis <lafs at ixthis period gr> 
#    Copyright (C) 2009 Athanasios Kasampalis <faif at gnu period org> 
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


## @package anim_sprite
#  Game's Linear Sprite Animation Utils.
#
# This module contains some classes which
# provide linear sprite animation motion.


try:
    import pygame.sprite

    import constants

    from random import seed, randint
    from datetime import datetime

    from graphics import load_image
except ImportError, err:
    print ''.join(["Couldn't load module. ", err])
    exit(constants.MOD_IMP_ERR)


## objects imported when `from <module> import *' is used
__all__ = ['VerticalAnimatedSprite', 'HorizontalAnimatedSprite']


## the default speed of a sprite movement
SPRITE_SPEED = 100


## class of an animation sprite
#
class AnimatedSprite(pygame.sprite.Sprite):

    ## create a new animated sprite
    #
    # @param self the object pointer
    # @param filename the sprite's image filename
    # @param speed the speed of the sprite's animation
    def __init__(self, filename, speed=SPRITE_SPEED):
        # call the base constructor
        pygame.sprite.Sprite.__init__(self)

        ## set up the speed of the sprite
        self.speed = speed

        ## set up the graphic of the sprite
        self.image = load_image(filename)[0]

        ## set up the x coordinate of the sprite
        self.x = 0

        ## set up the y coordinate of the sprite
        self.y = 0

    ## get the coordinates of the sprite
    #
    # @param self the object pointer
    # @return the x and y coordinates of the sprite 
    def get_coords(self):
        return self.x, self.y

    ## set the coordinates of the sprite
    #
    # @param self the object pointer
    # @param position the position of the sprite 
    def set_coords(self, position):
        x, y = position
        self.x = x
        self.y = y


## class of a vertically animation sprite
#
class VerticalAnimatedSprite(AnimatedSprite):

    ## create a new vertically animated sprite
    #
    # @param self the object pointer
    # @param filename the sprite's image filename
    # @param speed the speed of the sprite's animation
    def __init__(self, filename, speed=SPRITE_SPEED):
        # call the base animated sprite constructor
        AnimatedSprite.__init__(self, filename, speed) 

        # set up a random seed based on microseconds
        seed(datetime.now().microsecond)

        ## set up the x coordinate of the sprite
        self.x = randint(0, constants.SCREEN_WIDTH -
                            self.image.get_width())

        ## set up the y coordinate of the sprite
        self.y = -self.image.get_height()

    ## ensure that the position of the sprite
    ## on the window screen is the correct one
    #
    # @param self the object pointer
    def correct_position(self):
        if self.y > constants.SCREEN_HEIGHT:
            self.y = -self.image.get_height()
            self.x = randint(0, constants.SCREEN_WIDTH -
                                self.image.get_width())

    ## change the value of the y coordinate
    #
    # @param self the object pointer
    # @param seconds the time factor to use for moving the sprite
    def move_y(self, seconds):
        self.y += (seconds * self.speed) # distance moved


## class of a horizontally animation sprite
#
class HorizontalAnimatedSprite(AnimatedSprite):

    ## create a new horizontally animated sprite
    #
    # @param self the object pointer
    # @param filename the sprite's image filename
    # @param speed the speed of the sprite's animation
    def __init__(self, filename, speed=SPRITE_SPEED):
        # call the base animated sprite constructor
        AnimatedSprite.__init__(self, filename, speed) 

        # set up a random seed based on microseconds
        seed(datetime.now().microsecond)

        ## set up the y coordinate of the sprite
        self.y = randint(0, constants.SCREEN_HEIGHT -
                            self.image.get_height())

        ## set up the x coordinate of the sprite
        self.x = -self.image.get_width()

    ## ensure that the position of the sprite
    ## on the window screen is the correct one
    #
    # @param self the object pointer
    def correct_position(self):
        if self.x > constants.SCREEN_WIDTH:
            self.x = -self.image.get_width()
            self.y = randint(0, constants.SCREEN_HEIGHT -
                                self.image.get_height())

    ## change the value of the x coordinate
    #
    # @param self the object pointer
    # @param seconds the time factor to use for moving the sprite
    def move_x(self, seconds):
        self.x += (seconds * self.speed) # distance moved
