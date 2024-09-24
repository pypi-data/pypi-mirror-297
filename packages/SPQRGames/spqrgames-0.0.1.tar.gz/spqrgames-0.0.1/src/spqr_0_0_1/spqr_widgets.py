#!/usr/bin/python

# get modules
import sys, pygame
from pygame.locals import *
from spqr_defines import *
import spqr_gui as SGUI


# what follows is the base class used for the callback functions of thw widgets. Every
# widget has one, and you can modidy the widgets be pointing mouse_* to different functions
class SPQR_Callbacks:
    def __init__(self, description):
        self.mouse_over = mouse_over_std
        self.mouse_lclk = mouse_lclk_std
        self.mouse_rclk = mouse_rclk_std
        self.describe = description


# now a class for the items contained within the window
# this is the base class that you will only use to generate custom widgets
# in almost all cases you'll use the widgets defined by SPQR
class SPQR_Widget:
    def __init__(self, x, y, width, height):
        self.active = True
        self.visible = True
        self.rect = pygame.Rect(x, y, width, height)
        # add callbacks
        self.callbacks = SPQR_Callbacks("SPQR_Widget_Callback")
        # set an image up for later
        self.image = False
        # following used to store the parent window of the
        # widget... False if there is no valid parent
        self.parent = False
        self.describe = "SPQR_Widget"


# TODO: Build all of these items by subclassing the SPQR_Item one 
# place the standard items here, starting with a label
class SPQR_Label:
    def __init__(self, x, y, width, height, text):
        self.active = True
        self.visible = True
        self.rect = pygame.Rect(x, y, width, height)
        self.background_colour = (238, 238, 230)
        self.text_colour = (0, 0, 0)
        self.font = FONT_VERA
        self.justification = LEFT_JUSTIFY
        self.text = text
        self.callbacks = SPQR_Callbacks("SPQR_Label_Callback")
        # render the image text
        if self.build_label() == False:
            # well, something went wrong, lets create an empty gfx
            self.image = pygame.Surface((self.rect.w, self.rect.h))
            self.image.fill(self.background_colour)
        self.parent = False
        self.describe = "SPQR_Label"

    # code for the following routine taken from the Pygame code repository.
    # written by David Clark, amended by Chris Smith
    def build_label(self):
        final_lines = []
        requested_lines = self.text.splitlines()
        # Create a series of lines that will fit on the provided rectangle
        for requested_line in requested_lines:
            if lgui.fonts[self.font].size(requested_line)[0] > self.rect.w:
                words = requested_line.split(' ')
                # if any of our words are too long to fit, return.
                for word in words:
                    if lgui.fonts[self.font].size(word)[0] >= self.rect.w:
                        print("Error: Word (", word, ") was too long in label")
                        print("       Width was more than ", self.rect.w)
                        return False
                # Start a new line
                accumulated_line = ""
                for word in words:
                    test_line = accumulated_line + word + " "
                    # Build the line while the words fit.
                    if lgui.fonts[self.font].size(test_line)[0] < self.rect.w:
                        accumulated_line = test_line
                    else:
                        final_lines.append(accumulated_line)
                        accumulated_line = word + " "
                final_lines.append(accumulated_line)
            else:
                final_lines.append(requested_line)
        # Let's try to write the text out on the surface.
        self.image = pygame.Surface((self.rect.w, self.rect.h))
        self.image.fill(self.background_colour)
        accumulated_height = 0
        for line in final_lines:
            if accumulated_height + lgui.fonts[self.font].size(line)[1] >= self.rect.h:
                print("Error: Text string too tall in label")
                print("       ah=", accumulated_height, " h=", self.rect.h)
                return False
            if line != "":
                tempsurface = lgui.fonts[self.font].render(line, 1, self.text_colour)
                if self.justification == LEFT_JUSTIFY:
                    self.image.blit(tempsurface, (0, accumulated_height))
                elif self.justification == CENTRE_HORIZ:
                    self.image.blit(tempsurface, ((self.rect.w - tempsurface.get_width()) / 2, accumulated_height))
                elif self.justification == RIGHT_JUSTIFY:
                    self.image.blit(tempsurface, (self.rect.w - tempsurface.get_width(), accumulated_height))
                else:
                    print("Error: Invalid justification value in label")
                    return False
            accumulated_height += lgui.fonts[self.font].size(line)[1]
        return True


# possibly something even SIMPLER than the label - an image
class SPQR_Image:
    def __init__(self, x, y, width, height, image):
        self.active = True
        self.visible = True
        self.rect = pygame.Rect(x, y, width, height)
        # add the usual callbacks
        self.callbacks = SPQR_Callbacks("SPQR_Image_Callback")
        # image will be cropped if it's bigger than the supplied co-ords
        self.image = pygame.Surface((width, height))
        self.image.blit(lgui.images[image], (0, 0))
        self.parent = False
        self.describe = "SPQR_Image"


# and the simplest of all - a seperator bar
# regardless of width, they all have a height of 2
class SPQR_Seperator:
    def __init__(self, x, y, width):
        self.active = True
        self.visible = True
        self.rect = pygame.Rect(x, y, width, 2)
        self.image = pygame.Surface((width, 2))
        # now blit the 2 colours to the image
        pygame.draw.line(self.image, (80, 84, 80), (0, 0), (width, 0), 1)
        pygame.draw.line(self.image, (248, 252, 248), (0, 1), (width, 1), 1)
        # even sep bars have callbacks!
        self.callbacks = SPQR_Callbacks("SPQR_Seperator_Callback")
        self.parent = False
        self.describe = "SPQR_Seperator"


# and now a button
class SPQR_Button:
    def __init__(self, x, y, text):
        self.active = True
        self.visible = True
        width = lgui.images[BUTTON_STD].get_width()
        height = lgui.images[BUTTON_STD].get_height()
        self.rect = pygame.Rect(x, y, width, height)
        self.callbacks = SPQR_Callbacks("SPQR_Button_Callback")
        # get the image, please!
        self.image = lgui.draw_button(text)
        self.parent = False
        self.describe = "SPQR_Button"


lgui = SGUI.gui
