#!/usr/bin/python

# SPQR source code, Copyright 2024 CHUA某人
# Inspiration comes from Chris Smith's same project.See it at https://sourceforge.net/projects/spqr/

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

# design notes go here:

# The interface
# there are 3 parts to this: the menu bar at the top - DO NOT add widgets here
# The main map - again, do NOT add widgets here, unless you are prepared to have the
# image wiped when the map moves (so a pop-up menu would be ok)
# finally, the bottom info screen. THIS is where to place new widgets 

# get modules
import pygame

import spqr_events as SEVENT
import spqr_gui as SGUI
import spqr_menu as SMENU
import spqr_widgets as SWIDGET
import spqr_window as SWINDOW
from spqr_defines import *


# now include my own libs


# TODO: Place tests for lib loads here (use a message box)
# TODO: Convert all those odd images you use to the screen format
# TODO: Implement a middle mouse button drag map function

# routine to init everything...
def init():
	# start by defining the menu system that we want
	menu = [SMENU.SPQR_Menu_Parent("File"), SMENU.SPQR_Menu_Parent("Empire"), SMENU.SPQR_Menu_Parent("Help")]
	# then add the sub menus below these
	menu[0].add_child(SMENU.SPQR_Menu_Child("Load Game", SEVENT.not_yet_coded))
	menu[0].add_child(SMENU.SPQR_Menu_Child("Save Game", SEVENT.not_yet_coded))
	# this is a seperate, drawn bar to spli the text
	menu[0].add_child(SMENU.SPQR_Menu_Child("sep", SEVENT.not_yet_coded))
	menu[0].add_child(SMENU.SPQR_Menu_Child("Exit SPQR", SEVENT.quit_spqr))
	menu[1].add_child(SMENU.SPQR_Menu_Child("Vist Senate", SEVENT.not_yet_coded))
	menu[1].add_child(SMENU.SPQR_Menu_Child("Military Advice", SEVENT.not_yet_coded))
	menu[1].add_child(SMENU.SPQR_Menu_Child("Statistics", SEVENT.not_yet_coded))
	menu[2].add_child(SMENU.SPQR_Menu_Child("About", SEVENT.menu_help_about))
	menu[2].add_child(SMENU.SPQR_Menu_Child("sep", SEVENT.not_yet_coded))
	menu[2].add_child(SMENU.SPQR_Menu_Child("Help", SEVENT.menu_help_help))

	# Add the menubar at the top. It has no drawn window -
	index = lgui.add_window(SWINDOW.SPQR_Window(0, 0, 0, 0, "", False))
	# add the prepared menu onto this
	lgui.windows[index].add_item(SMENU.SPQR_Menu(menu))

	# now'll we have the main box underneath what will be the map
	# start with the window, of course
	index = lgui.add_window(SWINDOW.SPQR_Window(0, SCREEN_HEIGHT - BBOX_HEIGHT, SCREEN_WIDTH, BBOX_HEIGHT, "", False))
	# now we want to build up the window image
	lgui.windows[index].image = pygame.Surface((SCREEN_WIDTH, BBOX_HEIGHT))
	lgui.windows[index].image.fill((238, 238, 230))
	# draw the bar on the top
	pygame.draw.line(lgui.windows[index].image, (254, 120, 120), (0, 0), (SCREEN_WIDTH, 0), 1)
	pygame.draw.line(lgui.windows[index].image, (171, 84, 84), (0, 1), (SCREEN_WIDTH, 1), 2)
	pygame.draw.line(lgui.windows[index].image, (104, 51, 51), (0, 3), (SCREEN_WIDTH, 3), 1)
	# 2 more things here - the eagle design on the left to start
	w = lgui.images[IMG_EAGLE].get_width()
	h = lgui.images[IMG_EAGLE].get_height()
	lgui.windows[index].add_item(SWIDGET.SPQR_Image(4, 10, w, h, IMG_EAGLE))
	# and the mini-map on the rhs
	w = lgui.images[SMALL_MAP].get_width()
	h = lgui.images[SMALL_MAP].get_height()
	x = SCREEN_WIDTH - (lgui.images[SMALL_MAP].get_width() + 8)
	slot = lgui.windows[index].add_item(SWIDGET.SPQR_Image(x, 12, w, h, SMALL_MAP))
	lgui.windows[index].items[slot].callbacks.mouse_lclk = SEVENT.mini_map_click
	lgui.windows[index].display = True

	# add a test messagebox button.. this will be the quit button to start with
	x = SCREEN_WIDTH - (lgui.images[SMALL_MAP].get_width() + lgui.images[BUTTON_STD].get_width() + 16)
	slot = lgui.windows[index].add_item(SWIDGET.SPQR_Button(x, 12, "Quit"))
	# add the callback routine
	lgui.windows[index].items[slot].callbacks.mouse_lclk = SEVENT.quit_spqr
	lgui.windows[index].items[slot].describe = "The Messagebox"

	y = lgui.windows[index].items[slot].rect.y + 36
	slot = lgui.windows[index].add_item(SWIDGET.SPQR_Button(x, y, "Rome"))
	lgui.windows[index].items[slot].callbacks.mouse_lclk = SEVENT.centre_map

	y += 36
	slot = lgui.windows[index].add_item(SWIDGET.SPQR_Button(x, y, "Test"))
	lgui.windows[index].items[slot].callbacks.mouse_lclk = SEVENT.test_msgbox

	# update the screen
	lgui.update_gui()
	lgui.update_map()


# this is where actual code starts
# init the code - gui needs to be defined here to make it global
print("Please wait, initing() SPQR...")
# setup everything else
lgui = SGUI.gui
init()
# call the gui main loop
lgui.main_loop()
