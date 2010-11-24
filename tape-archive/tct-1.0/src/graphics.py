# -*- coding: utf-8 -*-

#    Game's Graphics Utilities.
#
#    This file is part of The Crime Tracer.
#
#    Copyright (C) 2009 Athanasios Kasampalis <faif at gnu period org> 
#    Copyright (C) 2009 Efstathios Xatzikiriakidis <lafs at ixthis period gr> 
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


## @package graphics
#  Game's Graphics Utilities.
#
# This module contains the game's graphics
# utilities, loading graphics, fonts, etc.


try:
    import pygame

    import constants

    from pygame.locals import RLEACCEL

    from os_utils import file_path
except ImportError, err:
    print ''.join(["Couldn't load module. ", err])
    exit(constants.MOD_IMP_ERR)


## objects imported when `from <module> import *' is used
__all__ = ['load_image', 'load_font', 'handle_mouse_cursor']


## the default size of a font
FONT_SIZE = 17

## the default colorkey of an image
IMAGE_COLORKEY = None


## load an image (with a colorkey - optional)
#
# @param filename the filename of the image
# @param colorkey the RGB value of the colorkey, or -1
#                 to get the topleft of the given image 
# @throw SystemExit when the load fails
# @return the loaded image and its coordinates
def load_image(filename, colorkey=IMAGE_COLORKEY):
    # get the path of the filename
    fullname = file_path(filename, constants.GRAPHICS_DIR)

    # try to load the image
    try:
        image = pygame.image.load(fullname)
    except:
        print ''.join(["Couldn't load image: ", fullname])
        raise SystemExit

    # check the current alpha value of the surface
    if image.get_alpha() is None:
        image = image.convert()
    else:
        image = image.convert_alpha()

    # check for image's colorkey
    if colorkey:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))

        image.set_colorkey(colorkey, RLEACCEL)

    # return the image and its rectangle
    return image, image.get_rect()


## load a font
#
# @param filename the filename of the font
# @param size the size of the font
# @throw SystemExit when the load fails
# @return the loaded font
def load_font(filename, size=FONT_SIZE):
    # get the path of the filename
    fullname = file_path(filename, constants.FONTS_DIR)

    # try to create the font
    try:
        font = pygame.font.Font(fullname, size)
    except:
        print ''.join(["Couldn't load font: ", fullname])
        raise SystemExit

    # return the font
    return font


## update the custom cursor
#
# @param mc the mouse cursor
# @param su the surface used for blitting
def handle_mouse_cursor(mc, su):
    x, y = pygame.mouse.get_pos()
    x -= mc.get_width() / 2.0
    y -= mc.get_height() / 2.0
    su.blit(mc, (x, y))
