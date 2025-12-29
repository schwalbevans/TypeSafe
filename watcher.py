import win32gui 
import asyncio
class checkForFiles: 
    while(True):
        whatisit = win32gui.GetForegroundWindow()
        print(win32gui.GetWindowText(whatisit))

if __name__ == "__main__": 
    pass