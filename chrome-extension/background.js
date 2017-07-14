
// Show on all pages
chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
    chrome.pageAction.show(tabId);
});

// Send current tabs url to MPV server
chrome.pageAction.onClicked.addListener(function(tab){
    // console.info("Clicked!", tab.url)
    playUrl(tab.url);
});

function playUrl(url) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = handleXHR;
    xhr.open("GET", "http://localhost:7531/?play_url="+url, true);
    xhr.send();
}

function handleXHR() {
  // console.log("XHR", arguments)
}

var parent = chrome.contextMenus.create({
	"id": "1",
	"title": "Play with MPV",
	"contexts": ["page", "link", "video", "audio"]
});

chrome.contextMenus.onClicked.addListener(function(info, tab) {
	// console.log("item " + info.menuItemId + " was clicked");
	// console.log("info: " + JSON.stringify(info));
	// console.log("tab: " + JSON.stringify(tab));

	playUrl(info["linkUrl"] || info["srcUrl"]|| info["pageUrl"]);
});