#!/usr/bin/python

# get modules
import sys, pygame
from pygame.locals import *
from spqr_defines import *
import spqr_gui as SGUI


# define an SPQR_Window
class SPQR_Window:
    def __init__(self, x, y, width, height, title, draw):
        self.active = True
        self.display = draw
        self.modal = False
        self.describe = "SPQR_Window"
        # use info as a storage for any of your own stuff
        # (you can use it to pass variables between function callbakcs, for example
        self.info = 0
        # if the passed values for x and y are -1 then
        # place the window at the centre of the screen
        if x == -1 or y == -1:
            x = (SCREEN_WIDTH - width) / 2
            y = (SCREEN_HEIGHT - height) / 2
        self.rect = pygame.Rect((x, y, width, height))
        self.caption = title
        # finally, we need a list of the items...
        self.items = []
        # now lets actually draw the window, if needed
        if draw == True:
            # get an image of the required size
            self.image = pygame.Surface((self.rect.w, self.rect.h))
            # flood fill it with grey and get a standard rectangle
            self.image.fill((238, 238, 230))
            foo = pygame.Rect((0, 0, 0, 0))
            # ok, we start with the sides, with some clever blitting
            # basically blit 4*4 images until you can only do 4*1 ones
            foo.x = 0
            foo.y = lgui.images[WIN_TL].get_height()
            lrg_draw = int((self.rect.h - foo.y) / 4)
            sml_draw = (self.rect.h - foo.y) - (lrg_draw * 4)
            offset = self.rect.w - lgui.images[WIN_RGT].get_width()
            for bar in range(lrg_draw):
                # blit the large images
                self.image.blit(lgui.images[WIN_LFT_LG], foo)
                foo.x += offset
                self.image.blit(lgui.images[WIN_RGT_LG], foo)
                foo.x -= offset
                foo.y += 4
            # ok, now the final small ones
            if sml_draw != 0:
                for bar in range(sml_draw):
                    self.image.blit(lgui.images[WIN_LFT], foo)
                    foo.x += offset
                    self.image.blit(lgui.images[WIN_RGT], foo)
                    foo.x -= offset
                    foo.y += 1
            # same sort of routine for the top and bottom
            foo.y = 0
            foo.x = lgui.images[WIN_TL].get_width()
            lrg_draw = int((self.rect.w - foo.x) / 4)
            sml_draw = (self.rect.w - foo.x) - (lrg_draw * 4)
            offset = self.rect.h - lgui.images[WIN_BOT].get_height()
            for bar in range(lrg_draw):
                # again, the large blits (as can be seen from their name)
                self.image.blit(lgui.images[WIN_TOP_LG], foo)
                foo.y += offset
                self.image.blit(lgui.images[WIN_BOT_LG], foo)
                foo.y -= offset
                foo.x += 4
            # then the small top/bottom fillers
            if sml_draw != 0:
                for bar in range(sml_draw):
                    self.image.blit(lgui.images[WIN_TOP], foo)
                    foo.y += offset
                    self.image.blit(lgui.images[WIN_BOT], foo)
                    foo.y -= offset
                    foo.x += 1
            # now draw in all of the corners
            foo = pygame.Rect((0, 0, 0, 0))
            self.image.blit(lgui.images[WIN_TL], foo)
            foo.y = self.rect.h - lgui.images[WIN_BL].get_height()
            self.image.blit(lgui.images[WIN_BL], foo)
            foo.x = self.rect.w - lgui.images[WIN_BR].get_width()
            self.image.blit(lgui.images[WIN_BR], foo)
            foo.y = 0
            self.image.blit(lgui.images[WIN_TR], foo)
            # right, all that's left to do is draw the text over the title bar
            # firstly render the text in it's own little gfx area
            lgui.fonts[FONT_VERA].set_bold(True)
            bar = lgui.fonts[FONT_VERA].render(title, True, (0, 0, 0))
            lgui.fonts[FONT_VERA].set_bold(False)
            # set it to centre of title bar
            foo.x = ((self.rect.w + (lgui.images[WIN_TL].get_width() * 2)) - bar.get_width()) / 2
            foo.y = ((lgui.images[WIN_TL].get_height() - bar.get_height()) / 2) + 1
            # render to image
            self.image.blit(bar, foo)
        else:
            # just in case we ever accidentally blit it, we define it anyway:
            self.image = pygame.Surface((0, 0))

    # add an item to the list with this code
    # TODO: me says, remove this code? why essentially rename a python function?
    # possible answer: Consistency. We add window items with the same name.
    def add_item(self, new_item):
        self.items.append(new_item)
        # we add to the last item, index is thus len()-1
        index = len(self.items) - 1
        # we now have a valid parent to add
        self.items[index].parent = self
        return index


lgui = SGUI.gui
