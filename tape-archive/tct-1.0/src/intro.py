# -*- coding: utf-8 -*-

#    Game's Intro Screen.
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


## @package intro
#  Game's Intro Screen.
#
# This module contains the game's intro screen implementation.


try:
    import pygame

    import sound_mixer
    import constants
    import graphics

    from cut_scenes import CutScenes
    from fsm import State
except ImportError, err:
    print ''.join(["Couldn't load module. ", err])
    exit(constants.MOD_IMP_ERR)


## objects imported when `from <module> import *' is used
__all__ = ['Intro']


## class for game's intro screen
#
class Intro(State):

    ## initialize the intro screen
    #
    # @param self the object pointer
    # @param game_opts the game's command line options
    def __init__(self, game_opts):
        # initialize the state
        State.__init__(self, 'intro')

        ## the game's command line options
        self.game_opts = game_opts

        ## the intro background slides
        self.slides = [
            graphics.load_image( # slide 0
                constants.FILES['graphics']['intro']['slides'][0])[0],

            graphics.load_image( # slide 1
                constants.FILES['graphics']['intro']['slides'][1])[0],

            graphics.load_image( # slide 2
                constants.FILES['graphics']['intro']['slides'][2])[0]
        ]

        ## a cut scenes object
        self.cs = CutScenes(self.slides)

        # set sound volume to minimum
        pygame.mixer.music.set_volume(0.0)

        # play the background music theme
        sound_mixer.play_music(
            constants.FILES['sounds']['menu']['share']['bg'][0])

        # pause or unpause music according to user preference
        if self.game_opts.music:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()

        # set sound volume to maximum
        pygame.mixer.music.set_volume(1.0)

    ## what to do when the intro is enabled
    #
    # @param self the object pointer
    def do_actions(self):
        # run the intro slideshow
        self.cs.run()

    ## what should be satisfied for enabling the next scene
    #
    # @param self the object pointer        
    # @return the name of the next scene        
    def check_conditions(self):
        # if the scene is finished, returns back
        # to the caller the name of the next one
        if self.cs.is_finished:
            return 'menu'

        # else return none
        return None
