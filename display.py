import os
import struct

class Display:
    def __init__(self):
        self.row = 0
        self.font = BitmapFont()

    def get_string_bitmap(self,str):
        w = self.font.font_width
        h = self.font.font_height
        line=[]
        max_x = 100
        x = 0
        for c in str:
            char_bitmap = self.font.get_char(c)
            if char_bitmap is None:
                # character not found; skip it
                continue
            line.extend(char_bitmap)
            x += w
            line.extend([0])
            x += 1
            if x >= max_x:
                break
        return line
        
    # print a sring to the display
    def text(self,str):
        str_bitmap = self.get_string_bitmap(str)

        for y in range(self.font.font_height):
            px_row = ""
            for col in str_bitmap:
                px = " "
                if (col >> y) & 0x1:
                    px = "*"
                px_row += px
            print(px_row)
            self.row += 1

    def clear(self):
        _ = os.system("clear")
        self.row = 0
        
    def end(self):
        pass
        

# MicroPython basic bitmap font renderer.
# Author: Tony DiCola
# License: MIT License (https://opensource.org/licenses/MIT)
class BitmapFont:
    """A helper class to read binary font tiles and 'seek' through them as a
    file to display in a framebuffer. We use file access so we dont waste 1KB
    of RAM on a font!"""
    def __init__(self, font_name='font5x8.bin'):
        # Specify the drawing area width and height, and the pixel function to
        # call when drawing pixels (should take an x and y param at least).
        # Optionally specify font_name to override the font file to use (default
        # is font5x8.bin).  The font format is a binary file with the following
        # format:
        # - 1 unsigned byte: font character width in pixels
        # - 1 unsigned byte: font character height in pixels
        # - x bytes: font data, in ASCII order covering all 255 characters.
        #            Each character should have a byte for each pixel column of
        #            data (i.e. a 5x8 font has 5 bytes per character).
        self.font_name = font_name

        # Open the font file and grab the character width and height values.
        # Note that only fonts up to 8 pixels tall are currently supported.
        try:
            self._font = open(self.font_name, 'rb')
            self.font_width, self.font_height = struct.unpack('BB', self._font.read(2))
            # simple font file validation check based on expected file size
            if 2 + 256 * self.font_width != os.stat(font_name)[6]:
                raise RuntimeError("Invalid font file: " + font_name)
        except OSError:
            print("Could not find font file", font_name)
            raise
        except OverflowError:
            # os.stat can throw this on boards without long int support
            # just hope the font file is valid and press on
            pass

    def deinit(self):
        """Close the font file as cleanup."""
        self._font.close()

    def __enter__(self):
        """Initialize/open the font file"""
        self.__init__()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        """cleanup on exit"""
        self.deinit()

    def get_char(self, char):
        # retrieves the font data for the specified char
        # data is returned as an array of font_width bytes
        char_data = []
        for char_x in range(self.font_width):
            self._font.seek(2 + (ord(char) * self.font_width) + char_x)
            try:
                col = struct.unpack('B', self._font.read(1))[0]
            except RuntimeError:
                return None
            char_data.append(col)
        return char_data
        
    def draw_char(self, char, x, y, framebuffer, color, size=1): # pylint: disable=too-many-arguments
        """Draw one character at position (x,y) to a framebuffer in a given color"""
        size = max(size, 1)
        # Don't draw the character if it will be clipped off the visible area.
        #if x < -self.font_width or x >= framebuffer.width or \
        #   y < -self.font_height or y >= framebuffer.height:
        #    return
        # Go through each column of the character.
        for char_x in range(self.font_width):
            # Grab the byte for the current column of font data.
            self._font.seek(2 + (ord(char) * self.font_width) + char_x)
            try:
                line = struct.unpack('B', self._font.read(1))[0]
            except RuntimeError:
                continue # maybe character isnt there? go to next
            # Go through each row in the column byte.
            for char_y in range(self.font_height):
                # Draw a pixel for each bit that's flipped on.
                if (line >> char_y) & 0x1:
                    framebuffer.fill_rect(x + char_x*size, y + char_y*size, size, size, color)

    def width(self, text):
        """Return the pixel width of the specified text message."""
        return len(text) * (self.font_width + 1)

