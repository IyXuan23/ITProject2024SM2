const chatElementRef = document.getElementById('chat-element');

function updateButtonTexts(subjectCode) {
    const button1 = chatElementRef.shadowRoot.querySelector('#button1');
    const button2 = chatElementRef.shadowRoot.querySelector('#button2');
    const button3 = chatElementRef.shadowRoot.querySelector('#button3');

    if (button1 && button2 && button3) {
        button1.textContent = `"Tell me what's the prerequisite for ${subjectCode}"`;
        button2.textContent = `"What are the learning outcomes for ${subjectCode}?"`;
        button3.textContent = `"How many assessments does ${subjectCode} have?"`;
    } else {
        console.error('No elements found with IDs button1, button2, or button3');
    }
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === 'UPDATE_BUTTON_TEXT') {
        console.log("received message");
        const subjectCode = message.subjectCode;
        updateButtonTexts(subjectCode);
        sendResponse({ received: true });
    }
    return true;
});