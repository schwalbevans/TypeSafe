import win32gui 
import asyncio
import time
from pywinauto import Application
from removePIICheck import checkForPii

#TODO: Clean this up so a user can come and go from text edit area as they please, as well as 
# Don't have it make typing super difficult
class checkForFiles: 
    def isUserinAI():
        pii_checker = checkForPii()
        textData = '' 
        while(True):
            time.sleep(1)
            whatisit = win32gui.GetForegroundWindow()
            if "Google Gemini" in win32gui.GetWindowText(whatisit): 
                    geminiTitle = win32gui.GetWindowText(whatisit)
                    app = Application(backend="uia").connect(title_re=".*Gemini.*")
                    dlg = app.window(title_re=".*Gemini.*")
                    for ctrl in dlg.descendants():   
                        if "ql-editor textarea" in ctrl.class_name():
                            textData = ctrl.window_text()
                            foundPII = pii_checker.analyze_text_for_pii(textData)
                            ctrl.set_edit_text(foundPII)
                            
                      
                            
                            
                                
                            
                        
if __name__ == "__main__": 
    checkForFiles.isUserinAI() 
    