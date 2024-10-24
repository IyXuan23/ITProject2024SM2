const chatElementRef = document.getElementById('chat-element');

function updateButtonTexts(subjectCode, courseCode) {

    const button1 = chatElementRef.shadowRoot.querySelector('#button1');
    const button2 = chatElementRef.shadowRoot.querySelector('#button2');
    const button3 = chatElementRef.shadowRoot.querySelector('#button3');
    const button1text = chatElementRef.shadowRoot.querySelector('#button1text');
    const button2text = chatElementRef.shadowRoot.querySelector('#button2text');
    const button3text = chatElementRef.shadowRoot.querySelector('#button3text');

    button1.style.display = 'block';
    button2.style.display = 'block';
    button3.style.display = 'block';

    if (subjectCode) {
        button1text.textContent = `Does ${subjectCode} have any prerequisites?`;
        button2text.textContent = `What can I learn from ${subjectCode}?`;
        button3text.textContent = `How many assessments does ${subjectCode} have?`;
    }
    else if (courseCode) {
        button1text.textContent = `Tell me what's the requirement for ${courseCode}?`;
        button2text.textContent = `What are the learning outcomes for ${courseCode}?`;
        button3text.textContent = `whats the course structure of ${courseCode}?`;
    }
    else {
        button1text.textContent = `What's the prerequisites for this subject?`;
        button2text.textContent = `Show me the structure for this course?`;
        button3text.textContent = `How many assessments does this subject have?`;
    }
}

function updateGreeting() {
    const greetingText = chatElementRef.shadowRoot.querySelector('#greetingText');
    const greetingText2 = chatElementRef.shadowRoot.querySelector('#greetingText2');
    greetingText.style.paddingLeft = '15px';
    greetingText2.style.paddingLeft = '15px';
    const now = new Date();
    const hour = now.getHours();
    let greeting = "";
    if (hour >= 5 && hour < 12) {
        greeting = "Good morning,";
    } else if (hour >= 12 && hour < 18) {
        greeting = "Good afternoon,";
    } else {
        greeting = "Good evening,";
    }
    greetingText.textContent = greeting;
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === 'UPDATE_GREETING') {
        updateGreeting();
        sendResponse({ received: true });
    }
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === 'UPDATE_BUTTON_TEXT_SUBJECT') {
        const subjectCode = message.subjectCode;
        updateButtonTexts(subjectCode, null);
        sendResponse({ received: true });
    }
    if (message.type === 'UPDATE_BUTTON_TEXT_COURSE') {
        const courseCode = message.courseCode;
        updateButtonTexts(null, courseCode);
        sendResponse({ received: true });
    }
    if (message.type === 'UPDATE_BUTTON_TEXT_SAMPLE') {
        updateButtonTexts(null, null);
        sendResponse({ received: true });
    }
    return true;
});
