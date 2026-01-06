import win32gui 
import asyncio
import time
from pywinauto import Application
from removePIICheck import checkForPii
import threading
import keyboard 
import ctypes  
import tkinter as tk
from tkinter import messagebox

#TODO: Clean this up so a user can come and go from text edit area as they please, as well as 
# Don't have it make typing super difficult
class checkForFiles: 
    def isUserinAI():
        pii_checker = checkForPii()
        textData = '' 
        piiIsPresent = False 
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
                            hook = None 
                            if foundPII: 
                                 ctrl.draw_outline(colour='red')
                                 def on_enter(e):
                                    print('enter pressed')
                                    def show_msg():
                                        response = ctypes.windll.user32.MessageBoxW(0, "PII Detected! Send anyway?", "DLP Warning", 0x04 | 0x30 | 0x1000)
                                        if response == 6: # User clicked Yes
                                            try: keyboard.unhook_key(hook)
                                            except: pass
                                            keyboard.send('enter')
                                    
                                    threading.Thread(target=show_msg).start()
                                 hook = keyboard.on_press_key('enter', lambda e: on_enter(e), suppress=True)
                                 print("hook set")
                            while (foundPII and "Google Gemini" in win32gui.GetWindowText(whatisit)):
                                    #time.sleep(1)
                                    textData = ctrl.window_text()
                                    foundPII = pii_checker.analyze_text_for_pii(textData)
                                    if not foundPII: 
                                         ctrl.draw_outline(colour='green')
                                         try: 
                                              keyboard.unhook_key(hook)
                                         except: 
                                              pass 
                                         hook = None 
                                    whatisit = win32gui.GetForegroundWindow()
                            
                            if hook:
                                try: keyboard.unhook(hook)
                                except: pass
                                 
if __name__ == "__main__": 
    checkForFiles.isUserinAI() 
    