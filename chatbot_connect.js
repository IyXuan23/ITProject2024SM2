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

    chatElement.onMessage = async (message) => {
        if (message.message.role === 'ai' && !message.isHistory) {
            chatElement.addMessage({
                html: `
                <div class="deep-chat-temporary-message" id = "suggestions-button" style="display: none">
                    <button class="deep-chat-button deep-chat-suggestion-button" id = "suggestion1" style="margin-top: 5px; boxShadow: '0px 0.3px 0.9px rgba(0, 0, 0, 0.12), 0px 1.6px 3.6px rgba(0, 0, 0, 0.16)'; borderRadius: 20px"></button>
                    <button class="deep-chat-button deep-chat-suggestion-button" id = "suggestion2" style="margin-top: 6px; boxShadow: '0px 0.3px 0.9px rgba(0, 0, 0, 0.12), 0px 1.6px 3.6px rgba(0, 0, 0, 0.16)'; borderRadius: 20px"></button>
                    <button class="deep-chat-button deep-chat-suggestion-button" id = "suggestion3" style="margin-top: 6px; boxShadow: '0px 0.3px 0.9px rgba(0, 0, 0, 0.12), 0px 1.6px 3.6px rgba(0, 0, 0, 0.16)'; borderRadius: 20px"></button>
                </div>`, 
                role: "user"
            });
            const suggestions = await fetchSimilarQuestions();
            console.log(suggestions);
            let j = 0;
            for (let i = 0; i < 3; i++) {
                if (suggestions[j] !== null) {
                    const button = chatElementRef.shadowRoot.querySelector(`#suggestion${i + 1}`);
                    button.textContent = suggestions[j];
                    j++;
                } else {
                    j++;
                }
            }
            const suggestionsButton = chatElementRef.shadowRoot.querySelector('#suggestions-button');
            suggestionsButton.style.display = "block";
        }
    };
});


async function fetchSimilarQuestions() {
    const userQuery = chatElement.getMessages()[chatElement.getMessages().length - 1].text;
    const encodedQuery = encodeURIComponent(userQuery);
    const url = `https://api-test-gamma-nine.vercel.app/api/v0/generate_popup_questions?question=${encodedQuery}`;
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Response status: ${response.status}`);
        }
        const json = await response.json();
        return json.questions;
    } catch (error) {
        console.error(error.message);
    }
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
                marginLeft: '15px',
                marginRight: '15px',
                backgroundColor: '#ffffff',
                borderRadius: '20px',
                padding: '8px',
                cursor: 'pointer',
                textAlign: 'center',
                marginTop: '12px',
                boxShadow: "0px 0.3px 0.9px rgba(0, 0, 0, 0.12), 0px 1.6px 3.6px rgba(0, 0, 0, 0.16)",
                animation: 'fadeIn 1s'
            },
            hover: { backgroundColor: '#ebebeb', transform: 'scale(1.015)', transition: 'transform 0.3s ease' },
            click: { backgroundColor: '#e4e4e4', transform: 'scale(1.015)', transition: 'transform 0.3s ease' },
        },
    },
    'custom-button-text': {
        styles: {
            default: { pointerEvents: 'none' },
        },
    },
};