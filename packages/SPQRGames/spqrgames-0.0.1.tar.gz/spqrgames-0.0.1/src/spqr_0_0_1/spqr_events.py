#!/usr/bin/python

# get modules
import sys

import spqr_extras as SEXTRAS
import spqr_gui as SGUI
from spqr_defines import *


# found here are all the functions triggered by the various mouse events
# they must all have the structure
# def function_name(handle,xpos,ypos)
# where xpos and ypos are the offset into whatever was pushed, and handle
# being a pointer the twidget that was clicked

# we start with just the quit function (cos it's like real easy!)
def quit_spqr(handle, xpos, ypos):
    result = SEXTRAS.messagebox((BUTTON_OK | BUTTON_CANCEL), "Quit SPQR?", FONT_VERA)
    if result == BUTTON_OK:
        # exit the game
        sys.exit(0)


def centre_map(handle, xpos, ypos):
    result = SEXTRAS.messagebox((BUTTON_OK | BUTTON_CANCEL), "Centre map on Rome?", FONT_VERA)
    if result == BUTTON_OK:
        # centre map on rome
        lgui.map_screen.x = ROME_XPOS - (lgui.map_rect.w / 2)
        lgui.map_screen.y = ROME_YPOS - (lgui.map_rect.h / 2)
        lgui.update_mini_map()
        lgui.update_map()


def test_msgbox(handle, xpos, ypos):
    SEXTRAS.messagebox(BUTTON_OK, "Just a little test, so far...", FONT_VERA)
    return
    # first thing we need are the actual buttons, so lets's generate them...
    index = lgui.add_window(-1, -1, 364, 230, "Attack by Persians!", True)
    # add a button to the window
    lgui.windows[index].add_item(SPQR_Button(164, 184, "No"))
    lgui.windows[index].add_item(SPQR_Button(264, 184, "Yes"))
    # and then a label
    lmessage = "Syria reports that Sapor II has sacked Palmyra. "
    lmessage += "Shall we attack his forces with LegioXXIII, "
    lmessage += "currently based in Judaea?"
    lgui.windows[index].add_item(SPQR_Label(136, 44, 220, 112, lmessage))
    # then add the image
    lgui.windows[index].add_item(SPQR_Image(18, 36, 100, 118, IMG_SOLDIER))
    # finally, a seperator, to make it look nice ;-)
    lgui.windows[index].add_item(SPQR_Seperator(14, 162, 336))
    # now we have to add the callbacks all that:
    # Both buttons and the image (pop-up saying 'You clicked me!')
    return click_code


# left click on mini map gives us this
def mini_map_click(handle, xpos, ypos):
    # make the click point the centre:
    xpos = xpos - lgui.blit_border_width
    ypos = ypos - lgui.blit_border_height
    # convert to map co-ords
    xpos = xpos * lgui.width_ratio
    ypos = ypos * lgui.height_ratio
    # correct if out of range
    if xpos < 0:
        xpos = 0
    elif xpos > lgui.map_max_x:
        xpos = lgui.map_max_x
    if ypos < 0:
        ypos = 0
    elif ypos > lgui.map_max_y:
        ypos = lgui.map_max_y
    # pass result to gui
    lgui.map_screen.x = xpos
    lgui.map_screen.y = ypos
    # update the screen
    lgui.update_mini_map()
    lgui.update_map()
    return True


# here come the defines for the menu system, but let's start with a general
# one to say that that part still needs to be coded
def not_yet_coded(handle, xpos, ypos):
    SEXTRAS.messagebox(BUTTON_OK, "Sorry, this feature has yet to be coded", FONT_VERA)
    return True


def menu_help_about(handle, xpos, ypos):
    message = "SPQR " + VERSION + "\n"
    message += "Written by " + AUTHOR + "\n"
    message += "\nLast Update " + LAST_UPDATE
    SEXTRAS.messagebox(BUTTON_OK, message, FONT_VERA)
    return True


def menu_help_help(handle, xpos, ypos):
    message = "Hopefully, as the gui progresses, this area should be a fully "
    message += "functional help database.\n\nFor now though, I have to point you "
    message += "to the excellent SPQR website"
    SEXTRAS.messagebox(BUTTON_OK, message, FONT_VERA)
    return True


# here's the start of the menu click code!
def file_menu(handle, xpos, ypos):
    pass
    return True


lgui = SGUI.gui
