#!/usr/bin/python

# get modules
import sys
import pygame
from pygame.locals import *
from spqr_defines import *
import spqr_gui as SGUI
import spqr_window as SWINDOW
import spqr_widgets as SWIDGET


# there are always some standard routines in any gui...here is a messagebox
# we start with the callbacks assigned to each button (if needed)
def msgbox_ok(handle, xpos, ypos):
    lgui.callback_temp = BUTTON_OK
    return BUTTON_OK


def msgbox_cancel(handle, xpos, ypos):
    lgui.callback_temp = BUTTON_CANCEL
    return BUTTON_CANCEL


def msgbox_yes(handle, xpos, ypos):
    lgui.callback_temp = BUTTON_YES
    return BUTTON_YES


def msgbox_no(handle, xpos, ypos):
    lgui.callback_temp = BUTTON_NO
    return BUTTON_NO


def msgbox_quit(handle, xpos, ypos):
    lgui.callback_temp = BUTTON_QUIT
    return BUTTON_QUIT


def msgbox_ignore(handle, xpos, ypos):
    lgui.callback_temp = BUTTON_IGNORE
    return BUTTON_IGNORE


# and then start with the actual routine itself
# flags are as defined above
# TODO: Make the messagebox update with a dirty rect, keep the
# old image and reupdate with the old image when done.
def messagebox(flags, text, font):
    # just quickly, did we have any buttons?
    if flags == 0:
        return BUTTON_FAIL
    # start by calculating the MINIMUM size for this messagebox and txt label
    txt_width = ((lgui.images[BUTTON_STD].get_width() + 8) * 3) + 4
    width = txt_width + ((lgui.images[WIN_TL].get_width() + 8) * 2)
    # get average size of height..
    height = (lgui.fonts[font].size("X")[1]) + 1
    # really short message?
    if lgui.fonts[font].size(text)[0] < txt_width:
        # then don't even bother with a 2nd line...easy
        # render text to spare image
        lgui.temp_image = lgui.fonts[font].render(text, 1, (0, 0, 0))
    else:
        # we KNOW we can't fit it into one line, try with 2,3,4 etc until it fits
        done = False
        ysize = height
        while not done:
            ysize = ysize + height
            done = lgui.txt_fit(text, txt_width, ysize, font)
        height = ysize
    # now we have the right size, lets render it!
    # start with a window, but work out the height first...
    wheight = height + lgui.images[WIN_TL].get_height() + lgui.images[WIN_BR].get_height() + 8
    # add height for sep bar (6) and buttons (2*button height)
    wheight += (lgui.images[BUTTON_STD].get_height() * 2) + 6

    # ok, the window gets rendered for us here
    index = lgui.add_window(SWINDOW.SPQR_Window(-1, -1, width, wheight, "Message", True))
    y = lgui.images[WIN_TL].get_height() + 8
    # print "Window details on messagebox():",y,width,height
    lgui.windows[index].add_item(SWIDGET.SPQR_Label(12, y, txt_width, height, text))
    # now add the seperator bar
    x = 12
    y += height + 5
    lgui.windows[index].add_item(SWIDGET.SPQR_Seperator(x, y, width - 24))
    y += 1 + (lgui.images[BUTTON_STD].get_height() / 2)
    # move x to the right, buttons are blitted from right to left
    x = width - 16 - (lgui.images[BUTTON_STD].get_width())
    # now we are ready to start printing buttons
    total_buttons = 0
    # logic is simple: found a button? yes, display it and
    # modify next print pos. quit if 4th button found
    if (flags & BUTTON_OK) != 0:
        slot = lgui.windows[index].add_item(SWIDGET.SPQR_Button(x, y, "OK"))
        # same for every instance of this little loop: add the callbacks
        lgui.windows[index].items[slot].callbacks.mouse_lclk = msgbox_ok
        x = x - (lgui.images[BUTTON_STD].get_width() + 12)
        total_buttons += 1
    if (flags & BUTTON_CANCEL) != 0:
        slot = lgui.windows[index].add_item(SWIDGET.SPQR_Button(x, y, "Cancel"))
        lgui.windows[index].items[slot].callbacks.mouse_lclk = msgbox_cancel
        x = x - (lgui.images[BUTTON_STD].get_width() + 12)
        total_buttons += 1
    if (flags & BUTTON_YES) != 0:
        slot = lgui.windows[index].add_item(SWIDGET.SPQR_Button(x, y, "Yes"))
        lgui.windows[index].items[slot].callbacks.mouse_lclk = msgbox_yes
        x = x - (lgui.images[BUTTON_STD].get_width() + 12)
        total_buttons += 1
    if ((flags & BUTTON_NO) != 0) & (total_buttons < 3):
        slot = lgui.windows[index].add_item(SWIDGET.SPQR_Button(x, y, "No"))
        lgui.windows[index].items[slot].callbacks.mouse_lclk = msgbox_no
        x = x - (lgui.images[BUTTON_STD].get_width() + 12)
        total_buttons += 1
    if ((flags & BUTTON_QUIT) != 0) & (total_buttons < 3):
        slot = lgui.windows[index].add_item(SWIDGET.SPQR_Button(x, y, "Quit"))
        lgui.windows[index].items[slot].callbacks.mouse_lclk = msgbox_quit
        x = x - (lgui.images[BUTTON_STD].get_width() + 12)
        total_buttons += 1
    if ((flags & BUTTON_IGNORE) != 0) & (total_buttons < 3):
        slot = lgui.windows[index].add_item(SWIDGET.SPQR_Button(x, y, "Ignore"))
        lgui.windows[index].items[slot].callbacks.mouse_lclk = msgbox_ignore
        total_buttons += 1
    # thats the graphics dealt with, make sure the whole window is modal
    lgui.windows[index].modal = True
    # actually display the messagebox
    lgui.update_gui()
    lgui.update_mini_map()
    # keep looping until we get a positive result
    lgui.callback_temp = BUTTON_FAIL
    while lgui.callback_temp == BUTTON_FAIL:
        lgui.main_loop_solo()
    # so we caught the answer, now we just have to tidy up
    # an active messagebox is ALWAYS top of the list, so just delete it
    # and then redraw the screen
    lgui.windows.pop()
    lgui.update_gui()
    lgui.update_map()
    # return the value we got
    return lgui.callback_temp


lgui = SGUI.gui
