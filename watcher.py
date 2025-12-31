import win32gui 
import asyncio
from pywinauto import Application
from removePIICheck import checkForPii


class checkForFiles: 
    def isUserinAI():
        textData = '' 
        while(True):
            whatisit = win32gui.GetForegroundWindow()
            if "Google Gemini" in win32gui.GetWindowText(whatisit): 
                    geminiTitle = win32gui.GetWindowText(whatisit)
                    app = Application(backend="uia").connect(title_re=".*Gemini.*")
                    dlg = app.window(title_re=".*Gemini.*")
                    for ctrl in dlg.descendants():   
                        if "ql-editor textarea" in ctrl.class_name():
                            textData = ctrl.window_text()
                            foundPII = checkForPii().analyze_text_for_pii(textData)
                            print(foundPII)
                    exit() 
                            #If user presses enter, check text before sending?
                            # or just while the user is typing if any data looks like pii! 
                            
                                
                            
                        
if __name__ == "__main__": 
    checkForFiles.isUserinAI() 
    