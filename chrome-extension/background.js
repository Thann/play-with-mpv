
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
	// Pause videos in tab
	chrome.tabs.executeScript({
		code: `
			for (const v of document.getElementsByTagName('video')) {
				v.pause();
			}`
	});
}

function handleXHR() {
	// console.log("XHR", arguments)
}

var parent = chrome.contextMenus.create({
	"id": "thann.play-with-mpv",
	"title": "Play with MPV",
	"contexts": ["page", "link", "video", "audio"]
});

chrome.contextMenus.onClicked.addListener(function(info, tab) {
	// console.log("item " + info.menuItemId + " was clicked");
	// console.log("info: " + JSON.stringify(info));
	// console.log("tab: " + JSON.stringify(tab));

	playUrl(info["linkUrl"] || info["srcUrl"]|| info["pageUrl"]);
});

chrome.commands.onCommand.addListener(function(command) {
	chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
		playUrl(tabs[0].url);
	});
});
