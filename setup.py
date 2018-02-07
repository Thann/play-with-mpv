import os
from setuptools import setup, find_packages

description = "Chrome extension and python server that allows you to play videos in webpages with MPV instead."

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "play-with-mpv",
    version = "0.0.6",
    author = "Jonathan Knapp",
    author_email = "jaknapp8@gmail.com",
    description = description,
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
        'gui_scripts': [
            'play-with-mpv=server:start',
        ],
    },
    setup_requires=['install_freedesktop>=0.2.0'],
    dependency_links=[
        "git+ssh://git@github.com/thann/install_freedesktop.git@master#egg=install_freedesktop-0.2.0"
    ],
    desktop_entries={
        'play-with-mpv': {
            'filename': 'thann.play-with-mpv',
            'Name': 'Play With MPV (server)',
            'Categories': 'AudioVideo;Audio;Video;Player;TV',
            'Comment': description,
            'Icon': 'mpv',
        },
    },
)
