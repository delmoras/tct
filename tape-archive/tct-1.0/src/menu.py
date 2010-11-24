# -*- coding: utf-8 -*-

#    Game's Menu Screen.
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


## @package menu
#  Game's Menu Screen.
#
# This module handles both the main and settings menus of
# the game. Menus get user events and trigger operations.


try:
    import os

    import pygame

    import sound_mixer
    import constants
    import graphics

    from os_utils import file_path, safe_exit
    from utils import get_time_sec
    from anim_sprite import *
    from credits import Credits
    from kezmenu import KezMenu
    from fsm import State
except ImportError, err:
    print ''.join(["Couldn't load module. ", err])
    exit(constants.MOD_IMP_ERR)


## objects imported when `from <module> import *' is used
__all__ = ['Menu']

## the main menu's position x co-ordinate
MENU_MAIN_POS_X = 525

## the main menu's position y co-ordinate
MENU_MAIN_POS_Y = 285

## menu keyboard repeat delay
MENU_KEY_DEL = 500

## menu keyboard repeat interval
MENU_KEY_INT = 200

## animated sprite speed
ANIM_SPRITE_SPEED = 200.0

## animated sprite alpha (on settings)
ANIM_SPRITE_ALPHA = 80.0


## class for game's menu screen
#
class Menu(State):

    ## initialize both the main and settings menu
    #
    # @param self the object pointer
    # @param game_opts the game's command line options
    def __init__(self, game_opts):
        # initialize the state
        State.__init__(self, 'menu')

        ## the game's command line options
        self.game_opts = game_opts

        ## the screen surface
        self.screen = pygame.display.get_surface() 

        ## flag to control the settings menu's loop
        self.menu_settings_running = None

        ## flag to control the main menu's loop
        self.menu_main_running = True

        # enable key repeat for the menu
        pygame.key.set_repeat(MENU_KEY_DEL, MENU_KEY_INT)

        ## set the main menu's background
        self.menu_main_bg = graphics.load_image(
            constants.FILES['graphics']['menu']['main']['bg'][0])[0]

        ## set the settings menu's background
        self.menu_settings_bg = graphics.load_image(
            constants.FILES['graphics']['menu']['share']['bg'][0])[0]

        ## set the settings menu's background box
        self.menu_box_bg = graphics.load_image(
            constants.FILES['graphics']['menu']['settings']['box'][0])[0]

        ## set the window frame
        self.window_frame = graphics.load_image(
            constants.FILES['graphics']['menu']['share']['frame'][0])[0]

        ## set the mouse cursor
        self.mouse_cursor = graphics.load_image(
            constants.FILES['graphics']['menu']['share']['cursor'][0])[0]

        ## set the sound when a menu option is entered
        self.select_option_snd = sound_mixer.load_sound(
            constants.FILES['sounds']['menu']['share']['sel'][0])

        ## create the main menu - string, callback function
        self.menu_main = KezMenu(self.game_opts,
                         ['Play'     , self._play_option],
                         ['Settings' , self._settings_option],
                         ['Credits'  , self._credits_option],
                         ['Quit'     , self._quit_option])

        # set the position of the main menu
        self.menu_main.set_position(MENU_MAIN_POS_X, MENU_MAIN_POS_Y)

        # set the main menu's font
        self.menu_main.set_font(graphics.load_font(
            constants.FILES['fonts']['menu']['share'][0], 30))

        # set the main menu's highlight color
        self.menu_main.set_highlight_color(pygame.Color('brown'))

        ## create the settings menu - string, callback function
        self.menu_settings = KezMenu(self.game_opts,
                             ['Fullscreen' , self._toggle_fullscreen_option],
                             ['Sounds'     , self._toggle_sounds_option],
                             ['Music'      , self._toggle_music_option],
                             ['Back'       , self._back_option])

        # disable the menu graphic for focused options
        self.menu_settings.toggle_image()

        # set the settings menu's font
        self.menu_settings.set_font(graphics.load_font(
            constants.FILES['fonts']['menu']['share'][0], 25))

        # set the position of the settings menu
        self.menu_settings.center_at(constants.SCREEN_WIDTH / 2.0,
                                     constants.SCREEN_HEIGHT / 2.0)
    
        # set the settings menu's highlight color
        self.menu_settings.set_highlight_color(pygame.Color('orange'))

        ## the animated sprite group
        self.anim_sprites = pygame.sprite.RenderUpdates()

        # vertical sprite sample
        self.anim_sprites.add(VertAnimSprite(
                constants.FILES['graphics']['menu']['share']['anim'][0],
                [0, 0], ANIM_SPRITE_SPEED))

        # horizontal sprite sample
        self.anim_sprites.add(HorAnimSprite(
                constants.FILES['graphics']['menu']['share']['anim'][1],
                [0, 0], ANIM_SPRITE_SPEED))

        ## create clock and track time
        self.clock = pygame.time.Clock()

    ## what to do when the main menu is enabled
    #
    # @param self the object pointer
    def do_actions(self):

        # display & update screen, get all the events
        while self.menu_main_running:
            # draw the background
            self.screen.blit(self.menu_main_bg, (0, 0))

            # count time passed in seconds
            time_passed_seconds = get_time_sec(self.clock.tick(50))

            # animate the sprites
            self.anim_sprites.update(time_passed_seconds)
            rectlist = self.anim_sprites.draw(self.screen)

            # draw the main menu
            self.menu_main.draw(self.screen)

            # draw the custom mouse cursor
            graphics.handle_mouse_cursor(self.mouse_cursor, self.screen)

            # draw the frame of the window
            self.screen.blit(self.window_frame, (0, 0))

            # display the screen surface
            pygame.display.update()
            
            # clear the sprites 
            self.anim_sprites.clear(self.screen, self.menu_main_bg)

            # get all the events
            events = pygame.event.get()

            # ......... and update the main menu
            # which needs access to those events
            self.menu_main.update(events)

            # main menu event loop
            for e in events:
                # quit when the close button is pressed
                if e.type == pygame.QUIT:
                    self._quit_option()
                # handle keyboard keys
                elif e.type == pygame.KEYDOWN:
                    # play the sound if there was a menu key shortcut
                    if self.game_opts.sound:
                        if e.key in (pygame.K_p, pygame.K_s, pygame.K_c):
                            sound_mixer.play_sound(
                                self.select_option_snd, 0.2)

                    # when user presses escape or 'q'uit key
                    if e.key in (pygame.K_ESCAPE, pygame.K_q):
                        self._quit_option()
                    # when user presses 'p'lay key
                    elif e.key == pygame.K_p:
                        self._play_option()
                    # when user presses 's'ettings key
                    elif e.key == pygame.K_s:
                        self._settings_option()
                    # when user presses 'c'redits key
                    elif e.key == pygame.K_c:
                        self._credits_option()

    ## entry point for main menu's settings option
    #
    # @param self the object pointer
    def _settings_option(self):
        # each time we enter in settings
        # sub menu, set the flag to true
        self.menu_settings_running = True

        # decrease the alpha of animated sprites
        for s in self.anim_sprites:
            s.image.set_alpha(ANIM_SPRITE_ALPHA)

        # display & update screen, get all the events
        while self.menu_settings_running:
            # draw the background
            self.screen.blit(self.menu_settings_bg, (0, 0))

            # draw the main menu
            self.menu_main.draw(self.screen)

            # count time passed in seconds
            time_passed_seconds = get_time_sec(self.clock.tick(50))

            # animate the sprites
            self.anim_sprites.update(time_passed_seconds)
            rectlist = self.anim_sprites.draw(self.screen)
            
            # draw settings menu background box
            self.screen.blit(self.menu_box_bg, (
             (constants.SCREEN_WIDTH - self.menu_box_bg.get_width()) / 2.0,
             (constants.SCREEN_HEIGHT - self.menu_box_bg.get_height()) / 2.0))

            # draw the settings menu
            self.menu_settings.draw(self.screen)

            # draw the custom mouse cursor
            graphics.handle_mouse_cursor(self.mouse_cursor, self.screen)

            # draw the frame of the window
            self.screen.blit(self.window_frame, (0, 0))

            # display the screen surface
            pygame.display.update()

            # clear the sprites
            self.anim_sprites.clear(self.screen, self.menu_main_bg)

            # get all the events
            events = pygame.event.get()

            # ..... and update the settings menu
            # which needs access to those events
            self.menu_settings.update(events)

            # settings menu event loop
            for e in events:
                # quit when the close button is pressed
                if e.type == pygame.QUIT:
                    self._back_option()
                    self._quit_option()
                # handle keyboard keys
                elif e.type == pygame.KEYDOWN:
                    # play the sound if there was a menu key shortcut
                    if self.game_opts.sound:
                        if e.key in (pygame.K_f, pygame.K_s, pygame.K_m,
                                     pygame.K_b, pygame.K_ESCAPE):
                            sound_mixer.play_sound(
                                self.select_option_snd, 0.2)

                    # when user presses escape key or 'b'ack key
                    if e.key in (pygame.K_ESCAPE, pygame.K_b):
                        self._back_option()
                    # when user presses 'f'ullscreen key
                    elif e.key == pygame.K_f:
                        self._toggle_fullscreen_option()
                    # when user presses 's'ounds key
                    elif e.key == pygame.K_s:
                        self._toggle_sounds_option()
                    # when user presses 'm'usic key
                    elif e.key == pygame.K_m:
                        self._toggle_music_option()

        # restore the alpha of the animated sprites
        for s in self.anim_sprites:
            s.image.set_alpha(255)

    ## entry point for main menu's new game option
    #
    # @param self the object pointer
    def _play_option(self):
        if self.game_opts.verbose:
            print 'Start a new game.'

    ## entry point for main menu's credits option
    #
    # @param self the object pointer
    def _credits_option(self):

        # get the path of the filename
        fullname = file_path(
            constants.FILES['texts']['menu']['credits']['text'][0],
            constants.TEXTS_DIR)

        # if credits text file exists and is readable
        if os.access(fullname, os.F_OK) and os.access(fullname, os.R_OK):
            if self.game_opts.verbose:
                print 'Go to the credits screen.'

            # create the credits screen
            c = Credits(self.screen,
                        self.game_opts,
                        self.window_frame,
                        self.menu_settings_bg,
                        self.select_option_snd,
                        fullname)

            # run the credits screen
            if not c.run():
                # quit if the close button is
                # pressed (inside the credits)
                self._quit_option()
        else:
            print ''.join(["Couldn't text file: ", fullname])

    ## entry point for main menu's quit option
    #
    # @param self the object pointer
    def _quit_option(self):
        if self.game_opts.verbose:
            print 'Exit the game!'

        # perform safe exit
        safe_exit()

    ## entry point for settings menu's toggle fullscreen option
    #
    # @param self the object pointer
    def _toggle_fullscreen_option(self):
        self.game_opts.fullscreen = not self.game_opts.fullscreen

        if self.game_opts.verbose:
            print 'Toggle fullscreen!'

        # store the position of the mouse cursor
        mouse_position = pygame.mouse.get_pos()

        # toggle the fullscreen <-> window mode
        pygame.display.set_mode(
            (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT),
            pygame.FULLSCREEN if self.game_opts.fullscreen else 0)

        # update the mouse cursor position
        pygame.mouse.set_pos(mouse_position)

    ## entry point for settings menu's toggle sounds option
    #
    # @param self the object pointer
    def _toggle_sounds_option(self):
        self.game_opts.sound = not self.game_opts.sound
        if self.game_opts.verbose:
            print 'Toggle sounds!'

    ## entry point for settings menu's toggle music option
    #
    # @param self the object pointer
    def _toggle_music_option(self):
        if self.game_opts.verbose:
            print 'Toggle music!'

        self.game_opts.music = not self.game_opts.music
        if self.game_opts.music:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()

    ## entry point for settings menu's back option
    #
    # @param self the object pointer
    def _back_option(self):
        self.menu_settings_running = False
        if self.game_opts.verbose:
            print 'Go back to main menu!'
