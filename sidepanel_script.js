chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === 'UPDATE_BUTTON_TEXT') {
        const subjectCode = message.subjectCode;
        console.log("received message");
        document.getElementById('button1').textContent = `"Tell me what's the prerequisite for ${subjectCode}"`;
        document.getElementById('button2').textContent = `"What are the learning outcomes for ${subjectCode}?"`;
        document.getElementById('button3').textContent = `"How many assessments does ${subjectCode} have?"`;
        sendResponse({ received: true });
    }
    return true;
});