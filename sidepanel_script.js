const chatElementRef = document.getElementById('chat-element');

function updateButtonTexts(subjectCode, courseCode) {
    const button1 = chatElementRef.shadowRoot.querySelector('#button1');
    const button2 = chatElementRef.shadowRoot.querySelector('#button2');
    const button3 = chatElementRef.shadowRoot.querySelector('#button3');

    if (button1 && button2 && button3 && subjectCode) {
        button1.textContent = `Tell me what's the prerequisite for ${subjectCode}`;
        button2.textContent = `What are the learning outcomes for ${subjectCode}?`;
        button3.textContent = `How many assessments does ${subjectCode} have?`;
    }
    if (button1 && button2 && button3 && courseCode) {
        button1.textContent = `Tell me what's the entry requirement for ${courseCode}?`;
        button2.textContent = `What are the learning outcomes for ${courseCode}?`;
        button3.textContent = `whats the course structure of ${courseCode}?`;
    }
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === 'UPDATE_BUTTON_TEXT_SUBJECT') {
        console.log("received message");
        const subjectCode = message.subjectCode;
        updateButtonTexts(subjectCode, null);
        sendResponse({ received: true });
    }
    if (message.type === 'UPDATE_BUTTON_TEXT_COURSE') {
        console.log("received message");
        const courseCode = message.courseCode;
        updateButtonTexts(null, courseCode);
        sendResponse({ received: true });
    }
    return true;
});