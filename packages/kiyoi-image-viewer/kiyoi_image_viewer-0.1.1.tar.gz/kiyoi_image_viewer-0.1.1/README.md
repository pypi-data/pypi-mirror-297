# About

Kiyoi is a Python image viewer based on [Pyside6](https://wiki.qt.io/Qt_for_Python) (Qt) and [Pillow](https://python-pillow.org/) designed to easily display images with optimal use of screen real-estate. There is no superfluous UI wasting space or unnecessary features like image editing, only functionality necessary to optimally view images.

# Features

* Minimal UI, doesn't waste space
* Image scaling with many filters/algorithms (via Pillow)
* (Temporary) cropping of images within the viewer
* Animated file (gif/png/other) support
* File switching via keyboard

# Installation

## Windows

1. Ensure you have python installed.
1. Run `pip install kiyoi_image_viewer`.
1. To install menu entries and file associations, `run kiyoi_winreg_install` at the Window console (cmd) (or `python -m "kiyoi_winreg_install"`).
    * To uninstall these, run `kiyoi_winreg_uninstall` at the Window console (or `python -m "kiyoi_winreg_uninstall"`).
1. Default associations are not set automatically. If you want Kiyoi as a default for all images, Windows has an option in system settings under "default apps" to select a "photo viewer". Kiyoi is added to that list by kiyoi_winreg_install.

## Linux

### Unmanaged Python

If your distro allows you to install Python packages directly with pip:

1. Run `pip install kiyoi_image_viewer`.
2. Get the `kiyoi.desktop file` (either out of the kiyoi_image_viewer site-packages folder in Python or more easily, download it from this repo)
3. Run `desktop-file-install /PATH/TO/kiyoi.desktop` (using the real path to wherever that file is)

### Managed Python

TODO

# Use

Kiyoi does not appear in the start/launch menu because it is not intended to be opened without a file. To use Kiyoi, you'll have to change file associations to point to it. If you need to invoke it directly, you can use `kiyoi_image_viewer`, which will immediately ask for a file.

# Controls

* Left click drag: Move the window
* Double left click: Minimize
* Ctrl + left click, middle click, escape key: Close window
* Right click: Open context menu
* Scroll wheel: Scale image
* Alt + scroll wheel, period key: Original image scale
* Ctrl + scroll wheel backward: Scale to screen (fit to tightest dimension)
* Ctrl + scroll wheel forward: Scale to screen (fully fill, will exceed screen size unless the image is the same aspect ratio as screen)
* =, +: Increase scale
* -, \_: Decrease scale
* Shift + left click drag: Crop image
* Shift + left click, comma key, Z: Remove crop
* W, A, up arrow, left arrow: Previous image (based on file sort specified in options)
* S, D, down arrow, right arrow: Next image (based on file sort specified in options)
* Space: Stop/play animation (if present)
* [: Previous frame of animation
* ]: Next frame of animation

# TODO

## Known Issues

* Scaling and cropping causes momentary flicker.
* If a Kiyoi instance is started by another application (like a web browser opening an image externally), the window will pop-under the application that invoked it. This is because of how window managers try to prevent focus-stealing. The way I handle processes causes the window manager to lose track of the open operation, so it doesn't make the connection and pops it under instead of over. I'm not sure if this is fixable.
* File type is identified by extension (like Windows) but it should by mimetype/both. This means you could run into file type mismatches on Linux if you have files with the wrong extensions.
* There are several issues with how windows are positioned by Qt:
    * Snapping should be cross platform, not just Linux configured for it (at least for other Kiyoi windows).
    * Zooming and cropping sometimes don't reposition the window correctly, if it would have been partially off-screen.
* Windows can get lost off-screen due to scaling.
* If an image covers the entire screen on Windows, it can cause a strange flickering with the taskbar. It seems to be some special case in Windows for how it handles windows that cover the entire screen, and it doesn't work entirely correctly. It should stop in a second or two if you don't move or resize the window.
* Next/previous won't notice new files added to the folder since the image was opened, because the program stores the list of files.
* Changing files can cause the program to freeze. This is because the file list isn't complete. Just wait, it WILL eventually come back, but it may take a while if you have a lot of files in the active directory.

## Planned Features

* An installer for Windows, to avoid the need for console commands
* Implement cropping via dragging corners of the window/image
* Implement "show in file explorer" functionality (hard to do cross-platform)
* Implement a way to edit cropping without clearing it and reapplying it (showing original image + box that can be moved/resized)
* Configurable controls (at least to an extent)
* Add a context menu option to open a new image
* Add a way to open the next/previous image in a new window
* Windows should accept drag-and-drop (possibly with a context menu to open in the current or a new window)
* Better memory limiting logic
* Error popups
* Loading spinners (Qt doesn't make this easy)
* Better animation controls and info, such as playback speed, playing backwards, going to specific frames, overriding file encoded frame times (sometimes they are wrong), and showing frame number
* Viewing/setting scale via context menu

# Troubleshooting

If any of these solutions fail, let me know.

## Opening an image opens two (or more) Kiyoi windows

This is because more than one master instance of Kiyoi is running. The way Kiyoi works is that one master instance responds to requests for images from newly opened instances. If somehow more than one of these is running, each one will open a window, leading to duplicates.

To fix this, close all Kiyoi windows. If that fails, kill all Kiyoi processes.

## Tooltips flicker

This seems to be a problem with Plasma/KDE (on Linux/BSD) and also affects other programs when using that system UI. To fix it, open KDE/Plasma's System Settings and go to Window Management -> Desktop Effects, and under the "Appearance" heading, disable Morphic Popups, then apply. You will have to restart the affected program(s) and possibly your computer.

## Changing images is slow

There are two possible causes for this. The most likely is that the image is simply large. Kiyoi has to open the image and then reprocess it before displaying it, so a very large image will take time to load. Alternatively, if changing image for the first time (next/previous image) is slow, the listing and sorting of files in that directory may be the problem, likely caused by an excessive number of files in the directory. Either of these can be caused by a slow drive and don't really have a solution beyond using a faster drive.

# Feedback

Either open an issue or send me an email at <williamkappler@gmail.com> with any bug reports (not already mentioned above) or suggestions. Please be aware this is a new project and the first time I've released an end-user application, so there may be some rough spots.

# Translation

Other than English, all existing translations are based on Google/Bing Translate or my minimal knowledge of the given language. If you would like to improve a translation or contribute a new one, please let me know.

Kiyoi uses a simple system of string replacement for translation. locales/lang.template contains the strings to be translated for a given language. Languages should be named with single or double part language codes, such as en.lang or en_US.lang. These should use valid ISO 639-1 codes for the language if they exist. Dialect language files will be preferred if they exist and match the user's locale. For instance, if en.lang and en_US.lang exist, US users will get en_US.lang while UK users will get en.lang.

Language synonyms also map dialects to other similar dialects, should it be useful to be more specific than falling back to the root language code. For instance, en_JP is a synonym of en_US, so Japanese English users will receive US English instead of the otherwise-chosen en (UK English).
