# -*- coding: utf-8 -*-

#    Menu System Utils.
#
#    This file is part of The Crime Tracer.
#
#    Copyright (C) 2009 Luca Fabbri <lucafbb at gmail com>
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


## @package kezmenu
#  Menu System Utils.
#
# This module contains a simple but complete
# class to create, display and handle menus.


try:
    import pygame

    import constants

    from sound_mixer import play_sound, load_sound
    from graphics import load_image
except ImportError, err:
    print ''.join(["Couldn't load module. ", err])
    exit(constants.MOD_IMP_ERR)


## objects imported when `from <module> import *' is used
__all__ = ['KezMenu']


## the distance between the menu's label and image
FOCUS_IMAGE_SPACE = 8


## class to create and handle simple menus
#
class KezMenu(object):

    ## initialize the menu
    #
    # @param self the object pointer
    # @param game_opts the game's command line options
    # @param menu_opts the game's menu options
    def __init__(self, game_opts, *menu_opts):
 
        ## create a programmer friendly mapping stucture of the menu options
        self.options = [{'label': x[0], 'callable': x[1]} for x in menu_opts]

        ## store the game options
        self.game_opts = game_opts

        # set the default menu dimensions (these dimensions
        # are calculated depending on the font and its size)

        ## menu's width
        self.width = 0

        ## menu's height
        self.height = 0

        # set up the default coordinates of the menu

        ## menu's x coordinate
        self.x = 0

        ## menu's y coordinate
        self.y = 0

        ## the topleft corner of the screen
        self.screen_topleft_offset = (0, 0)

        ## set the default focused option
        self.option = 0

        ## set the default previous focused option
        self.option_previous = self.option

        ## set the default normal color of the menu font
        self.normal_color = pygame.Color('black')

        ## set the default focused color of the menu font
        self.focus_color = pygame.Color('red')

        ## default is to enable support of menu image on focused options
        self.image_enabled = True

        ## default is to enable support mouse on menu
        self.mouse_enabled = True

        ## set mouse focusing at unknown at default
        self.mouse_focus = None
        self._font = None

        ## set a default font and its size (also fix size)
        self.font = pygame.font.Font(None, 32)
        self._fix_size()

        ## set the default sound to play when an option is focused
        self.focus_sound = load_sound(
             constants.FILES['sounds']['menu']['share']['focus'][0])

        ## set the default sound to play when an option is entered
        self.select_sound = load_sound(
             constants.FILES['sounds']['menu']['share']['sel'][0])

        ## set the default graphic to display before the option label
        self.focus_graphic = load_image(
             constants.FILES['graphics']['menu']['share']['focus'][0])[0]

    ## fix the menu size (called
    ## when the font is changed)
    #
    # @param self the object pointer
    def _fix_size(self):
        self.height = 0
        # for each option in the menu (set menu's width, height)
        for o in self.options:
            text = o['label']
            font = o['font']
            ren = font.render(text, True, self.normal_color)

            # find the maximum label width and set the menu's width
            if ren.get_width() > self.width:
                self.width = ren.get_width()

            # add all labels' heights and set the menu's height
            self.height += font.get_height()

    ## blit the menu to a surface
    #
    # @param self the object pointer
    # @param surface the surface used
    def draw(self, surface):
        offset = 0
        i = 0
        ol, ot = self.screen_topleft_offset
        first = self.options and self.options[0]
        last = self.options and self.options[-1]
        for o in self.options:
            indent = o.get('padding_col', 0)

            # padding above the line
            if o != first and o.get('padding_line', 0):
                offset += o['padding_line']
            
            font = o.get('font', self._font)

            # if there is a highlight color use it
            if i == self.option and self.focus_color:
                clr = self.focus_color
            else:
                clr = self.normal_color

            # get the label of the option
            text = o['label']

            # get the size of the first letter
            letter_width, letter_height = font.size(text[0])

            # render the options's label
            ren = font.render(text, True, clr)

            # lock the surface
            surface.lock()

            # draw line in correct coordinates in
            # order to underline the first letter
            pygame.draw.line(ren, clr, (0, letter_height-1),
                                       (letter_width, letter_height-1))

            # unlock the surface
            surface.unlock()

            if ren.get_width() > self.width:
                self.width = ren.get_width()

            o['label_rect'] = pygame.Rect(
                (ol + self.x + indent, ot + self.y + offset),
                (ren.get_width(), ren.get_height()))

            surface.blit(ren, (self.x + indent, self.y + offset))

            # divide the difference between the font and graphic height
            calc_space = abs((font.get_height() -
                              self.focus_graphic.get_height()) / 2.0)

            # print the menu image on focused option (only if it's enabled)
            if i == self.option and self.image_enabled:
                surface.blit(self.focus_graphic,
                             (abs(self.x - FOCUS_IMAGE_SPACE -
                                  self.focus_graphic.get_width()),
                              self.y + calc_space + offset))

            offset += font.get_height()

            # padding below the line
            if o != last and o.get('padding_line', 0):
                offset += o['padding_line']

            i += 1

    ## update the menu and get input for the menu
    #
    # @param self the object pointer
    # @param events the events called
    def update(self, events):
        for e in events:

            # keyboard controls
            if e.type == pygame.KEYDOWN:

                # change menu option
                if e.key == pygame.K_DOWN:
                    self.option += 1
                elif e.key == pygame.K_UP:
                    self.option -= 1

                # play a sound when a menu option:

                # is focused
                if e.key in (pygame.K_UP, pygame.K_DOWN):
                    if self.game_opts.sound:
                        play_sound(self.focus_sound, 0.2)
                # is entered
                elif e.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if self.game_opts.sound:
                        play_sound(self.select_sound, 0.2)

                    self.options[self.option]['callable']()

            # mouse controls (only if it's enabled)
            if self.mouse_enabled:
                # if there is some mouse motion
                if e.type == pygame.MOUSEMOTION:
                    # keep in mind the previous option
                    self.option_previous = self.option

                    # check the mouse's positions to
                    # know if move focus on a option
                    self._check_mouse_pos_for_focus()

                    # play a sound only when we change between options
                    if self.game_opts.sound:
                        if self.option != self.option_previous:
                            play_sound(self.focus_sound, 0.2)
                # if there are any mouse buttons pressed down
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    # check the mouse's positions to
                    # know if move focus on a option
                    self._check_mouse_pos_for_focus()

                    # get mouse button events
                    lb, cb, rb = pygame.mouse.get_pressed()

                    # play when left button is pressed on focused option
                    if lb and self.mouse_focus:
                        if self.game_opts.sound:
                            play_sound(self.select_sound, 0.2)

                        self.options[self.option]['callable']()

        # menu options limits (cyclic sense)
        if self.option > len(self.options) - 1:
            self.option = 0
        elif self.option < 0:
            self.option = len(self.options) - 1

    ## check the mouse's positions to
    ## know if move focus on a option
    #
    # @param self the object pointer
    def _check_mouse_pos_for_focus(self):
        i = 0

        # get mouse position at the moment
        mouse_pos = pygame.mouse.get_pos()
        ml, mt = self.position

        # for each option in the menu
        for o in self.options:
            # get its label rectangle
            rect = o.get('label_rect')
            if rect:
                # if an option is focused, update that option and
                # then inform the caller that the mouse is focused
                if rect.collidepoint(mouse_pos):
                    self.option = i
                    self.mouse_focus = True
                    break
            i += 1
        else:
            # there was no mouse focus on menu options
            self.mouse_focus = False

    ## toggle the graphic of the menu options
    #
    # @param self the object pointer
    def toggle_image(self):
        self.image_enabled = not self.image_enabled

    ## set the top-left of the menu at x, y
    #
    # @param self the object pointer
    # @param x the x coordinate
    # @param y the y coordinate
    def set_position(self, x, y):
        ## menu's position (x, y)
        self.position = (x, y)

    ## set the top-left of the menu at x, y
    #
    # @param self the object pointer
    # @param position the x and y coordinates
    def _set_position(self, position):
        x, y = position
        self.x = x
        self.y = y

    ## set the font used for the menu
    #
    # @param self the object pointer
    # @param font the preloaded font
    def set_font(self, font):
        self.font = font

    ## set the font used for the menu
    #
    # @param self the object pointer
    # @param font the preloaded font
    def _set_font(self, font):
        self._font = font
        for o in self.options:
            o['font'] = font
        self._fix_size()

    ## set the highlight color of the menu options
    #
    # @param self the object pointer
    # @param color the color on focused options
    def set_highlight_color(self, color):
        self.focus_color = color

    ## set the normal color of the menu options
    #
    # @param self the object pointer
    # @param color the color on normal options
    def set_normal_color(self, color):
        self.normal_color = color

    ## center the menu at x, y
    #
    # @param self the object pointer
    # @param x the x coordinate
    # @param y the y coordinate
    def center_at(self, x, y):
        self.x = x - (self.width / 2.0)
        self.y = y - (self.height / 2.0)

    position = property(lambda self: (self.x, self.y), _set_position,
                        doc = """The menu position inside the container.""")

    font = property(lambda self: self._font, _set_font,
                    doc = """Font used by the menu.""")
