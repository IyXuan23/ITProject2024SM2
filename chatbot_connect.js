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
                    <button class="deep-chat-button deep-chat-suggestion-button" id = "suggestion1" style="margin-top: 5px"></button>
                    <button class="deep-chat-button deep-chat-suggestion-button" id = "suggestion2" style="margin-top: 6px"></button>
                    <button class="deep-chat-button deep-chat-suggestion-button" id = "suggestion3" style="margin-top: 6px"></button>
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

    const url = `https://api-test-gamma-nine.vercel.app/api/v0/generate_questions`;
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