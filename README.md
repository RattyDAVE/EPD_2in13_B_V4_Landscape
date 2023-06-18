# EPD_2in13_B_V4_Landscape
Waveshare Pico ePaper 2.13 B V4 Landscape MicroPython Driver

This is a based off the official driver at https://github.com/waveshareteam/Pico_ePaper_Code/blob/main/python/Pico_ePaper-2.13-B_V4.py


To use:
```python
epd = EPD_2in13_B_V4_Landscape()
```

Example test usage
```python
from EPD_2in13_B_V4_Landscape import EPD_2in13_B_V4_Landscape

epd = EPD_2in13_B_V4_Landscape()
    
epd.imageblack.fill(0xff)
epd.imagered.fill(0xff)
epd.imageblack.text("This is a Test", 0, 10, 0x00)
epd.display()
```

All other methods function as normal.

```python
epd.Clear(0xff, 0xff)
epd.imageblack.fill(0xff)
epd.imagered.fill(0xff)
epd.imageblack.text("Waveshare", 0, 10, 0x00)
epd.imagered.text("ePaper-2.13B", 0, 25, 0x00)
epd.imageblack.text("RPi Pico", 0, 40, 0x00)
epd.imagered.text("Hello World", 0, 55, 0x00)
epd.display()
```

## Methods

### Draw the original shape

The following methods to draw shapes on framebuffer。

```python
epd.imageblack.fill(c)
epd.imagered.fill(c)
```

Fills the entire framebuffer with the specified color。

```python
epd.imageblack.pixel(x, y[, c])
epd.imagered.pixel(x, y[, c])
```

If C is not given, the color value of the specified pixel is obtained. If C is given, the specified pixel is set to the given color.

```python
epd.imageblack.hline(x, y, w, c)
epd.imagered.hline(x, y, w, c)
```

```python
epd.imageblack.vline(x, y, h, c)
epd.imagered.vline(x, y, h, c)
```

```python
epd.imageblack.line(x1, y1, x2, y2, c)
epd.imagered.line(x1, y1, x2, y2, c)
```

Draws a line from a set of coordinates using a given color and a thickness of 1 pixel. The line method draws lines to the second set of coordinates, while the hline 和 vline methods draw horizontal and vertical lines respectively until the given length.

```python
epd.imageblack.rect(x, y, w, h, c)
epd.imagered.rect(x, y, w, h, c)
```

```python
epd.imageblack.fill_rect(x, y, w, h, c)
epd.imagered.fill_rect(x, y, w, h, c)
```

Draws a rectangle at a given location, size, and color. The rect method only draws 1 pixel outline, while th fill_rect method for drawing contour and interior.


### Draw Text

```python
epd.imageblack.text(s, x, y[, c])
epd.imagered.text(s, x, y[, c])
```

Use coordinates as top left corner of text to write text to FrameBuffer . The color of the text can be defined by optional parameters, but the default value is 1. The size of all characters is 8x8 pixels, and currently the font cannot be changed.

### Other methods

```python
epd.imageblack.scroll(xstep, ystep)
epd.imagered.scroll(xstep, ystep)
```

Move the contents of FrameBuffer according to the given vector. This may leave footprints of previous colors in FrameBuffer .

```python
epd.imageblack.blit(fbuf, x, y[, key])
epd.imagered.blit(fbuf, x, y[, key])
```

Draw another FrameBuffer on the current one at the given coordinates`. If key is specified, it should be a color integer, and the corresponding color will be treated as transparent: all pixels with that color value will not be drawn.

This method works between instances of FrameBuffer with different formats, but due to color format mismatch, the resulting color may be unexpected.

## Resources
- https://www.waveshare.com/wiki/Pico-ePaper-2.13-B
- https://www.waveshare.com/w/upload/d/d8/2.13inch_e-Paper_%28B%29_V3_Specification.pdf
