# -*- coding: utf-8 -*-

#    Game's Cut Scenes Implementation.
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


## @package cut_scenes
#  Game's Cut Scenes Implementation.
#
# This module contains the game's cut scenes implementation.


try:
    import pygame

    import constants
    import graphics

    from pygame.locals import *

    from os_utils import safe_exit
except ImportError, err:
    print ''.join(["Couldn't load module. ", err])
    exit(constants.MOD_IMP_ERR)


## objects imported when `from <module> import *' is used
__all__ = ['CutScenes']


## class for game's cut scenes action
#
class CutScenes(object):

    ## initialize in order to cut scenes
    #
    # @param self the object pointer
    # @param slides the list of slides images
    def __init__(self, slides):
        ## the screen surface
        self.screen = pygame.display.get_surface()

        ## the list of background slides
        self.slides = slides

        ## the blank background slide
        self.blank = graphics.load_image(
            constants.FILES['graphics']['intro']['blank'][0])[0].convert()

        ## set the alpha to maximum value
        self.alphavalue = 255

        ## create clock and track time
        self.clock = pygame.time.Clock()

        ## flag to indicate if the scene is finished
        self.is_finished = False

    ## run the slideshow
    #
    # @param self the object pointer
    def run(self):
        # perform cutscene slides main process
        for slide in self.slides:
            # while the alpha of the blank slide is not zero
            while self.alphavalue >= 0:
                # set the blank slide alternation delay 
                self.clock.tick(80)

                # decrease alpha value
                self.alphavalue -= 5

                # set the new alpha value of the blank slide
                self.blank.set_alpha(self.alphavalue)

                # blit the slide
                self.screen.blit(slide, (0, 0))

                # blit the blank slide
                self.screen.blit(self.blank, (0, 0))

                # display the screen surface
                pygame.display.update()

            # set the slides presence delay 
            time = 100

            # show the slide for some time
            while time >= 0:
                # delay for each time monad
                self.clock.tick(10)

                # blit the slide
                self.screen.blit(slide, (0, 0))

                # display the screen surface
                pygame.display.update()

                # intro event loop
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        # perform safe exit
                        safe_exit()

                # handle keyboard keys
                key = pygame.key.get_pressed()
                # when user presses return key or space key
                if key[K_RETURN] or key[K_SPACE]:
                    # force to go to the next slide
                    time = 0
                
                # decrease the time where a slide is showed
                time -= 1

            # while the alpha of the blank slide is not zero
            while self.alphavalue <= 255:
                # set the blank slide alternation delay 
                self.clock.tick(80)

                # decrease alpha value
                self.alphavalue += 5

                # set the new alpha value of the blank slide
                self.blank.set_alpha(self.alphavalue)

                # blit the slide
                self.screen.blit(slide, (0, 0))

                # blit the blank slide
                self.screen.blit(self.blank, (0, 0))

                # display the screen surface
                pygame.display.update()

        # the scene is finished
        self.is_finished = True
