
// Show on all pages
chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
    chrome.pageAction.show(tabId);
});

// Send current tabs url to MPV server
chrome.pageAction.onClicked.addListener(function(tab){
    // console.info("Clicked!", tab.url)
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = handleXHR;
    xhr.open("GET", "http://localhost:7531/?play_url="+tab.url, true);
    xhr.send();
});

function handleXHR() {
  // console.log("XHR", arguments)
}
