# -*- coding: utf-8 -*-

#    Game's Manager.
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


## @package game_manager
#  Game's Manager.
#
# This module contains the game's manager which keeping
# track of the active scene (i.e. intro, menu, level 1,
# etc.), changing between scenes, etc.


try:
    import constants

    from fsm import FSM
    from intro import Intro
    from menu import Menu
except ImportError, err:
    print ''.join(["Couldn't load module. ", err])
    exit(constants.MOD_IMP_ERR)


## objects imported when `from <module> import *' is used
__all__ = ['GameManager']


## a game manager class
#
# The game manager is responsible for keeping
# track of the active scene (i.e. intro, menu,
# level 1, etc), changing between scenes, etc.
class GameManager(object):

    ## initialize the game manager
    #
    # @param self the object pointer
    # @param game_opts the game's command line options
    def __init__(self, game_opts):
        ## the game scenes/levels
        self.scenes = FSM()

        # set the scenes
        intro_state = Intro(game_opts)
        menu_state = Menu(game_opts)

        # group the scenes
        scenes = (intro_state, menu_state)

        # add the scenes to the state machine
        for s in scenes:
            self.scenes.add_state(s)
        
        # enable the active state
        self.scenes.active_state = intro_state

    ## execute the appropriate scene
    #
    # @param self the object pointer
    def run_scene(self):
        self.scenes.run()

    ## change (and start) the active scene
    #
    # @param self the object pointer
    # @param scene the name of the new active scene
    def set_active_scene(self, scene):
        self.scenes.set_state(scene)
        self.run_scene()
