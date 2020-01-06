#!/usr/bin/env python
import os
from setuptools import setup, find_packages

description = "Chrome extension and python server that allows you to play videos in webpages with MPV instead."

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def get_version():
    from subprocess import Popen, PIPE
    try:
        from subprocess import DEVNULL # py3
    except ImportError:
        import os
        DEVNULL = open(os.devnull, 'wb')

    def run(*cmd):
        return (Popen(cmd, stderr=DEVNULL, stdout=PIPE)
                .communicate()[0].decode('utf8').strip())

    return(run('git', 'describe', '--tags').replace('-','.post',1).replace('-','+',1)
        or '0.0.0.post{}+g{}'.format(
            run('git', 'rev-list', '--count', 'HEAD'),
            run('git', 'rev-parse', '--short', 'HEAD')))

setup(
    name = "play-with-mpv",
    version = get_version(),
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

    py_modules=["play_with_mpv"],
    install_requires=['wheel', 'youtube-dl'],
    entry_points={
        'gui_scripts': [
            'play-with-mpv=play_with_mpv:start',
        ],
    },
    setup_requires=['wheel', 'install_freedesktop>=0.2.0'],
    dependency_links=[
        "https://github.com/thann/install_freedesktop/tarball/master#egg=install_freedesktop-0.2.0"
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
