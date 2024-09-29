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

chrome.webNavigation.onHistoryStateUpdated.addListener((details) => {
    chrome.tabs.get(details.tabId, (tab) => {
        const url = new URL(tab.url);
        const path = url.pathname.split('/');
        if (path[1] === 'subjects') {
            const subjectCode = path[2].toUpperCase();
            setTimeout(() => chrome.runtime.sendMessage({
                type: 'UPDATE_BUTTON_TEXT_SUBJECT',
                subjectCode: subjectCode
            }), 1001);
        }
        if (path[2] === 'subjects') {
            const subjectCode = path[3].toUpperCase();
            setTimeout(() => chrome.runtime.sendMessage({
                type: 'UPDATE_BUTTON_TEXT_SUBJECT',
                subjectCode: subjectCode
            }), 1001);
        }
        if (path[1] === 'courses') {
            const subjectCode = path[2].toUpperCase();
            setTimeout(() => chrome.runtime.sendMessage({
                type: 'UPDATE_BUTTON_TEXT_COURSE    ',
                subjectCode: subjectCode
            }), 1001);
        }
        if (path[2] === 'courses') {
            const courseCode = path[3].toUpperCase();
            setTimeout(() => chrome.runtime.sendMessage({
                type: 'UPDATE_BUTTON_TEXT_COURSE',
                courseCode: courseCode
            }), 1001);
        }
    });
});