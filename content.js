const hoverball = document.createElement('img');
hoverball.id = 'unimelb-handbot-hoverball';
hoverball.src = chrome.runtime.getURL('Chatbot_logo_128.png');
document.body.appendChild(hoverball);

const chatContainer = document.createElement('div');
chatContainer.id = 'unimelb-handbot-chat-container';
chatContainer.style.display = 'none';
document.body.appendChild(chatContainer);

function createCloseButton() {
  const closeButton = document.createElement('div');
  closeButton.id = 'unimelb-handbot-close-button';
  closeButton.innerHTML = '&times;';
  closeButton.style.position = 'absolute';
  closeButton.style.top = '5px';
  closeButton.style.right = '15px';
  closeButton.style.fontSize = '25px';
  closeButton.style.cursor = 'pointer';
  closeButton.style.color = '#666';
  closeButton.style.zIndex = '1001';

  closeButton.addEventListener('mouseover', () => {
    closeButton.style.color = '#000';
  });

  closeButton.addEventListener('mouseout', () => {
    closeButton.style.color = '#666';
  });

  closeButton.addEventListener('click', () => {
    chatContainer.style.transform = 'translateY(20px)'; 
    chatContainer.style.opacity = '0';
    setTimeout(() => {
      chatContainer.style.display = 'none';
    }, 300);
    console.log('Chat interface closed');
  });

  return closeButton;
}

function loadChatInterface() {
  fetch(chrome.runtime.getURL('test_popup.html'))
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.text();
    })
    .then(data => {
      chatContainer.innerHTML = data;
      console.log('Chat interface HTML loaded successfully');
      
      const closeButton = createCloseButton();
      chatContainer.appendChild(closeButton);
      
      const scripts = Array.from(chatContainer.getElementsByTagName('script'));
      scripts.forEach((script, index) => {
        const newScript = document.createElement('script');
        if (script.src) {
          newScript.src = chrome.runtime.getURL(script.src.split('/').pop());
        } else {
          newScript.textContent = script.textContent;
        }
        newScript.onload = () => {
          console.log(`Script ${index + 1}/${scripts.length} loaded`);
          if (script === scripts[scripts.length - 1]) {
            initializeChat();
          }
        };
        newScript.onerror = (error) => {
          console.error(`Error loading script ${index + 1}/${scripts.length}:`, error);
        };
        document.body.appendChild(newScript);
      });
    })
    .catch(error => {
      console.error('Error loading chat interface:', error);
      chatContainer.innerHTML = '<p>加载聊天界面时出错。请刷新页面后重试。</p>';
    });
}

function initializeChat() {
  console.log('Initializing chat');
  const chatElement = chatContainer.querySelector('deep-chat');
  if (chatElement) {
    chatElement.style.width = '100%';
    chatElement.style.height = '100%';
    chatElement.demo = true;
    console.log('Chat element initialized');
  } else {
    console.error('Chat element not found');
  }
}

hoverball.addEventListener('click', () => {
  if (chatContainer.style.display === 'none') {
    chatContainer.style.display = 'block';
    setTimeout(() => {
      chatContainer.style.transform = 'translateY(0)';
      chatContainer.style.opacity = '1';
    }, 10);
    if (chatContainer.innerHTML === '') {
      console.log('Loading chat interface');
      loadChatInterface();
    } else {
      console.log('Chat interface already loaded');
    }
  } else {
    chatContainer.style.transform = 'translateY(20px)';
    chatContainer.style.opacity = '0';
    setTimeout(() => {
      chatContainer.style.display = 'none';
    }, 300);
    console.log('Chat interface hidden');
  }
});

hoverball.style.width = '48px';
hoverball.style.height = '48px';
hoverball.style.cursor = 'pointer';

hoverball.style.position = 'fixed';
hoverball.style.right = '20px';
hoverball.style.bottom = '20px';
hoverball.style.zIndex = '1000';
hoverball.style.boxShadow = '0 2px 10px rgba(0,0,0,0.2)';
hoverball.style.borderRadius = '50%';
hoverball.style.transition = 'transform 0.3s ease';

hoverball.addEventListener('mouseover', () => {
  hoverball.style.transform = 'scale(1.3)';
});

hoverball.addEventListener('mouseout', () => {
  hoverball.style.transform = 'scale(1)';
});


chatContainer.style.position = 'fixed';
chatContainer.style.right = '20px';
chatContainer.style.bottom = '80px';
chatContainer.style.width = '400px';
chatContainer.style.height = '600px';
chatContainer.style.backgroundColor = 'white';
chatContainer.style.zIndex = '1000';
chatContainer.style.boxShadow = '0 0 10px rgba(0,0,0,0.1)';
chatContainer.style.borderRadius = '10px';
chatContainer.style.overflow = 'hidden';
chatContainer.style.transition = 'all 0.3s ease-out';
chatContainer.style.transform = 'translateY(20px)'; 
chatContainer.style.opacity = '0';