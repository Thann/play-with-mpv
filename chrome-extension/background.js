
// Show on all pages
chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
    chrome.pageAction.show(tabId);
});

function HandleContex(info, tab){
  if(typeof info.linkUrl !== 'undefined'){
    sendurl(info.linkUrl);
  }else {
    sendurl(tab.url);
  }
}

//Adding context menu item
chrome.runtime.onInstalled.addListener(function() {
var contexts = ["link"]
chrome.contextMenus.create({"title": "Play In MPV", "id":"plaympvlink", "contexts":contexts});
});
// adding listener for contex Click
chrome.contextMenus.onClicked.addListener(HandleContex);

// Send current tabs url to MPV server
chrome.pageAction.onClicked.addListener(HandleContex);

function sendurl(url){
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = handleXHR;
  xhr.open("GET", "http://localhost:7531/?play_url="+url, true);
  xhr.send();
}

function handleXHR() {
  // console.log("XHR", arguments)
}
