try:
    import smbus
except ImportError:
    from mock import smbus
import time
import socket
import subprocess
import random
from datetime import datetime

LCD_ADDR = 0x3e
RGB_ADDR = 0x60
bus = smbus.SMBus(1)

# ---------- LCD LOW LEVEL ----------
def lcd_cmd(cmd):
    bus.write_byte_data(LCD_ADDR, 0x80, cmd)
    time.sleep(0.002)

def lcd_data(data):
    bus.write_byte_data(LCD_ADDR, 0x40, data)
    time.sleep(0.002)

def lcd_init():
    lcd_cmd(0x38)
    lcd_cmd(0x39)
    lcd_cmd(0x14)
    lcd_cmd(0x70)
    lcd_cmd(0x56)
    lcd_cmd(0x6C)
    time.sleep(0.2)
    lcd_cmd(0x38)
    lcd_cmd(0x0C)
    lcd_cmd(0x01)

def lcd_clear():
    lcd_cmd(0x01)
    time.sleep(0.01)

def lcd_set_cursor(line, pos=0):
    addr = 0x80 + (0x40 * line) + pos
    lcd_cmd(addr)

def lcd_print(text):
    text = text.ljust(16)[:16]
    for char in text:
        lcd_data(ord(char))

# ---------- RGB ----------
def lcd_set_rgb(r, g, b):
    bus.write_byte_data(RGB_ADDR, 0x00, 0x00)
    bus.write_byte_data(RGB_ADDR, 0x01, 0x00)
    bus.write_byte_data(RGB_ADDR, 0x08, 0xAA)
    bus.write_byte_data(RGB_ADDR, 0x04, r)
    bus.write_byte_data(RGB_ADDR, 0x03, g)
    bus.write_byte_data(RGB_ADDR, 0x02, b)

# ---------- SYSTEM INFO ----------
def get_ip():
    try:
        result = subprocess.check_output(["hostname", "-I"], timeout=3)
        return result.decode().split()[0]
    except:
        return "No Network"

# ---------- MAIN ----------
FACES = [":)", ":(", ";)", ":D", ":|", ":o", ":p", ";D", "^^", ":3"]

def main():
    lcd_init()
    lcd_set_rgb(0, 32, 0)  # green

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lcd_set_cursor(0)
    lcd_print(now)

    ip = get_ip()
    face = random.choice(FACES)
    lcd_set_cursor(1)
    lcd_print(ip + " " + face)

if __name__ == "__main__":
    main()
