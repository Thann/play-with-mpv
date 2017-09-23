import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "play-with-mpv",
    version = "0.0.3",
    author = "Jonathan Knapp",
    author_email = "jaknapp8@gmail.com",
    description = "Chrome extension and python server that allows you to play videos in webpages with MPV instead.",
    license = "MIT",
    keywords = "mpv video play chrome extension",
    url = "http://github.com/thann/play-with-mpv",
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],

    py_modules=["server"],
    install_requires=['youtube-dl'],
    entry_points={
        # 'console_scripts': [
        'gui_scripts': [
            'play-with-mpv=server:start',
        ],
    },
    setup_requires=['install_freedesktop'],
    desktop_entries={
        'play-with-mpv': {
            'Name': 'Play With MPV (server)',
            # 'GenericName': 'play-with-mpv',
            'Categories': 'AudioVideo;Audio;Video;Player;TV',
            'Icon': 'mpv',
        },
    },
)
