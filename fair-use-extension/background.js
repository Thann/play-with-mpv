
// Show on all pages
chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
	chrome.pageAction.show(tabId);
});

// Send current tabs url to MPV server
chrome.pageAction.onClicked.addListener(function(tab){
	// console.info("Clicked!", tab.url)
	fairuseUrl(tab.url, true);
});

function fairuseUrl(url, pause) {
	chrome.storage.sync.get({
		server_url: null,
		ytdl_args: null,
		location: null,
	}, function(opts) {
		if (!opts.server_url)
			opts.server_url = 'http://localhost:7531';
		if (opts.ytdl_args) {
			opts.ytdl_args = opts.ytdl_args.split(/\n/);
		} else {
			opts.ytdl_args = [];
		}
		const params = {
			fairuse_url: url,
			location: opts.location,
			ytdl_args: opts.ytdl_args,
		}
		// build query-string
		const query = Object.entries(params)
			.map(([k,v]) => {
				k = encodeURIComponent(k);
				if ([null, undefined].includes(v)) {
					v = '';
				} else if (v.map) { // arrays
					v = v.map(encodeURIComponent).join(`&${k}=`);
				} else {
					v = encodeURIComponent(v)	;
				}
				return `${k}=${v}`;
			})
			.join('&');
		const xhr = new XMLHttpRequest();
		xhr.onreadystatechange = handleXHR;
		xhr.open("GET", `${opts.server_url}/?${query}`, true);
		xhr.send();
	});
}

function handleXHR() {
	// console.log("XHR", arguments)
}

var parent = chrome.contextMenus.create({
	"id": "thann.fair-use-download",
	"title": "Download video for Fair Use",
	"contexts": ["page", "link", "video", "audio"]
});

chrome.contextMenus.onClicked.addListener(function(info, tab) {
	// console.log("item " + info.menuItemId + " was clicked");
	// console.log("info: " + JSON.stringify(info));
	// console.log("tab: " + JSON.stringify(tab));

	fairuseUrl(info["linkUrl"] || info["srcUrl"]|| info["pageUrl"], true);
});

chrome.commands.onCommand.addListener(function(command) {
	chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
		fairuseUrl(tabs[0].url, true);
	});
});
