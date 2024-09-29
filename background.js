chrome.runtime.onMessage.addListener((message, sender) => {
    (async () => {
        if (message.type === 'open_side_panel') {
            await chrome.sidePanel.open({ tabId: sender.tab.id });
            await chrome.sidePanel.setOptions({
                tabId: sender.tab.id,
                path: 'sidepanel.html',
                enabled: true
            });
        }
    })();
});

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    const url = new URL(tab.url);
    const path = url.pathname.split('/');
    if (path[1] === 'subjects' && path[2]) {
        const subjectCode = path[2].toUpperCase();
        console.log("sending message");
        setTimeout(() => chrome.runtime.sendMessage({
            type: 'UPDATE_BUTTON_TEXT',
            subjectCode: subjectCode
        }), 1001);
    }
});