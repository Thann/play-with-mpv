// Saves options to chrome.storage

function save_options() {
    const server_url = document.getElementById('server_url').value || null;
    const ytdl_args = document.getElementById('ytdl_args').value || null;
    const location = document.getElementById('location').value || null;
    chrome.storage.sync.set({
        server_url, ytdl_args, location
    }, function() {
        // Update status to let user know options were saved.
        const status = document.getElementById('status');
        status.textContent = 'Options saved.';
        setTimeout(function() {
            status.textContent = '';
        }, 1000);
    });
}

// Restores select box and checkbox state using the preferences
// stored in chrome.storage.
function restore_options() {
    chrome.storage.sync.get({
        server_url: null,
        ytdl_args: null,
        location: null,
    }, function(opts) {
        document.getElementById('server_url').value = opts.server_url;
        document.getElementById('ytdl_args').value = opts.ytdl_args;
        document.getElementById('location').value = opts.location || '';

        // TODO: chrome seems to block this.
        // Check server connectivity
        // const xhr = new XMLHttpRequest();
        // xhr.onreadystatechange = function(e) {
        //   document.getElementById('server_status').textContent = (
        //     e.currentTarget.status?
        //     'Connected!':
        //     'Disconected!')
        // };
        // xhr.open("GET", opts.server_url, true);
        // xhr.send();
    });
}

document.addEventListener('DOMContentLoaded', restore_options);
document.getElementById('save').addEventListener('click', save_options);
