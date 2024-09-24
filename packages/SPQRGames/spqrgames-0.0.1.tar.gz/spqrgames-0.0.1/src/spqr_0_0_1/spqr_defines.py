#!/usr/bin/python

# this file contains the global variables for spqr

VERSION = "v0.0.9"
AUTHOR = "Chris Smith"
EMAIL = "maximinus@gmail.com"
SYSTEM = "GNU/Linux"
STARTED = "1st Jan 2005"
LAST_UPDATE = "20th Apr 2005"

# now place the equivalent of some defines
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCROLL_SPEED = 8
SCROLL_DIAG = 6
GOLDEN_RATIO = 1.618
SPQR_FULLSCR = True
ROME_XPOS = 850
ROME_YPOS = 799

# font's used by the game
FONT_DUSTISMO = 0
FONT_VERA = 1

# images loaded by the gui system, used to draw the gui
MAIN_MAP = 0
BACK_MAP = 1
WIN_TL = 2
WIN_LFT = 3
WIN_BL = 4
WIN_BOT = 5
WIN_BR = 6
WIN_RGT = 7
WIN_TR = 8
WIN_TOP = 9
WIN_LFT_LG = 10
WIN_BOT_LG = 11
WIN_RGT_LG = 12
WIN_TOP_LG = 13
BUTTON_STD = 14
SMALL_MAP = 15
IMG_EAGLE = 16
IMG_SOLDIER = 17

# mouse events as seen by the gui
MOUSE_NONE = 0
MOUSE_OVER = 1
MOUSE_LCLK = 2
MOUSE_RCLK = 3

# and then as seen by the callback list (this is a hack)
# TODO: Fix this hack by merging this and the above list together
#       mmm... replace all instances of M_xxx with MOUSE_xxx ?
M_NONE = 0
M_OVER = 1
M_LCLK = 2
M_RCLK = 3

# standard buttons that the messagebox function uses
BUTTON_FAIL = 0
BUTTON_OK = 1
BUTTON_CANCEL = 2
BUTTON_YES = 4
BUTTON_NO = 8
BUTTON_QUIT = 16
BUTTON_IGNORE = 32

# text layout types
LEFT_JUSTIFY = 0
RIGHT_JUSTIFY = 1
CENTRE_HORIZ = 2

# height of bottom box from bottom of screen
BBOX_HEIGHT = 140

# offsets for when we draw a pop-up menu to screen
MENU_X_OFFSET = 2
MENU_Y_OFFSET = 23
SEP_OFFSET = 15
SEP_HEIGHT = 9
SEP_HOFF = 4
MENU_FRSTSPC = 4
MENU_TXT_HGT = 8
MENU_SPACER = 8
MENU_WEX = 8
# alpha is from 0 to 255, where 0 is transparent
MENU_ALPHA = 128
# colour of the highlight
MENU_HLCOL = (170, 83, 83)
MENU_HBORDER = 6


# TODO: Need to define all the colours we use as well

# these are the standard callbacks, they should never be called
# they are here to prevent an exception should an unregistered
# event ever be called
def mouse_over_std(handle, x, y):
    print("Error: mouse_over_std called")
    return False


def mouse_lclk_std(handle, x, y):
    print("Error: mouse_lclk_std called")
    return False


def mouse_rclk_std(handle, x, y):
    print("Error: mouse_rclk_std called")
    return False
