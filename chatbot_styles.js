const elementRef = document.getElementById("chat-element");

elementRef.htmlClassUtilities = {
  ['custom-button']: {
    events: {
      click: (event) => {
        const text = event.target.children[0].innerText;
        elementRef.submitUserMessage({ text: text.substring(1, text.length - 1) });
      },
    },
    styles: {
      default: { backgroundColor: '#ffffff', borderRadius: '10px', padding: '10px', cursor: 'pointer', textAlign: 'center' },
      hover: { backgroundColor: '#ebebeb' },
      click: { backgroundColor: '#e4e4e4' },
    },
  },
  ['custom-button-text']: { styles: { default: { pointerEvents: 'none' } } },
};