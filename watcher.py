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
                        if "ql-editor textarea" in ctrl.class_name():
                            print(f"Type: {ctrl.class_name()} | Title: '{ctrl.window_text()}'")
                         #   try:
                         #       print(f"User Input: {ctrl.get_value()}")
                         #   except Exception:
                         #       print(f"User Input: {ctrl.window_text()}")
                    exit()
if __name__ == "__main__": 
    checkForFiles.isUserinAI() 
    