# Play with MPV
Chrome extension and python server that allows you to play videos in webpages with MPV instead.

## Installation
1. Install [MPV](https://mpv.io/installation/)
2. Install [python 2 or 3](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/installing/)
3. Install [chrome extension](https://chrome.google.com/webstore/detail/play-with-mpv/hahklcmnfgffdlchjigehabfbiigleji)
4. Run `pip install git+git://github.com/thann/play-with-mpv --user`
5. Start server by running `play-with-mpv` (or use the Linux _free desktop_ shortcut)

(optional) Install [peerflix](https://github.com/mafintosh/peerflix) to stream torrents

## Usage
Navigate to a youtube video, then click the extension (or right-click a link). MPV should popup and start playing the video.

![screenshot](https://github.com/thann/play-with-mpv/raw/master/screenshot.png)

## Protips
Configure MPV to have no border, stay on top, and start in the corner: edit `~/.config/mpv/mpv.conf`
```
ontop=yes
border=no
window-scale=0.4
geometry=100%:100%
```

Inorder to resize the window without borders: edit `~/.config/mpv/input.conf`
```
` cycle border
ALT+UP add window-scale 0.05
ALT+DOWN add window-scale -0.05
```

