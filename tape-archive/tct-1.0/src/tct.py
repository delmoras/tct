#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    Game's Main Entry.
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


## @package tct
#  Game's Main Entry.
#
# This module contains the game's main entry. It checks
# for any inserted command line options, forms a window
# and then starts the game manager for the rest things.


try:
    import os
    import sys

    import pygame

    import constants

    from parse_options import get_parsed_opts
    from graphics import load_image
    from game_manager import GameManager
except ImportError, err:
    print ''.join(["Couldn't load module. ", err])
    exit(constants.MOD_IMP_ERR)


## objects imported when `from <module> import *' is used
__all__ = ['main']


## the game's window title (in window mode)
GAME_WINDOW_TITLE = constants.GAME_PACKAGE


## game's entry point
#
def main():
    # change the current directory to the one of the game
    os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))

    # parse, get game's command line
    # options, return options' flags
    game_opts = get_parsed_opts()

    # make the window of the game always centered
    os.environ["SDL_VIDEO_CENTERED"] = "1"

    # set up the pygame system for the game
    pygame.init()

    # create game's window screen
    pygame.display.set_mode(
        (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT),
        pygame.FULLSCREEN if game_opts.fullscreen else 0)

    # set game's window title
    pygame.display.set_caption(GAME_WINDOW_TITLE)

    # set game's window icon
    pygame.display.set_icon(load_image(
        constants.FILES['graphics']['window']['icon'][0])[0])

    # hide game's mouse cursor
    pygame.mouse.set_visible(False)

    # create the game manager
    gm = GameManager(game_opts)

    # main loop flag
    main_loop_running = True

    # main game event loop
    while main_loop_running:
        # run the game manager        
        gm.run_scene()

        # on quit exit the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_loop_running = False

    # uninitialize all the pygame systems
    pygame.quit()

    # here the game terminates normally


# run the script if executed
if __name__ == '__main__':
    main()
