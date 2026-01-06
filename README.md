🛡️ RedactOS (Alpha)
  The OS-Level Privacy Guard for AI.
  
  RedactOS is an open-source security tool that prevents sensitive data (PII) from leaking into AI models like Gemini, ChatGPT, and Claude.
  
  Unlike browser extensions, which are blind to desktop apps, RedactOS uses Windows Accessibility APIs to monitor text fields at the operating system level. It sits quietly in the background and only activates when you are typing into a known AI interface.

⚠️ ALPHA RELEASE WARNING
  This software is currently in active development (v0.1.0).
  
  Do not use for critical compliance needs yet.
  
  Expect bugs, especially on non-standard screen resolutions.
  
  Current Support: Best experienced on Google Gemini in Chrome/Edge on Windows 10/11.
  
  We are releasing this early to gather feedback from the security and developer community. Please report bugs in the Issues tab.

✨ Features
  OS-Level Interception: Uses uiautomation to read text fields directly from the window manager.
  
  Privacy Filters: Only scans text when the active window title matches an AI provider (e.g., "ChatGPT", "Gemini", "Claude"). We do not scan your banking or email windows.
  
  Local Processing: All PII detection happens locally on your machine using Python and Regex/Microsoft Presidio. No data is ever sent to the cloud.
  
  Visual Guard: Draws a transparent red overlay over the text box when secrets are detected.

🚀 Installation (for Developers)
  RedactOS is written in Python. To run the Alpha, you need Python 3.10+ installed.
  
  Clone the repository:
  
  Bash
  
  git clone https://github.com/YOUR_USERNAME/RedactOS.git
  cd RedactOS
  Install dependencies:
  
  Bash
  
  pip install -r requirements.txt
  (Note: This installs uiautomation, pyqt6, and presidio-analyzer)
  
  Run the Guard:
  
  Bash
  
  python watcher.py
  
🛠️ Usage
  Run the script. You will see [RedactOS] Privacy Filter Active in your console.
  
  Open Google Gemini (gemini.google.com) in your browser.
  
  Type a test secret into the prompt, for example:
  
  "My secret credit card is 4000 1234 5678 9010"
  
  You should see a Red Border appear around the text box.
  
  If you try to hit ENTER, RedactOS will block the input and warn you.

🗺️ Roadmap
  [x] v0.1: Basic Text Interception on Windows (Gemini Support).
  
  [ ] v0.2: Support for ChatGPT Desktop App, ChatGPT Web and Microsoft Copilot Desktop.
  
  [ ] v0.3: "Sanitize & Send" Popup Menu.
  
  [ ] v0.4: File Upload Interception (.pdf, .docx).

  [ ] v0.5: File Upload Interception (.pdf, .docx).
  
  

📄 License & Commercial Use
  RedactOS is open-source software licensed under the GNU Affero General Public License v3.0 (AGPLv3).
  
  What this means:
  You are free to: Use, modify, and distribute this software.
  
  The Catch: If you modify this software and use it as part of a service (internal or external), you must release your source code changes to the public under the same license.

💼 Commercial License
  Do you want to use RedactOS in your company without open-sourcing your modifications? 
  
  We will offer a Commercial License that removes the AGPL restrictions and includes:
  
  Signed MSI Installers (Easy deployment).
  
  Centralized Admin Dashboard.
  
  Priority Support.
  
  Join the Waitlist for RedactOS Pro

🤝 Contributing
  We welcome Pull Requests! We are specifically looking for help with:
  
  Improving the Regex patterns in engine.py.
  
  Reducing false positives in input_guard.py.
  
  Adding support for macOS (Accessibility API).
  
  Disclaimer: RedactOS is a security tool, not a guarantee. It is designed to catch accidental leaks, but no tool is 100% perfect. Always verify what you send to AI models.
