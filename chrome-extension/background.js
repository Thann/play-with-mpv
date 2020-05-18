
// Show on all pages
chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
	chrome.pageAction.show(tabId);
});

// Send current tabs url to MPV server
chrome.pageAction.onClicked.addListener(function(tab){
	// console.info("Clicked!", tab.url)
	playUrl(tab.url, true);
});

function playUrl(url, pause) {
	chrome.storage.sync.get({
		server_url: null,
		maxheight: null,
		mpv_args: null,
	}, function(opts) {
		if (!opts.server_url)
			opts.server_url = 'http://localhost:7531';
		if (opts.mpv_args) {
			opts.mpv_args = opts.mpv_args.split(/\n/);
		} else {
			opts.mpv_args = [];
		}
		if (opts.maxheight) {
			opts.mpv_args.splice(0, 0,
			`--ytdl-format=bestvideo[height<=?${opts.maxheight}]+bestaudio/best`);
		}
		const query = (`?play_url=` + encodeURIComponent(url) + [''].concat(
			opts.mpv_args.map(encodeURIComponent)).join('&mpv_args='));

		const xhr = new XMLHttpRequest();
		xhr.onreadystatechange = handleXHR;
		xhr.open("GET", `${opts.server_url}/${query}`, true);
		xhr.send();

		// Pause videos in tab
		pause && chrome.tabs.executeScript({code: `
			for (const v of document.getElementsByTagName('video')) {
				v.pause();
			}`
		});
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

	playUrl(info["linkUrl"] || info["srcUrl"]|| info["pageUrl"], true);
});

chrome.commands.onCommand.addListener(function(command) {
	chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
		playUrl(tabs[0].url, true);
	});
});
