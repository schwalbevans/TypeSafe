import win32gui 
import asyncio
import pywinauto 

class checkForFiles: 
    def isUserinAI(): 
        while(True):
            whatisit = win32gui.GetForegroundWindow()
            if "Google Gemini" in win32gui.GetWindowText(whatisit): 
                    print(win32gui.Get)
                

if __name__ == "__main__": 
    checkForFiles.isUserinAI() 
    