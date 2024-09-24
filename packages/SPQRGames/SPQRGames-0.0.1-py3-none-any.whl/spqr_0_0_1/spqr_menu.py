#!/usr/bin/python

# get modules
import sys, pygame
from pygame.locals import *
from spqr_defines import *
import spqr_gui as SGUI
import spqr_widgets as SWIDGET


class SPQR_Menu_Child:
    def __init__(self, text, code):
        self.active = True
        self.visible = True
        self.text = text
        # rectangle is defined when the parent menu is drawn
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.callbacks = SWIDGET.SPQR_Callbacks("SPQR_Menu_Child_Callback")
        # less faffing as we add the menu code pointer right here in the constructor
        self.callbacks.mouse_lclk = code
        self.parent = False
        self.describe = "SPQR_Menu_Child"


# following 2 routines are placeholders - they are the standard routines called if
# you do NOT specify a routine to be called

# standard entry point when a menu parent is clicked
def menu_parent_click(handle, xpos, ypos):
    messagebox(BUTTON_OK, "You clicked a parent menu", FONT_VERA)
    return True


# and the same for a child click
def menu_child_click(handle, xpos, ypos):
    messagebox(button - ok, "You clicked a child menu", FONT_VERA)
    return True


class SPQR_Menu_Parent:
    def __init__(self, text):
        self.active = True
        self.visible = True
        self.text = text
        self.children = []
        # a place to store the graphics...
        self.image = pygame.Surface((1, 1))
        self.highlight = pygame.Surface((1, 1))
        # the area of this rect is set when the SPQR_menu is set up
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.callbacks = SWIDGET.SPQR_Callbacks("SPQR_Menu_Parent_Callback")
        self.callbacks.mouse_lclk = menu_parent_click
        self.parent = False
        self.describe = "SPQR_Menu_Parent"

    def add_child(self, child):
        self.children.append(child)
        return (len(self.children)) - 1


# this is the routine called when user clicks the mouse area
# it has to decide which menu was clicked
def parent_menu_call(handle, xpos, ypos):
    # first check if we are in the target areas
    # *titlebar has to be at top of screen for this to work*
    i = 0
    index = -1
    while i < len(handle.offsets):
        if handle.offsets[i].collidepoint(xpos, ypos):
            index = i
        i += 1
    if index == -1:
        return True
    # set the destination rect...
    w = handle.menu[index].image.get_width()
    h = handle.menu[index].image.get_height()
    dest = pygame.Rect((handle.offsets[index].x - MENU_X_OFFSET, MENU_Y_OFFSET, w, h))
    # make a copy of whats on the screen right here...
    screen_copy = pygame.Surface((dest.w, dest.h))
    screen_copy.blit(pygame.display.get_surface(), (0, 0), dest)
    # copy the menu image across
    lgui.screen.blit(handle.menu[index].image, dest)
    # and update the screen
    pygame.display.update(dest)

    # should halt and test mouse responses here
    # any click outside of menu - leave routine
    # any click inside the menu - do the code
    # any mouse_over in a valid menu option - highlight the menu option

    # loop forever
    exit_menu = False
    highlight_on = False
    last_highlight = pygame.Rect(1, 1, 1, 1)
    while not exit_menu:
        event = pygame.event.poll()
        # did user release the mouse?
        if event.type == MOUSEBUTTONUP and event.button == 1:
            x, y = pygame.mouse.get_pos()
            # outside our menu?
            if not dest.collidepoint(x, y):
                # no more work to do
                exit_menu = True
            else:
                # check to see if we clicked something...
                for foo in handle.menu[index].children:
                    hrect = pygame.Rect(foo.rect.x, foo.rect.y, foo.rect.w, foo.rect.h)
                    # offset into menu
                    hrect.x += dest.x
                    hrect.y += dest.y
                    # are we in this one?
                    if hrect.collidepoint(x, y):
                        # call the routine, clear up and then exit
                        foo.callbacks.mouse_lclk(foo, x, y)
                        exit_menu = True
        elif event.type == MOUSEMOTION:
            x, y = pygame.mouse.get_pos()
            # inside the menu?
            if dest.collidepoint(x, y) == True:
                # is the mouse NOT in the last_highlight? Cos if so, we
                # need to update that portion of then screen
                if last_highlight.collidepoint(x, y) == False:
                    last_highlight.x -= dest.x
                    last_highlight.y -= dest.y
                    # copy portion on menu to screen
                    lgui.screen.blit(handle.menu[index].image, dest)
                    # and update the screen
                    pygame.display.update(dest)
                # test against all highlights
                for foo in handle.menu[index].children:
                    hrect = pygame.Rect(foo.rect.x, foo.rect.y, foo.rect.w, foo.rect.h)
                    # offset into menu
                    hrect.x += dest.x
                    hrect.y += dest.y
                    # already highlighted this?
                    if last_highlight != hrect and hrect.w != 1:
                        # are we in this one?
                        if hrect.collidepoint(x, y) == True:
                            # draw the highlight
                            lgui.screen.blit(handle.menu[index].highlight, hrect)
                            pygame.display.update(dest)
                            highlight_on = True
                            last_highlight = hrect
    # tidy the screen back up again
    lgui.screen.blit(screen_copy, dest)
    pygame.display.update(dest)
    return True


# Here's a fairly complex one - the menu system, only ever one instance of in our code (?)
# it always occupies the top of the screen
class SPQR_Menu:
    def __init__(self, children):
        self.active = True
        self.visible = True
        self.parents = []
        # children is an array of arrays, with a one-on-one
        self.menu = children
        # load the base image we will use to generate the titlebar gfx
        titlebar = pygame.image.load("./gfx/titlebar.png").convert()
        # store the rect for later
        self.rect = pygame.Rect(0, 0, SCREEN_WIDTH, titlebar.get_height())
        # draw the top bar starting here
        # now work out what size the rhs pixmap text is
        rhs_txt = "SPQR " + VERSION
        rhs_txt_width = (lgui.fonts[FONT_VERA].size(rhs_txt)[0] + 8)
        # blit the lhs
        x_blits = int((SCREEN_WIDTH - rhs_txt_width - 51) / 8)
        self.image = pygame.Surface((SCREEN_WIDTH, titlebar.get_height()))
        dest = pygame.Rect(0, 0, 8, titlebar.get_height())
        for foo in range(x_blits - 6):
            self.image.blit(titlebar, dest)
            dest.x += 8
        # blit the rhs
        titlebar = pygame.image.load("./gfx/titlebar_fill.png").convert()
        dest.x = SCREEN_WIDTH - (rhs_txt_width + 56)
        while dest.x < SCREEN_WIDTH:
            self.image.blit(titlebar, dest)
            dest.x += titlebar.get_width()
        # ok, now we can add the text to the rhs:
        foo = lgui.fonts[FONT_VERA].render(rhs_txt, True, (0, 0, 0))
        dest.x = SCREEN_WIDTH - (rhs_txt_width + 8)
        dest.y = 4
        self.image.blit(foo, dest)
        # and then the menu on the lhs:
        # here is where we set up the rects for mouse selection
        self.offsets = []
        dest.x = 8
        for foo in self.menu:
            text = foo.text
            lgui.fonts[FONT_VERA].set_bold(True)
            itmp = lgui.fonts[FONT_VERA].render(text, True, (255, 255, 255))
            lgui.fonts[FONT_VERA].set_bold(False)
            self.image.blit(itmp, dest)
            # add rect area of this menu entry
            self.offsets.append(pygame.Rect((dest.x, 1, itmp.get_width() + 12, titlebar.get_height() - 1)))
            # calculate offset for next menu entry
            dest.x += itmp.get_width() + 16
            # draw the actual menu here as well
            self.menu_draw(foo)
        # finish the defines
        self.callbacks = SWIDGET.SPQR_Callbacks("SPQR_Menu_Callback")
        # now set so that the menu traps all the clicks on it
        self.callbacks.mouse_lclk = parent_menu_call
        self.parent = False
        self.describe = "SPQR_Menu"

    def menu_draw(self, menu):
        # draw a menu, given the menu
        pics = []
        height = 0
        i = 0
        width = 0
        sep_bar = False
        # firstly draw all the parts we need to fully render the menu image
        for foo in menu.children:
            # loop through all children of this menu
            text = foo.text
            # is it a seperator?
            if text == "sep":
                # remember that fact
                pics.append(pygame.Surface((1, 1)))
                sep_bar = True
                height += SEP_HEIGHT + MENU_FRSTSPC
            else:
                pics.append(lgui.fonts[FONT_VERA].render(text, True, (0, 0, 0)))
                height += pics[i].get_height() + MENU_TXT_HGT
            # longest section so far?
            if pics[i].get_width() > width:
                width = pics[i].get_width()
            i += 1
        # so then , do we need a sep bar? If so, draw it
        if sep_bar == True:
            bar = pygame.Surface((width, SEP_HEIGHT))
            bar.fill((246, 246, 246))
            pygame.draw.line(bar, (149, 149, 149), (0, SEP_HOFF), (width, SEP_HOFF), 1)
        # allow for blank pixels on either side, and some extra breathing space
        width += (MENU_SPACER * 2) + MENU_WEX
        # allow for vertical spacing as well
        height += +MENU_FRSTSPC
        # now place all of those renders together
        # allow for a 1 pixel border around the menu
        menu.image = pygame.Surface((width + 2, height + 2))
        # set background and draw border
        menu.image.fill((246, 246, 246))
        pygame.draw.line(menu.image, (220, 220, 220), (0, 0), (0, 0), 1)
        pygame.draw.line(menu.image, (220, 220, 220), (width + 1, 0), (width + 1, 0), 1)
        pygame.draw.line(menu.image, (220, 220, 220), (0, height + 1), (0, height + 1), 1)
        pygame.draw.line(menu.image, (220, 220, 220), (width + 1, height + 1), (width + 1, height + 1), 1)
        pygame.draw.line(menu.image, (194, 194, 194), (1, 0), (width, 0), 1)
        pygame.draw.line(menu.image, (194, 194, 194), (0, 1), (0, height), 1)
        pygame.draw.line(menu.image, (194, 194, 194), (width + 1, 1), (width + 1, height), 1)
        pygame.draw.line(menu.image, (194, 194, 194), (1, height + 1), (width, height + 1), 1)
        # now plop in the text
        dest = pygame.Rect((MENU_SPACER, (MENU_TXT_HGT / 2), menu.image.get_width() - 2, 0))
        dest.y += MENU_FRSTSPC
        # FINALLY we can draw what will be the highlight for this menu
        # the 32 is to force a 32 bit surface for alpha blitting
        txt_htest = MENU_TXT_HGT + MENU_SPACER + MENU_HBORDER
        menu.highlight = pygame.Surface((width, txt_htest), 0, 32)
        # then set the alpha value
        menu.highlight.set_alpha(MENU_ALPHA)
        # lets try to draw on this surface
        menu.highlight.fill(MENU_HLCOL)
        index = 0
        # now render the actual menu bar proper
        for text in pics:
            dest.h = text.get_height()
            if dest.h == 1:
                # draw the sep bar
                dest.h = bar.get_height()
                menu.image.blit(bar, dest)
                # store details for later
                menu.children[index].rect = pygame.Rect((1, 1, 1, 1))
                index += 1
                dest.y += SEP_HEIGHT + MENU_FRSTSPC
            else:
                # blit the text
                menu.image.blit(text, dest)
                # store the rect for mouse selection later
                menu.children[index].rect = pygame.Rect(
                    (dest.x - (MENU_SPACER - 1), dest.y - MENU_HBORDER, width, txt_htest))
                index += 1
                dest.y += dest.h + MENU_TXT_HGT
        # and thats it
        return True

    def add_menu(self, parent):
        self.parents.append(parent)
        return (len(self.parents)) - 1


lgui = SGUI.gui
