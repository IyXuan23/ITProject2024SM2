const chatElement = document.getElementById("chat-element");

document.addEventListener('DOMContentLoaded', async(event) => {
    
    chatElement.requestInterceptor = async (requestDetails) => {
        const userQuery = requestDetails.body.messages[requestDetails.body.messages.length - 1].text;
        const encodedQuery = encodeURIComponent(userQuery);
        const newUrl = `https://api-test-gamma-nine.vercel.app/api/v0/generate_sql?question=${encodedQuery}`;
        chatElement.connect.url = newUrl;
        return requestDetails;
    };

    chatElement.responseInterceptor = (response) => {
        result = response.response;
        response = { text: result};
        return response;
    };

    chatElement.onMessage = (message) => {
        if (message.message.role === 'ai' && !message.isHistory) {
            chatElement.addMessage({
                html: `
                <div class="deep-chat-temporary-message">
                    <button class="deep-chat-button deep-chat-suggestion-button" id = "suggestion1" style="margin-top: 5px"></button>
                    <button class="deep-chat-button deep-chat-suggestion-button" id = "suggestion2" style="margin-top: 6px"></button>
                    <button class="deep-chat-button deep-chat-suggestion-button" id = "suggestion3" style="margin-top: 6px"></button>
                </div>`, 
                role: "user"
            });
            const suggestion1 = chatElementRef.shadowRoot.querySelector('#suggestion1')
            const suggestion2 = chatElementRef.shadowRoot.querySelector('#suggestion2')
            const suggestion3 = chatElementRef.shadowRoot.querySelector('#suggestion3')
            const suggestion = getRndSuggestion();
            suggestion1.textContent = suggestion[0]
            suggestion2.textContent = suggestion[1]
            suggestion3.textContent = suggestion[2]
            console.log(message.message.html);
        }
    };
});


function getRndSuggestion() {
    const suggestions = [
        "Tell me what's the prerequisite for this subject?",
        "What are the learning outcomes for this subject?",
        "How many assessments does this subject have?",
        "Who is the coordinator for this subject?",
        "What are the teaching times for this subject?",
        "When is the census date for this subject?",
    ]
    while (suggestions.length < 6) {
        var r = Math.floor(Math.random() * suggestions.length) + 1;
        if (arr.indexOf(r) === -1) arr.push(r);
    }
    return suggestions;
}

chatElementRef.htmlClassUtilities = {
    'custom-button': {
        events: {
            click: (event) => {
                const text = event.currentTarget.querySelector('.custom-button-text').innerText;
                chatElementRef.submitUserMessage({ text: text.substring(0, text.length) });
            },
        },
        styles: {
            default: {
                marginLeft: '10px',
                marginRight: '10px',
                backgroundColor: '#ffffff',
                borderRadius: '10px',
                padding: '10px',
                cursor: 'pointer',
                textAlign: 'center',
                marginTop: '10px',
                boxshadow: '0 0 0 5px rgba(0, 0, 0, 0.5)',
                border: '1px solid #969696'
            },
            hover: { backgroundColor: '#ebebeb', transform: 'scale(1.03)', transition: 'transform 0.3s ease' },
            click: { backgroundColor: '#e4e4e4', transform: 'scale(1.03)', transition: 'transform 0.3s ease' },
        },
    },
    'custom-button-text': {
        styles: {
            default: { pointerEvents: 'none' },
        },
    },
};