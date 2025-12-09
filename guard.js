console.log("[JS] Guard Script Loaded into Page.");

// 1. Establish Connection to Python
// We wait 1 second to ensure QWebChannel library is loaded
setTimeout(() => {
    if (typeof QWebChannel === 'undefined') {
        console.error("[JS] QWebChannel library missing!");
        return;
    }
    
    new QWebChannel(qt.webChannelTransport, function(channel) {
        window.pyBridge = channel.objects.airlock;
        console.log("[JS] 🔒 Connected to Python Bridge.");
        startWatcher();
    });
}, 1000);


// 2. Watch for the Chat Box
function startWatcher() {
    console.log("[JS] Starting DOM Watcher...");
    const observer = new MutationObserver(() => {
        // Selector for ChatGPT input box (div with contenteditable)
        // We look for 'prompt-textarea' ID which ChatGPT currently uses
        const box = document.getElementById('prompt-textarea');
        
        if (box && !box.dataset.secured) {
            attachLock(box);
        }
    });
    observer.observe(document.body, { childList: true, subtree: true });
}


// 3. Intercept 'Enter' Key
function attachLock(element) {
    console.log("[JS] 🛡️ Secure Lock Attached to Input Box.");
    element.dataset.secured = "true";
    
    element.addEventListener('keydown', (e) => {
        // If Enter is pressed (without Shift)
        // TODO: Add in ability to check if the user sends message by clicking send button and not just enter 
        if (e.key === 'Enter' && !e.shiftKey) {
            
            // A. STOP the send immediately
            e.preventDefault();
            e.stopImmediatePropagation();
            
            // B. Get Text
            const text = element.innerText || element.value;
            console.log("[JS] Keydown Intercepted. Sending to Python: ", text);
            
            // C. Send to Python
            if (window.pyBridge) {
                window.pyBridge.check_text(text); // TODO: Stops message from sending wether or not it's malicious
            }
        }
    }, true); // Use Capture Phase
}