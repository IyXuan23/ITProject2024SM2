const chatElement = document.getElementById("chat-element");

document.addEventListener('DOMContentLoaded', (event) => {
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