import win32gui 
import asyncio
from pywinauto import Application

class checkForFiles: 
    def isUserinAI(): 
        while(True):
            whatisit = win32gui.GetForegroundWindow()
            if "Google Gemini" in win32gui.GetWindowText(whatisit): 
                    geminiTitle = win32gui.GetWindowText(whatisit)
                    app = Application(backend="uia").connect(title_re=".*Gemini.*")
                    dlg = app.window(title_re=".*Gemini.*")
                    for ctrl in dlg.descendants():
                        if "chat-app" in ctrl.class_name():
                            pass    
                            
                    
                

if __name__ == "__main__": 
    checkForFiles.isUserinAI() 
    