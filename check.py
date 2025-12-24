import webview

class Api:
    def test(self):
        print("Test")

api = Api()

# DIAGNOSTIC: Try to open a window WITH the bridge
try:
    print("Attempting to launch WITH js_api...")
    webview.create_window('Bridge Test', 'https://google.com', js_api=api)
    webview.start()
except Exception as e:
    print("\nFAILED. The JS Bridge is the cause.")
    print(e)
