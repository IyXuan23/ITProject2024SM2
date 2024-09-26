chrome.runtime.onMessage.addListener((message, sender) => {
    (async () => {
        if (message.type === 'open_side_panel') {
            await chrome.sidePanel.open({ tabId: sender.tab.id });
            await chrome.sidePanel.setOptions({
                tabId: sender.tab.id,
                path: 'sidepanel.html',
                enabled: true
            });
        } else if (message.type === 'close_side_panel') {
            await chrome.sidePanel.setOptions({
                tabId: sender.tab.id,
                enabled: false
            });
        }
    })();
});

const ORIGIN = 'https://handbook.unimelb.edu.au/search';

chrome.sidePanel
    .setPanelBehavior({ openPanelOnActionClick: true })
    .catch((error) => console.error(error));

chrome.tabs.onUpdated.addListener(async (tabId, info, tab) => {
    if (!tab.url) return;
    const url = new URL(tab.url);
    // Enables the side panel on handbook.unimelb.edu.au
    if (url.origin === ORIGIN) {
        await chrome.sidePanel.setOptions({
            tabId,
            path: 'sidepanel.html',
            enabled: true
        });
    } else {
        // Disables the side panel on all other sites
        await chrome.sidePanel.setOptions({
            tabId,
            enabled: false
        });
    }
});