const hoverball = document.createElement('img');
hoverball.id = 'unimelb-handbot-hoverball';
hoverball.src = chrome.runtime.getURL('Chatbot_logo_128.png');
document.body.appendChild(hoverball);

let sidePanelOpen = false;

hoverball.addEventListener('click', () => {
  if (sidePanelOpen) {
    chrome.runtime.sendMessage({ type: 'close_side_panel' });
  } else {
    chrome.runtime.sendMessage({ type: 'open_side_panel' });
  }
  sidePanelOpen = !sidePanelOpen;
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