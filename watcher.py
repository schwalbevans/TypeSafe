import win32gui 
import time
from pywinauto import Application
from removePIICheck import checkForPii
import threading
import keyboard 
import ctypes  
import tkinter as tk
import win32con

class Overlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.config(bg='fuchsia')
        self.frame = tk.Frame(self.root, bg='fuchsia', highlightthickness=3)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.root.withdraw()

    def show(self, rect, color):
        self.frame.config(highlightbackground=color)
        w = rect.right - rect.left
        h = rect.bottom - rect.top
        self.root.geometry(f"{w}x{h}+{rect.left}+{rect.top}")
        hwnd = self.root.winfo_id()
        style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT)        
        win32gui.SetLayeredWindowAttributes(hwnd, 0x00FF00FF, 0, win32con.LWA_COLORKEY)
        self.root.deiconify()
        self.root.update()

    def hide(self):
        self.root.withdraw()
        self.root.update()

class checkForFiles: 
    def __init__(self):
        self.pii_checker = checkForPii()
        self.hook = None
        self.overlay = Overlay()

    def _show_msg(self):
        """Shows the blocking message box in a separate thread."""
        response = ctypes.windll.user32.MessageBoxW(0, "PII Detected! Send anyway?", "DLP Warning", 0x04 | 0x30 | 0x1000)
        if response == 6: # User clicked Yes
            self._remove_hook()
            keyboard.send('enter')

    def _on_enter(self, e):
        """Callback for the keyboard hook."""
        print('enter pressed')
        threading.Thread(target=self._show_msg).start()

    def _remove_hook(self):
        """Safely removes the keyboard hook."""
        if self.hook:
            try:
                keyboard.unhook_key(self.hook)
            except (ValueError, KeyError):
                pass
            self.hook = None
            print("hook removed")

    def _set_hook(self):
        """Sets the keyboard hook if not already set."""
        if self.hook is None:
            self.hook = keyboard.on_press_key('enter', self._on_enter, suppress=True)
            print("hook set")

    def isUserinAI(self):
        """Main monitoring loop."""
        print("Watcher started...")
        while True:
            try:
                foreground_window = win32gui.GetForegroundWindow()
                window_title = win32gui.GetWindowText(foreground_window)

                if "Google Gemini" in window_title:
                    app = Application(backend="uia").connect(title_re=".*Gemini.*")
                    dlg = app.window(title_re=".*Gemini.*")
                    
                    editor = None
                    for ctrl in dlg.descendants():   
                        if "ql-editor textarea" in ctrl.class_name():
                            editor = ctrl
                            break
                    
                    if editor:
                        while "Google Gemini" in win32gui.GetWindowText(win32gui.GetForegroundWindow()):
                            text_data = editor.window_text()
                            found_pii = self.pii_checker.analyze_text_for_pii(text_data)

                            if found_pii: 
                                self.overlay.show(editor.rectangle(), 'red')
                                self._set_hook()
                            else:
                                if self.hook:
                                    self.overlay.show(editor.rectangle(), 'green')
                                    self._remove_hook()
                                else:
                                    self.overlay.hide()
                            
                            time.sleep(0.2) # Reduce CPU usage
                    
                    # Cleanup if we leave the window
                    self._remove_hook()
                    self.overlay.hide()
                
                else:
                    time.sleep(1)

            except Exception as e:
                # print(f"Error: {e}")
                self._remove_hook()
                self.overlay.hide()
                time.sleep(1)
                                 
if __name__ == "__main__": 
    watcher = checkForFiles()
    watcher.isUserinAI()