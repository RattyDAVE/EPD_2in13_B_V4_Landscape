# EPD_2in13_B_V4_Landscape
Waveshare Pico ePaper 2.13 B V4 Landscape MicroPython Driver

This is a based off the official driver at https://github.com/waveshareteam/Pico_ePaper_Code/blob/main/python/Pico_ePaper-2.13-B_V4.py


To use:
```python
epd = EPD_2in13_B_V4_Landscape()
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

Resources
- https://www.waveshare.com/wiki/Pico-ePaper-2.13-B
- https://www.waveshare.com/w/upload/d/d8/2.13inch_e-Paper_%28B%29_V3_Specification.pdf
