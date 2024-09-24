#!/usr/bin/python

# file contains the gui class

# get modules
import pygame
import sys

from pygame.locals import *

from spqr_defines import *


# now of course we need a class to hold all of the windows, i.e. the basic GUI class
# this class also inits the gfx display
class SPQR_GUI:
    def __init__(self, width, height):
        self.windows = []
        pygame.init()
        # ok, now init the basic screen
        # set variable SPQR_FULLSCR to flip fullscreen/windowed (set in SPQR_defines.py)
        # done now so image.convert works when we load the images
        if SPQR_FULLSCR:
            self.screen = pygame.display.set_mode((width, height), HWSURFACE | FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((width, height), HWSURFACE)
        pygame.display.set_caption("SPQR " + VERSION)
        # next up is to load in some images into the gfx array
        self.images = []
        self.images.append(pygame.image.load("./gfx/map.png").convert())
        # add a back buffer map render.. this will become the map that we render
        foo = pygame.Surface((self.images[MAIN_MAP].get_width(), self.images[MAIN_MAP].get_height()))
        self.images.append(foo)
        self.images.append(pygame.image.load("./gfx/win_tl.png").convert())
        self.images.append(pygame.image.load("./gfx/win_lft.png").convert())
        self.images.append(pygame.image.load("./gfx/win_bl.png").convert())
        self.images.append(pygame.image.load("./gfx/win_bot.png").convert())
        self.images.append(pygame.image.load("./gfx/win_br.png").convert())
        self.images.append(pygame.image.load("./gfx/win_rgt.png").convert())
        self.images.append(pygame.image.load("./gfx/win_tr.png").convert())
        self.images.append(pygame.image.load("./gfx/win_top.png").convert())
        self.images.append(pygame.image.load("./gfx/win_lft_lg.png").convert())
        self.images.append(pygame.image.load("./gfx/win_bot_lg.png").convert())
        self.images.append(pygame.image.load("./gfx/win_rgt_lg.png").convert())
        self.images.append(pygame.image.load("./gfx/win_top_lg.png").convert())
        self.images.append(pygame.image.load("./gfx/button.png").convert())
        self.images.append(pygame.image.load("./gfx/small_map.png").convert())
        self.images.append(pygame.image.load("./gfx/eagle.png").convert())
        self.images.append(pygame.image.load("./gfx/soldier.png").convert())

        # set up the fonts
        pygame.font.init()
        self.fonts = []
        self.fonts.append(pygame.font.Font("./gfx/Dustismo_Roman.ttf", 14))
        self.fonts.append(pygame.font.Font("./gfx/Vera.ttf", 14))

        # some basic variables that SPQR uses regularly
        # where to start the map blit from when blasting it to the screen
        foo = (SCREEN_HEIGHT - (BBOX_HEIGHT + self.images[WIN_TL].get_height())) + 1
        # define the 'from' rectangle
        self.map_screen = pygame.Rect((0, 0, SCREEN_WIDTH, foo))
        # and the target rectangle for the blit:
        self.map_rect = pygame.Rect((0, (self.images[WIN_TL].get_height()) - 1, SCREEN_WIDTH, foo))
        # centre the map for the start blit
        self.map_screen.x = ROME_XPOS - (self.map_rect.w / 2)
        self.map_screen.y = ROME_YPOS - (self.map_rect.h / 2)
        # store a rect of the maximum map limits we can scroll to
        # obviously 0/0 for top left corner - this just denotes bottom right corner
        self.map_max_x = self.images[MAIN_MAP].get_width() - SCREEN_WIDTH
        self.map_max_y = self.images[MAIN_MAP].get_height() - self.map_rect.h
        # damn silly variable for the mini map rect blit
        self.y_offset_mini_map = BBOX_HEIGHT + self.images[WIN_TL].get_height()
        # a temp image for some uses
        self.temp_image = pygame.Surface((0, 0))
        # variables so callbacks and external code can communicate
        self.callback_temp = BUTTON_FAIL
        # a flag to see if a menu is waiting for input
        self.menu_active = False

        # set up the mini map
        self.blit_rect = pygame.Rect(0, 0, 0, 0)
        # calculate width and height of square to blit
        self.width_ratio = float(self.images[MAIN_MAP].get_width()) / float(self.images[SMALL_MAP].get_width() - 1)
        self.height_ratio = float(self.images[MAIN_MAP].get_height()) / float(self.images[SMALL_MAP].get_height() - 1)
        # LESSON: in python, you need to force the floats sometimes
        self.blit_rect.w = int(float(self.map_rect.w) / self.width_ratio)
        self.blit_rect.h = int(float(self.map_rect.h) / self.height_ratio)
        # boy, am I dreading the maths when we hit the economic simulation code :-)
        self.blit_border_width = self.blit_rect.w / 2
        self.blit_border_height = self.blit_rect.h / 2
        self.blit_border_x_max = self.images[SMALL_MAP].get_width() - self.blit_border_width
        self.blit_border_y_max = self.images[SMALL_MAP].get_height() - self.blit_border_height
        # pre-calculate some stuff
        self.mini_x_offset = SCREEN_WIDTH - (self.images[SMALL_MAP].get_width() + 7)
        self.mini_y_offset = SCREEN_HEIGHT - (self.images[SMALL_MAP].get_height() + 13)
        self.mini_source = pygame.Rect(0, 0, self.images[SMALL_MAP].get_width(), self.images[SMALL_MAP].get_height())
        self.mini_dest = pygame.Rect(self.mini_x_offset - 1, self.mini_y_offset - 1, 0, 0)
        self.update_mini_map()

        # set up buffer screen
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        # make background the standard colour
        self.background.fill((238, 238, 230))
        # display the changes
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

    # now a function to add a window
    # it has it's own function because it has to return the index number
    # of the created window
    def add_window(self, window):
        self.windows.append(window)
        # since we always append to the list, the index is always
        # the size of the array minus 1 (since we start the array at 0)
        index = len(self.windows) - 1
        # print "The index of this window is ",index
        return index

    # a function to redraw all the windows
    def update_gui(self):
        # before doing ANYTHING else, blit the map
        self.screen.blit(gui.images[MAIN_MAP], self.map_rect, self.map_screen)
        index = 0
        # we have to do the window testing in reverse to the way we blit, as the first
        # object blitted is on the 'bottom' of the screen, and we have to test from the top
        for foo in self.windows:
            if foo.display:
                # print "Displaying window #",index
                # print "x=",foo.rect.x,"  y=",foo.rect.y
                self.screen.blit(foo.image, (foo.rect.x, foo.rect.y))
            for bar in foo.items:
                # print "Got an ",bar.describe,"!"
                if bar.visible:
                    x1 = foo.rect.x + bar.rect.x
                    y1 = foo.rect.y + bar.rect.y
                    self.screen.blit(bar.image, (x1, y1))
            # if the current window is modal, quit this routine
            index += 1
            if foo.modal:
                break
        pygame.display.flip()

    # this one merely updates the map, rather than blit all those
    # gui things as well
    def update_map(self):
        self.screen.blit(self.images[MAIN_MAP], self.map_rect, self.map_screen)
        # before blitting the mini map rect, we need to update the mini map itself
        self.screen.blit(self.images[SMALL_MAP], self.mini_dest, self.mini_source)
        pygame.draw.rect(self.screen, (0, 0, 0), self.blit_rect, 1)
        pygame.display.flip()

    # and this one merely blits the cursor in the mini map
    def update_mini_map(self):
        # work out what the corrent co-ords are for the mini-map cursor
        xpos = self.map_screen.x / self.width_ratio
        ypos = self.map_screen.y / self.height_ratio
        self.blit_rect.x = xpos + self.mini_x_offset
        self.blit_rect.y = ypos + self.mini_y_offset
        self.screen.blit(self.images[SMALL_MAP], self.mini_dest, self.mini_source)
        pygame.draw.rect(self.screen, (0, 0, 0), self.blit_rect, 1)
        pygame.display.flip()

    # routine captures what event we got, then passes that message along
    # to the testing routine (i.e. this code only checks if a MOUSE event
    # happened, the later function checks if we got a GUI event)
    def check_inputs(self):
        event = pygame.event.poll()
        action = MOUSE_NONE
        # cancel current menu if we got mouse button down
        if event.type == MOUSEBUTTONDOWN and gui.menu_active == True:
            gui.menu_active = False
            return False
        if event.type != NOEVENT:
            # if it's a rmb down, then exit
            # TODO: Sort out a proper exit function
            if event.type == MOUSEBUTTONDOWN and event.button == 3:
                sys.exit(0)
            # was it left mouse button up?
            elif event.type == MOUSEBUTTONUP and event.button == 1:
                x, y = pygame.mouse.get_pos()
                action = MOUSE_LCLK
                gui.test_mouse(x, y, action)
            else:
                # have we moved?
                if event.type == MOUSEMOTION:
                    x, y = pygame.mouse.get_pos()
                    action = MOUSE_OVER
                    gui.test_mouse(x, y, action)
            if action == MOUSE_NONE:
                return False
            else:
                return True

    # simple: do we have to scroll the map? If so, do it now!
    def check_scroll_area(self, x, y):
        update = False
        if x == 0:
            if y == 0:
                # scroll down right
                self.map_screen.x -= SCROLL_DIAG
                self.map_screen.y -= SCROLL_DIAG
                update = True
            elif y == (SCREEN_HEIGHT - 1):
                # scroll up right
                self.map_screen.x -= SCROLL_DIAG
                self.map_screen.y += SCROLL_DIAG
                update = True
            else:
                # scroll the map right
                self.map_screen.x -= SCROLL_SPEED
                update = True
        elif x == (SCREEN_WIDTH - 1):
            if y == 0:
                # scroll down left
                self.map_screen.x += SCROLL_DIAG
                self.map_screen.y -= SCROLL_DIAG
                update = True
            elif y == (SCREEN_HEIGHT - 1):
                # scroll up left
                self.map_screen.x += SCROLL_DIAG
                self.map_screen.y += SCROLL_DIAG
                update = True
            else:
                # scroll map left
                self.map_screen.x += SCROLL_SPEED
                update = True
        elif y == 0:
            # scroll map down
            self.map_screen.y -= SCROLL_SPEED
            update = True
        elif y == (SCREEN_HEIGHT - 1):
            # scroll map up
            self.map_screen.y += SCROLL_SPEED
            update = True
        # so, if something, then we need to re-draw the screen display
        if update:
            # clear any menu flags we have
            gui.mouse_active = False
            # check the scroll areas...
            if self.map_screen.x < 0:
                self.map_screen.x = 0
            elif self.map_screen.x > gui.map_max_x:
                self.map_screen.x = gui.map_max_x
            if self.map_screen.y < 0:
                self.map_screen.y = 0
            elif self.map_screen.y > gui.map_max_y:
                self.map_screen.y = gui.map_max_y
            # and then finally draw it!
            self.update_mini_map()
            self.update_map()
            return True
        # return false if no update done
        return False

    # use this function to test the mouse against all objects
    # TODO: Explicitly return if mouse inside the window is not used, UNLESS
    #       the windows states otherwise (self.grab_mouse=False, maybe)
    def test_mouse(self, x, y, action):
        # print "Called, and got:"
        quit = False
        # normally I'd use for foo in self.windows, but we need to traverse
        # this list in the opposite direction to the way we render them
        index = len(self.windows) - 1
        while index > -1:
            foo = self.windows[index]
            index = index - 1
            if quit:
                return
            # if this is a modal window, then stop after processing:
            quit = foo.modal
            # is the mouse pointer inside the window, or is there any window at all?
            if foo.rect.collidepoint(x, y) == True or foo.display == False:
                # check all of the points inside the window
                for bar in foo.items:
                    if bar.active:
                        # don't forget to include the offsets into the window
                        x_off = x - foo.rect.x
                        y_off = y - foo.rect.y
                        if bar.rect.collidepoint(x_off, y_off):
                            # get offset into widget
                            x_widget = x_off - bar.rect.x
                            y_widget = y_off - bar.rect.y
                            # now test to see if we need to make a call
                            if action == MOUSE_OVER and bar.callbacks.mouse_over != mouse_over_std:
                                print("Do a mouse over on ", bar.describe)
                                return
                            elif action == MOUSE_LCLK and bar.callbacks.mouse_lclk != mouse_lclk_std:
                                # call the function
                                bar.callbacks.mouse_lclk(bar, x_widget, y_widget)
                                return
                            elif action == MOUSE_RCLK and bar.callbacks.mouse_rclk != mouse_rclk_std:
                                print("Do a mouse right click on ", bar.describe)
                                return
                            # and then exit
                            return
                # obviously not on an item, then!
                if foo.display:
                    bar = 1
            # print "  Inside a window"
            else:
                bar = 2
        # print "  Outside the windows"

    # this is the main game loop. There are 2 varients of it, one which keeps
    # looping forever, and a solo version which runs only once
    def main_loop(self):
        exit = False
        while not exit:
            pygame.event.pump()
            # ok main loop: after setting everything up, just keep calling gui.check_inputs()
            # we ignore any map scrolls if the top level window is model
            x, y = pygame.mouse.get_pos()
            if not self.windows[len(self.windows) - 1].modal:
                if self.check_scroll_area(x, y):
                    continue
            # now check normal events
            self.check_inputs()

    # this is the 'run once only' version of main_loop
    # TODO: Define all functions as I have done this one
    def main_loop_solo(self):
        """SPQR_Gui.main_loop() - call with nothing
		Returns True if map moved, false otherwise"""
        pygame.event.pump()
        x, y = pygame.mouse.get_pos()
        if not self.windows[len(self.windows) - 1].modal:
            if self.check_scroll_area(x, y):
                return True
        # now check normal events
        self.check_inputs()
        return False

    # function to draw a standard button
    def draw_button(self, text):
        # make a copy of the button bitmap
        foo = pygame.Surface((gui.images[BUTTON_STD].get_width(), gui.images[BUTTON_STD].get_height()))
        area = pygame.Rect((0, 0, foo.get_width(), foo.get_height()))
        foo.blit(gui.images[BUTTON_STD], area)
        # render the text
        bar = gui.fonts[FONT_VERA].render(text, True, (0, 0, 0))
        # centre the text and overlay it
        x = (gui.images[BUTTON_STD].get_width() - bar.get_width()) / 2
        y = (gui.images[BUTTON_STD].get_height() - bar.get_height()) / 2
        area = pygame.Rect((x, y, bar.get_width(), bar.get_height()))
        foo.blit(bar, area)
        return foo

    # tries to fit text onto a surface
    # returns False if area is too small, otherwise returns
    # True and actual renders it in the gui spare image
    def txt_fit(self, text, x, y, fnt):
        final_lines = []
        requested_lines = text.splitlines()
        # Create a series of lines that will fit on the provided rectangle
        for requested_line in requested_lines:
            if self.fonts[fnt].size(requested_line)[0] > x:
                words = requested_line.split(' ')
                # if any of our words are too long to fit, return.
                for word in words:
                    if self.fonts[fnt].size(word)[0] >= x:
                        # TODO: should actually handle long words, since a web address
                        # has been found to be too long for this code!
                        print("Error: Word was too long in label")
                        return False
                # Start a new line
                accumulated_line = ""
                for word in words:
                    test_line = accumulated_line + word + " "
                    # Build the line while the words fit.
                    if self.fonts[fnt].size(test_line)[0] < x:
                        accumulated_line = test_line
                    else:
                        final_lines.append(accumulated_line)
                        accumulated_line = word + " "
                final_lines.append(accumulated_line)
            else:
                final_lines.append(requested_line)
        # everything seemed to work ok.. so far!
        accumulated_height = 0
        for line in final_lines:
            if accumulated_height + self.fonts[fnt].size(line)[1] >= y:
                return False
            accumulated_height += self.fonts[fnt].size(line)[1]
        return True


# set up variables for main code
# create the gui object - sets up screen as well
gui = SPQR_GUI(SCREEN_WIDTH, SCREEN_HEIGHT)
