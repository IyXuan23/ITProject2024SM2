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
        response = {text: result};
        return response;
    };
});

chatElement.validateInput = (text) => {
    return text.length > 0;
};

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
                boxshadow: '0 0 0 5px rgba(0, 0, 0, 0.5)'
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