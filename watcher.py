import win32gui 
import asyncio
class checkForFiles: 
    def isUserinAI(): 
        while(True):
            whatisit = win32gui.GetForegroundWindow()
            if "Google Gemini" in win32gui.GetWindowText(whatisit): 
                print("Gemini Found") 

if __name__ == "__main__": 
    checkForFiles.isUserinAI() 
    