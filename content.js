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
    closeButton.style.transform = 'scale(1.1)';
  });

  closeButton.addEventListener('mouseout', () => {
    closeButton.style.color = '#666';
    closeButton.style.transform = 'scale(1)';
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

async function loadChatInterface() {
  try {
    const response = await fetch(chrome.runtime.getURL('test_popup.html'));
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.text();
    chatContainer.innerHTML = data;
    console.log('Chat interface HTML loaded successfully');
    
    chatContainer.style.width = '400px';
    chatContainer.style.height = '600px';
    chatContainer.style.display = 'flex';
    chatContainer.style.flexDirection = 'column';
    
    const closeButton = createCloseButton();
    chatContainer.appendChild(closeButton);
    
    chatContainer.offsetHeight;
    
    const deepChatScript = document.createElement('script');
    deepChatScript.src = chrome.runtime.getURL('deepChat.bundle.js');
    await new Promise((resolve, reject) => {
      deepChatScript.onload = () => {
        console.log('DeepChat script loaded');
        if (typeof DeepChat !== 'undefined') {
          console.log('DeepChat is defined after script load');
        } else {
          console.error('DeepChat is still undefined after script load');
        }
        resolve();
      };
      deepChatScript.onerror = (error) => {
        console.error('Error loading DeepChat script:', error);
        reject(error);
      };
      document.head.appendChild(deepChatScript);
    });

    const scripts = Array.from(chatContainer.getElementsByTagName('script'));
    for (let i = 0; i < scripts.length; i++) {
      const script = scripts[i];
      const newScript = document.createElement('script');
      if (script.src) {
        newScript.src = chrome.runtime.getURL(script.src.split('/').pop());
      } else {
        newScript.textContent = script.textContent;
      }
      await new Promise((resolve, reject) => {
        newScript.onload = () => {
          console.log(`Script ${i + 1}/${scripts.length} loaded:`, newScript.src || 'inline script');
          resolve();
        };
        newScript.onerror = (error) => {
          console.error(`Error loading script ${i + 1}/${scripts.length}:`, error);
          reject(error);
        };
        document.body.appendChild(newScript);
      });
    }
    
    console.log('All scripts loaded, initializing chat');
    initializeChat();
  } catch (error) {
    console.error('Error loading chat interface:', error);
    chatContainer.innerHTML = '<p>Error loading chat interface</p>';
  }
}

function initializeChat() {
  console.log('Initializing chat');
  const chatElement = chatContainer.querySelector('deep-chat');
  if (chatElement) {
    console.log('Chat element found:', chatElement);
    console.log('Chat element dimensions:', chatElement.offsetWidth, chatElement.offsetHeight);
    console.log('Chat element attributes:', Array.from(chatElement.attributes).map(attr => `${attr.name}="${attr.value}"`).join(', '));
    
    console.log('DeepChat defined in initializeChat:', typeof DeepChat !== 'undefined');
    
    if (typeof DeepChat !== 'undefined') {
      try {
        new DeepChat({
          container: chatElement,
          demo: true
        });
        console.log('Deep chat manually initialized');
      } catch (error) {
        console.error('Error initializing DeepChat:', error);
      }
    } else {
      console.error('DeepChat is not defined. Current global objects:', Object.keys(window));
      const deepChatScript = document.createElement('script');
      deepChatScript.src = chrome.runtime.getURL('deepChat.bundle.js');
      deepChatScript.onload = () => {
        console.log('DeepChat script reloaded');
        if (typeof DeepChat !== 'undefined') {
          console.log('DeepChat is defined after script reload');
          new DeepChat({
            container: chatElement,
            demo: true
          });
        } else {
          console.error('DeepChat is still undefined after script reload');
        }
      };
      document.head.appendChild(deepChatScript);
    }
    
    console.log('Chat element initialization attempt completed');
  } else {
    console.error('Chat element not found');
  }
}

hoverball.addEventListener('click', () => {
  if (chatContainer.style.display === 'none') {
    chatContainer.style.display = 'flex';
    chatContainer.style.flexDirection = 'column';
    setTimeout(() => {
      chatContainer.style.transform = 'translateY(0)';
      chatContainer.style.opacity = '1';
      console.log('Chat container should now be visible');
      initializeChat();
    }, 300);
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

hoverball.style.width = '60px';
hoverball.style.height = '60px';
hoverball.style.cursor = 'pointer';

hoverball.style.position = 'fixed';
hoverball.style.right = '20px';
hoverball.style.bottom = '20px';
hoverball.style.zIndex = '1000';
hoverball.style.boxShadow = '0 2px 10px rgba(0,0,0,0.2)';
hoverball.style.borderRadius = '50%';
hoverball.style.transition = 'transform 0.3s ease';

hoverball.addEventListener('mouseover', () => {
  hoverball.style.transform = 'scale(1.1)';
});

hoverball.addEventListener('mouseout', () => {
  hoverball.style.transform = 'scale(1)';
});

chatContainer.style.position = 'fixed';
chatContainer.style.right = '20px';
chatContainer.style.bottom = '90px';
chatContainer.style.width = '500px';
chatContainer.style.height = '600px';
chatContainer.style.backgroundColor = 'white';
chatContainer.style.zIndex = '1002';
chatContainer.style.boxShadow = '0 0 10px rgba(0,0,0,0.1)';
chatContainer.style.borderRadius = '10px';
chatContainer.style.overflow = 'hidden';
chatContainer.style.transition = 'all 0.3s ease-out';
chatContainer.style.transform = 'translateY(20px)'; 
chatContainer.style.opacity = '0';