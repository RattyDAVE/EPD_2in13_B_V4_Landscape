import os

def wget(url, filename):
    from urequests import get
    r = get(url)
    with open(filename, 'wb') as f:
        f.write(r.content)
 
if not 'lib' in os.listdir():
    os.mkdir("/lib")

wget("https://raw.githubusercontent.com/RattyDAVE/EPD_2in13_B_V4_Landscape/main/EPD_2in13_B_V4_Landscape.py","lib/EPD_2in13_B_V4_Landscape.py")
