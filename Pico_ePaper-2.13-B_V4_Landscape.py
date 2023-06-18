from machine import Pin, SPI
import framebuf
import utime

EPD_WIDTH = 250
EPD_HEIGHT = 128  # height is really 122 pixels, but the code needs it to be divisible by 8

RST_PIN         = 12
DC_PIN          = 8
CS_PIN          = 9
BUSY_PIN        = 13

lookup = [
    0x0, 0x8, 0x4, 0xc, 0x2, 0xa, 0x6, 0xe, 0x1, 0x9, 0x5, 0xd, 0x3, 0xb, 0x7, 0xf
]

def reverse(n):
    return (lookup[n & 0b1111] << 4) | (lookup[n >> 4])

class EPD_2in13_B_V4_Landscape:
    def __init__(self):
        self.reset_pin = Pin(RST_PIN, Pin.OUT)
        
        self.busy_pin = Pin(BUSY_PIN, Pin.IN, Pin.PULL_UP)
        self.cs_pin = Pin(CS_PIN, Pin.OUT)
        
        if EPD_HEIGHT % 8 == 0:
            self.height = EPD_HEIGHT
        else :
            self.HEIGHT = (EPD_HEIGHT // 8) * 8 + 8
        self.width = EPD_WIDTH
               
        self.spi = SPI(1)
        self.spi.init(baudrate=4000_000)
        self.dc_pin = Pin(DC_PIN, Pin.OUT)
                
        self.buffer_balck = bytearray(self.width * self.height // 8)
        self.buffer_red = bytearray(self.width * self.height // 8)
        
        self.imageblack = framebuf.FrameBuffer(self.buffer_balck, self.width, self.height, framebuf.MONO_VLSB)
        self.imagered = framebuf.FrameBuffer(self.buffer_red, self.width, self.height, framebuf.MONO_VLSB)
        self.init()

    def digital_write(self, pin, value):
        pin.value(value)

    def digital_read(self, pin):
        return pin.value()

    def delay_ms(self, delaytime):
        utime.sleep(delaytime / 1000.0)

    def spi_writebyte(self, data):
        self.spi.write(bytearray(data))

    def module_exit(self):
        self.digital_write(self.reset_pin, 0)

    # Hardware reset
    def reset(self):
        self.digital_write(self.reset_pin, 1)
        self.delay_ms(50)
        self.digital_write(self.reset_pin, 0)
        self.delay_ms(2)
        self.digital_write(self.reset_pin, 1)
        self.delay_ms(50)

    def send_command(self, command):
        self.digital_write(self.dc_pin, 0)
        self.digital_write(self.cs_pin, 0)
        self.spi_writebyte([command])
        self.digital_write(self.cs_pin, 1)

    def send_data(self, data):
        self.digital_write(self.dc_pin, 1)
        self.digital_write(self.cs_pin, 0)
        self.spi_writebyte([data])
        self.digital_write(self.cs_pin, 1)
        
    def send_data1(self, buf):
        self.digital_write(self.dc_pin, 1)
        self.digital_write(self.cs_pin, 0)
        self.spi.write(bytearray(buf))
        self.digital_write(self.cs_pin, 1)
        
    def ReadBusy(self):
        print('busy')
        while(self.digital_read(self.busy_pin) == 1): 
            self.delay_ms(10) 
        print('busy release')
        self.delay_ms(20)
        
    def TurnOnDisplay(self):
        self.send_command(0x20)  # Activate Display Update Sequence
        self.ReadBusy()

    def SetWindows(self, Xstart, Ystart, Xend, Yend):
        self.send_command(0x44) # SET_RAM_X_ADDRESS_START_END_POSITION
        self.send_data((Xstart>>3) & 0xFF)
        self.send_data((Xend>>3) & 0xFF)

        self.send_command(0x45) # SET_RAM_Y_ADDRESS_START_END_POSITION
        self.send_data(Ystart & 0xFF)
        self.send_data((Ystart >> 8) & 0xFF)
        self.send_data(Yend & 0xFF)
        self.send_data((Yend >> 8) & 0xFF)
        
    def SetCursor(self, Xstart, Ystart):
        self.send_command(0x4E) # SET_RAM_X_ADDRESS_COUNTER
        self.send_data(Xstart & 0xFF)

        self.send_command(0x4F) # SET_RAM_Y_ADDRESS_COUNTER
        self.send_data(Ystart & 0xFF)
        self.send_data((Ystart >> 8) & 0xFF)
    

    def init(self):
        print('init')
        self.reset()
        
        self.ReadBusy()   
        self.send_command(0x12)  #SWRESET
        self.ReadBusy()   

        self.send_command(0x01) #Driver output control      
        self.send_data(0xf9)
        self.send_data(0x00)
        self.send_data(0x00)

        self.send_command(0x11) #data entry mode       
        self.send_data(0x03)

        self.SetWindows(0, 0, self.height-1, self.width-1)
        self.SetCursor(0, 0)

        self.send_command(0x3C) #BorderWaveform
        self.send_data(0x05)

        self.send_command(0x18) #Read built-in temperature sensor
        self.send_data(0x80)

        self.send_command(0x21) #  Display update control
        self.send_data(0x80)
        self.send_data(0x80)

        self.ReadBusy()
        
        return 0       
        
    def display(self):
        self.send_command(0x24)
        h = int(self.height / 8)
        for j in range(0, self.width):
            for i in range(0, h):
                self.send_data(reverse(self.buffer_balck[i * self.width + (self.width - j - 1)]))
                
        self.send_command(0x26)
        h = int(self.height / 8)
        for j in range(0, self.width):
            for i in range(0, h):
                self.send_data(reverse(self.buffer_red[i * self.width + (self.width - j - 1)]))              
        self.TurnOnDisplay()

    
    def Clear(self, colorblack, colorred):
        self.send_command(0x24)
        self.send_data1([colorblack] * self.width * int(self.height / 8))
        
        self.send_command(0x26)
        self.send_data1([colorred] * self.width * int(self.height / 8))
                                
        self.TurnOnDisplay()

    def sleep(self):
        self.send_command(0x10) 
        self.send_data(0x01)
        
        self.delay_ms(2000)
        self.module_exit()
                
if __name__=='__main__':
    epd = EPD_2in13_B_V4_Landscape()
    epd.Clear(0xff, 0xff)
    
    epd.imageblack.fill(0xff)
    epd.imagered.fill(0xff)
    epd.imageblack.text("Waveshare", 0, 10, 0x00)
    epd.imagered.text("ePaper-2.13B", 0, 25, 0x00)
    epd.imageblack.text("RPi Pico", 0, 40, 0x00)
    epd.imagered.text("Hello World", 0, 55, 0x00)
    epd.display()
    epd.delay_ms(2000)
    
    epd.imagered.vline(10, 90, 40, 0x00)
    epd.imagered.vline(90, 90, 40, 0x00)
    epd.imageblack.hline(10, 90, 80, 0x00)
    epd.imageblack.hline(10, 130, 80, 0x00)
    epd.imagered.line(10, 90, 90, 130, 0x00)
    epd.imageblack.line(90, 90, 10, 130, 0x00)
    epd.display()
    epd.delay_ms(2000)
    
    epd.imageblack.rect(10, 150, 40, 40, 0x00)
    epd.imagered.fill_rect(60, 150, 40, 40, 0x00)
    epd.display()
    epd.delay_ms(2000)
        
    epd.Clear(0xff, 0xff)
    epd.delay_ms(2000)
    print("sleep")
    epd.sleep()
