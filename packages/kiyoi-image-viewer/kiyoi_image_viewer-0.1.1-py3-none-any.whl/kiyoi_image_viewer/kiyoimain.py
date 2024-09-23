#!/usr/bin/python3

# Copyright (c) 2024 William Kappler
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
# OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.

# Note: This script may be launched directly, but is intended to be launched by
# the "kiyoi" shell script, because launching this directly will undesirably
# block the console that ends up running the master instance. The launcher
# makes sure the script releases the console. However, direct launching is
# necessary for development/debugging.

import argparse
import atexit
from collections import OrderedDict
from enum import Enum
import errno
from functools import cmp_to_key, partial
import json
import locale
import math
import os
import random
import sys
import tempfile
from threading import Thread
from time import sleep
import uuid
import warnings

import pyperclip

# These must come BEFORE PIL. PIL will change its loaded modules depending on if
# it detects PySide or not.
from PySide6.QtCore import Qt, QRect, QSize, QPoint, QSettings, QTimer, QStandardPaths, SIGNAL
from PySide6.QtGui import QPixmap, QAction, QActionGroup, QIcon
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QRubberBand, QMenu, QDialog, QVBoxLayout, QDialogButtonBox, QFileDialog, QSizePolicy

from PIL import UnidentifiedImageError as PillowUnidentifiedImageError
from PIL import Image as PillowImage
from PIL import ImageQt as PillowImageQt

from .kiyoiconstants import *

SCRIPT_PATH = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

# Developer-only: invokes recording of language strings to a file.
LANGUAGE_RECORD = False

PER_IMAGE_SCALE_MEMORY_LIMIT_MB = 1024 # 1 gb, only applies to upscaling (native size and downscaling is always allowed)

INTERPROCESS_COMMUNICATION_DIRECTORY = PROGRAM_NAME.lower() + "_com"
MAIN_INSTANCE_LOCK_FILE = PROGRAM_NAME.lower() +  ".lock"
MAIN_INSTANCE_REQUEST_FILE_PREFIX = PROGRAM_NAME.lower() +  "_"
MAIN_INSTANCE_REQUEST_FILE_SUFFIX = ".req"
MAIN_INSTANCE_REQUEST_TIMEOUT_MIN_MSEC = 1000.0
MAIN_INSTANCE_REQUEST_TIMEOUT_RANDOM_MSEC = 2000.0 # Used to try to prevent stepping on new processes
INTERPROCESS_INTERVAL_MSEC = 50

SETTINGS_FILE = "settings.ini"
LANGUAGE_DIRECTORY = os.path.join(SCRIPT_PATH, "locales")
LANGUAGE_SYNONYMS_DIRECTORY = os.path.join(LANGUAGE_DIRECTORY, "synonyms")
LANGUAGE_FILE_SUFFIX = ".lang"
LANGUAGE_SYNONYM_FILE_SUFFIX = ".syn"
LANGUAGE_NAME_STRING = "LANGUAGE_FULL_NAME"
LANGUAGE_FALLBACK_CODE = "en"

RESOURCE_DIRECTORY = os.path.join(SCRIPT_PATH, "resources")

BROWSER_FILTER = "Supported Images ({})".format(' '.join(['*.'+s for s in SUPPORTED_EXTENSIONS_NO_DOT]))

def clamp(x, l, h):
    return max(l, min(h, x))

SCALE_LIST_ADAPTIVE = [1+1/10*clamp(x, -9, 10)+1/5*clamp(x-10,0,10)+1/4*clamp(x-20,0,8)+1/3*clamp(x-28,0,6)+1/2*clamp(x-34,0,4)+clamp(x-38,0,6) for x in range(-9, 45)]
SCALE_LIST_EXPONENTIAL = [2**(0.25*x) for x in range(-16,17)]
SCALE_LIST_TEN_PERCENT = [1 + 0.1 * x for x in range(-9,51)]

SCALE_FILTERS = {
    PillowImage.Resampling.NEAREST.name: PillowImage.Resampling.NEAREST,
    PillowImage.Resampling.BOX.name: PillowImage.Resampling.BOX,
    PillowImage.Resampling.BILINEAR.name: PillowImage.Resampling.BILINEAR,
    PillowImage.Resampling.HAMMING.name: PillowImage.Resampling.HAMMING,
    PillowImage.Resampling.BICUBIC.name: PillowImage.Resampling.BICUBIC,
    PillowImage.Resampling.LANCZOS.name: PillowImage.Resampling.LANCZOS
}

SCALE_LEVEL_LISTS = {
    "ADAPTIVE": SCALE_LIST_ADAPTIVE,
    "EXPONENTIAL": SCALE_LIST_EXPONENTIAL,
    "TEN_PERCENT": SCALE_LIST_TEN_PERCENT
}

WHEEL_DELTA_PER_STEP = 120 # Per Qt docs

MINIMUM_CROPPED_SIZE = 5

WARNING_MESSAGE_INTERVAL_MSEC = 10000 # 10 seconds

# Note this is only raised on applyScale(), not if an existing scale is reset on image change.
# However, a UI message is generated in both cases. This is mostly used to prevent multiple
# scale steps from all being blocked if a smaller number of them could be applied successfully.
class ImageMemoryException(Exception):
    pass


def replaceText(language, string, record=None):
    if record is not None:
        record[string] = ""

    if language and string in language:
        return language[string]
    else:
        return string

def replaceTextAnnotateDifference(string):
    conf_string = _(string)
    sys_string = _sys(string)

    if conf_string != sys_string:
        return "{} ({})".format(conf_string, sys_string)
    else:
        return conf_string

_diff = replaceTextAnnotateDifference


# This is basically a very specialized form of error logger, just to propagate an
# error message created during image processing.
class ImageErrorReporter():
    listeners = []

    # The listener must be a function that takes a string argument.
    @classmethod
    def addListenerFxn(cls, fxn):
        cls.listeners.append(fxn)

    @classmethod
    def reportError(cls, message):
        for fxn in cls.listeners:
            fxn(message)


def getInterprocessCommunicationDir():
    return os.path.join(tempfile.gettempdir(), INTERPROCESS_COMMUNICATION_DIRECTORY, os.getlogin(), '')

def getLockFilePath():
    return os.path.join(getInterprocessCommunicationDir(), MAIN_INSTANCE_LOCK_FILE)


class FileSortType(Enum):
    ALPHABETICAL_ASC = 1
    ALPHABETICAL_DSC = 2
    MODIFIED_ASC = 3
    MODIFIED_DSC = 4
    CREATED_ASC = 5
    CREATED_DSC = 6


class ListRounding(Enum):
    EITHER = 1 # Round to closest value
    PREFER_UP = 2 # Round up to closest value, or down if none exists
    PREFER_DOWN = 3 # Round down to closest value, or up if none exists


def closestInList(items, value, rounding):
    if rounding is ListRounding.EITHER:
        return min(enumerate(items), key=lambda x: abs(x[1] - value))[0]
    else:
        # Either list may end up empty because of the condition here.
        # The condition is necessary to prevent "bleedover" of the
        # wrong direction in the form of negative distances;
        # since we find the closest by using the min distance,
        # negative distances would be a problem.
        uplist   = [(i,(x - value)) for i,x in enumerate(items) if (x - value) >= 0]
        downlist = [(i,(value - x)) for i,x in enumerate(items) if (value - x) >= 0]

        if not uplist and not downlist:
            raise ValueError("Invalid list")

        # If there are no items in the preferred direction, fall back to
        # the other direction.
        if rounding is ListRounding.PREFER_UP or not downlist:
            searchlist = uplist
        elif rounding is ListRounding.PREFER_DOWN or not uplist:
            searchlist = downlist

        # [0] is the original value, [1] is the distance from the search value.
        return min(searchlist, key=lambda x: x[1])[0]


# Simple Qt dialog that only displays a single message.
class BasicDialog(QDialog):
    def __init__(self, parent, title, message):
        super().__init__(parent)

        self.setWindowTitle(title)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(self.accept)

        label = QLabel(message)
        label.setOpenExternalLinks(True)

        self.layout = QVBoxLayout()
        self.layout.addWidget(label)
        self.layout.addWidget(self.buttonBox)

        self.setLayout(self.layout)

# Another simple dialog that performs an action on approval. Modal.
class ActionDialog(QDialog):
    def __init__(self, parent, conf_fxn, question, approve_capt, deny_capt, title):
        super().__init__(parent)

        self.setWindowTitle(title)

        self.buttonBox = QDialogButtonBox()

        self.buttonBox.addButton(approve_capt, QDialogButtonBox.AcceptRole)
        self.buttonBox.addButton(deny_capt, QDialogButtonBox.RejectRole)

        self.buttonBox.accepted.connect(conf_fxn)
        self.buttonBox.rejected.connect(self.close)

        label = QLabel(question)

        self.layout = QVBoxLayout()
        self.layout.addWidget(label)
        self.layout.addWidget(self.buttonBox)

        self.setLayout(self.layout)

        self.setModal(True)


# This is used as the base class for image processing layers that
# convert a Pillow image into a seemlessly animated image.
# * FileImageLayer (extraction of frames and storing original frames)
# * ScaleImageLayer (scaling images to a given ratio)
# * CropImageLayer (cropping frames)
# * QtImageLayer (convert Pillow images to Qt images)
class ImageLayer:
    def __init__(self):
        if type(self) == ImageLayer:
            raise NotImplementedError("ImageLayer is abstract and cannot be instantiated.")

    # Scaled/cropped width (which one depends on the layer, but it also accounts for lower layers)
    def getImageWidth(self):
        return self.getPillowImage(0).width

    # Scaled/cropped height (which one depends on the layer, but it also accounts for lower layers)
    def getImageHeight(self):
        return self.getPillowImage(0).height

    # Raw (not scaled/cropped) width
    def getBaseImageWidth(self):
        return self.sublayer.getBaseImageWidth()

    # Raw (not scaled/cropped) height
    def getBaseImageHeight(self):
        return self.sublayer.getBaseImageHeight()

    def hasAnimation(self):
        return self.getFrameCount() > 1

    # Iterates frames of the image; entirely to allow writing "for frame in layer".
    def __iter__(self):
        class ImageLayerIterator:
            def __init__ (self, lst):
                self.lst = lst
                self.current = 0

            def __iter__ (self):
                return self

            def __next__ (self):
                try:
                    item = self.lst[self.current]
                except IndexError:
                    raise StopIteration()
                self.current += 1
                return item

        return ImageLayerIterator(self.getLayerFrameList())

    def getLayerFrameList(self):
        if hasattr(self, "layer_frames") and self.layer_frames:
            return self.layer_frames
        else:
            return self.sublayer.getLayerFrameList()

    def setBaseImage(self, pillow_image):
        self.sublayer.setBaseImage(pillow_image)
        self.updateLayer()

    # "bounds" is the distances from their respective edges,
    # given as (left, top, right, bottom).
    # Note: Pillow's coordinate system is different!
    # These coordinates get translated to Pillow's later.
    def applyCrop(self, bounds, cumulative):
        self.sublayer.applyCrop(bounds, cumulative)
        self.updateLayer()

    def isCropped(self):
        return self.sublayer.isCropped()

    def getCropBounds(self):
        return self.sublayer.getCropBounds()

    # accumulate_scale, if true, applies the scale ratio on top of the
    # existing scale ratio. Otherwise, the given ratio replaces the old one.
    def applyScale(self, ratio, pillow_filter, accumulate_scale=False):
        self.sublayer.applyScale(ratio, pillow_filter, accumulate_scale)
        self.updateLayer()

    def getScaleRatio(self):
        return self.sublayer.getScaleRatio()

    def getScalingFilter(self):
        return self.sublayer.getScalingFilter()

    def getFrameCount(self):
        return self.sublayer.getFrameCount()

    def getFrameDuration(self, frame_number):
        return self.sublayer.getFrameDuration(frame_number)

    def getPillowImage(self, frame_number):
        return self.getLayerFrameList()[frame_number]

    def getQtImage(self, frame_number):
        raise NotImplementedError


class FileImageLayer(ImageLayer):
    def getBaseImageWidth(self):
        return self.getImageWidth()

    def getBaseImageHeight(self):
        return self.getImageHeight()

    def setBaseImage(self, pillow_image):
        self.layer_frames = []
        self.frame_lengths = []
        if hasattr(pillow_image, "n_frames") and pillow_image.n_frames != 1:
            for i in range(pillow_image.n_frames):
                pillow_image.seek(i)
                self.layer_frames.append(pillow_image.copy())
                self.frame_lengths.append(pillow_image.info['duration'])
        else:
            self.layer_frames = [pillow_image]
            self.frame_lengths = None

    def getFrameDuration(self, frame_number):
        if self.frame_lengths is not None:
            return self.frame_lengths[frame_number]
        else:
            return None

    def getFrameCount(self):
        if self.frame_lengths is not None:
            return len(self.frame_lengths)
        else:
            return 1


class ScaleImageLayer(ImageLayer):
    def __init__(self, sublayer):
        self.sublayer = sublayer

        self.scale_ratio = 1
        self.scaling_filter = PillowImage.Resampling.BILINEAR

    def checkMemoryUsage(self, ratio):
        # This is approximate, but that's enough.
        memory_req = self.getFrameCount() * self.getBaseImageWidth() * self.getBaseImageHeight() * ratio * ratio * 4 / 1024 / 1024
        if memory_req > PER_IMAGE_SCALE_MEMORY_LIMIT_MB and ratio > 1:
            ImageErrorReporter.reportError(_("Cannot increase size: memory usage would exceed limit."))
            return False
        else:
            return True

    def updateLayer(self):
        if self.scale_ratio is not None and not math.isclose(self.scale_ratio, 1):
            # Recheck the scale ratio in case the image has been swapped.
            # It's OK to reset the scale here if it fails; this should ONLY trip when changing
            # images, and it's simpler to just reset it in that case than guess a correct size.
            if not self.checkMemoryUsage(self.scale_ratio):
                self.scale_ratio = 1
                self.layer_frames = None
                return

            orig_width = self.sublayer.getImageWidth()
            orig_height = self.sublayer.getImageHeight()

            size = (int(self.scale_ratio * orig_width), int(self.scale_ratio * orig_height))

            self.layer_frames = []

            for frame in self.sublayer:
                self.layer_frames.append(frame.resize(size, resample=self.scaling_filter))
        else:
            self.layer_frames = None

    def applyScale(self, ratio, pillow_filter, accumulate_scale=False):
        if ratio is not None:
            if accumulate_scale:
                ratio = self.scale_ratio * ratio

            if self.checkMemoryUsage(ratio):
                self.scale_ratio = ratio
            else:
                # Note, this intentionally bypasses image update.
                # If the filter was also intended to be changed, it will need changed again.
                raise ImageMemoryException

        if pillow_filter is not None:
            self.scaling_filter = pillow_filter

        self.updateLayer()

    def getScaleRatio(self):
        return self.scale_ratio

    def getScalingFilter(self):
        return self.scaling_filter


class CropImageLayer(ImageLayer):
    def __init__(self, sublayer):
        self.sublayer = sublayer

        self.crop_bounds = None

    def updateLayer(self):
        if self.crop_bounds is not None and self.crop_bounds != (0, 0, 0, 0):
            if len(self.crop_bounds) != 4:
                raise ValueError

            orig_width = self.sublayer.getImageWidth()
            orig_height = self.sublayer.getImageHeight()

            pil_crop = (self.crop_bounds[0],
                        self.crop_bounds[1],
                        orig_width - self.crop_bounds[2],
                        orig_height - self.crop_bounds[3])

            self.layer_frames = []

            for frame in self.sublayer:
                self.layer_frames.append(frame.crop(pil_crop))
        else:
            self.layer_frames = None

    def setBaseImage(self, pillow_image):
        # Don't allow crop boundaries to carry over between images. They likely do not make sense.
        # In the rare case they do, it would likely confuse the user more than help them.
        self.crop_bounds = None
        super().setBaseImage(pillow_image)

    def applyCrop(self, bounds, cumulative):
        if bounds is not None and len(bounds) != 4:
            raise ValueError

        if self.crop_bounds is not None and cumulative:
            # Add the old bounds and new bounds.
            # We can't just iterate because Python tuples are always constant,
            # so we do this nonsense instead. Gee, Python is so much simpler.
            self.crop_bounds = tuple(map(sum, zip(self.crop_bounds, bounds)))
        else:
            self.crop_bounds = bounds

        self.updateLayer()

    def isCropped(self):
        return self.crop_bounds is not None and self.crop_bounds != (0, 0, 0, 0)

    def getCropBounds(self):
        if self.crop_bounds is not None:
            return self.crop_bounds
        else:
            return (0, 0, 0, 0)

    # Crop needs to implement this function to make sure crop bounds
    # scale with the image. NOTE: this assumes crop is on top of scale in the
    # image layers (it should be).
    def applyScale(self, ratio, pillow_filter, accumulate_scale=False):
        old_ratio = self.sublayer.getScaleRatio()

        # This may raise ImageMemoryException. Let it; it's the caller's job to handle it.
        self.sublayer.applyScale(ratio, pillow_filter, accumulate_scale)

        if ratio is not None and self.isCropped():
            # The ratio may not be exactly what was passed to this function because of accumulate.
            ratio = self.getScaleRatio()

            rel_ratio = ratio / old_ratio
            self.crop_bounds = tuple(int(x * rel_ratio) for x in self.crop_bounds)

        if self.isCropped():
            self.updateLayer()


class QtImageLayer(ImageLayer):
    def __init__(self, sublayer):
        self.sublayer = sublayer

    def updateLayer(self):
        self.qt_images = []
        for frame in self.sublayer:
            self.qt_images.append(PillowImageQt.ImageQt(frame))

    def getQtImage(self, frame_number):
        return self.qt_images[frame_number]


def makeImageLayers():
    # The layers assume this order remains the same. However, new layers could be added.
    file_layer = FileImageLayer()
    scale_layer = ScaleImageLayer(file_layer)
    crop_layer = CropImageLayer(scale_layer)
    qt_layer = QtImageLayer(crop_layer)
    return qt_layer


class Viewer(QMainWindow):
    def __init__(self, app, filepath):
        super().__init__(None)
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.main_menu = None
        self.accum_wheel_delta = 0
        self.drawing_crop = False
        self.drawing_crop_origin = None
        self.rubber_band = None
        self.drag_down_window_offset = None
        self.file_list = None
        self.file_list_thread = None

        self.current_filepath = None
        self.app = app

        self.image_layers = makeImageLayers()

        self.current_frame = 0
        self.play_animation = False

        # This isn't started until an animated image is loaded.
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.animate)
        self.animation_timer.setSingleShot(True)

        self.label = QLabel(self)
        self.setCentralWidget(self.label)

        # TODO: This message can easily be missed if the image is bigger than the screen, which
        # is likely because it's most likely to trigger on giant images.
        self.memory_warning = QLabel(self)
        self.memory_warning.hide()
        self.memory_warning.setStyleSheet("color: white; font-size: 16px; font-weight: 500; background: black; padding: 6px;")
        self.memory_warning.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.memory_warning.updateGeometry()
        self.memory_warning.adjustSize()

        self.warning_timer = QTimer(self)
        self.warning_timer.timeout.connect(self.memory_warning.hide)
        self.warning_timer.setSingleShot(True)
        self.warning_timer.setInterval(WARNING_MESSAGE_INTERVAL_MSEC)

        def showImageMessage(msg):
            self.warning_timer.start()
            self.memory_warning.setText(msg) # Already translated
            self.memory_warning.updateGeometry()
            self.memory_warning.adjustSize()
            self.memory_warning.show()

        ImageErrorReporter.addListenerFxn(showImageMessage)

        self.setImageFromPath(filepath)
        self.regenerate()
        self.initMenu()

    def onCopyImagePath(self):
        try:
            pyperclip.copy(self.current_filepath)
        except pyperclip.PyperclipException as e:
            raise pyperclip.PyperclipException('pyperclip.copy() failed. On Linux/BSD, this may be due to you missing the program "xsel".') from e

    def showAbout(self):
        BasicDialog(self, _("About"), _("ABOUT_CONTENT")).exec()

    def showHelp(self):
        BasicDialog(self, _("Help"), _("HELP_CONTENT")).exec()

    def makeLanguageMenu(self):
        ag_languages = QActionGroup(self)
        ag_languages.setExclusive(True)

        sorted_langs = OrderedDict(sorted(self.app.getLocales().items()))

        for lang_code, lang_name in sorted_langs.items():
            action = QAction(lang_code, self, checkable=True)
            action.triggered.connect(partial(self.app.changeLocale, lang_code))
            action.setText("{} [{}]".format(lang_name, lang_code))

            if lang_code == self.app.getCurrentLocale():
                action.setChecked(True)

            ag_languages.addAction(action)

        menu = QMenu(_diff("Language"))

        menu.addActions(ag_languages.actions())
        return menu

    def initMenu(self):
        if self.main_menu:
            self.main_menu.deleteLater()

        act_next_image = QAction(_("Next image"), self)
        act_next_image.triggered.connect(partial(self.changeImage, 1))

        act_prev_image = QAction(_("Previous image"), self)
        act_prev_image.triggered.connect(partial(self.changeImage, -1))

        act_copy_path = QAction(_("Copy image path"), self)
        act_copy_path.triggered.connect(self.onCopyImagePath)

        ag_scale_filter = QActionGroup(self)
        ag_scale_filter.setExclusive(True)

        for name, filter in SCALE_FILTERS.items():
            action = QAction(_(name), self, checkable=True)
            action.triggered.connect(partial(self.app.setSetting, "ScalingAlgorithm", name))

            # Make tooltips optional if the language lacks them.
            if _(name + "_TOOLTIP") != "":
                action.setToolTip(_(name + "_TOOLTIP"))

            if filter is self.getScalingFilter():
                action.setChecked(True)

            ag_scale_filter.addAction(action)

        ag_scale_level_list = QActionGroup(self)
        ag_scale_level_list.setExclusive(True)

        for name, list in SCALE_LEVEL_LISTS.items():
            action = QAction(_(name), self, checkable=True)
            action.setToolTip(", ".join(['%.2f' % x for x in list]))
            action.triggered.connect(partial(self.app.setSetting, "ScalingList", name))

            if list is self.getScaleLevelList():
                action.setChecked(True)

            ag_scale_level_list.addAction(action)

        ag_file_sort = QActionGroup(self)
        ag_file_sort.setExclusive(True)

        for sort_type in FileSortType:
            action = QAction(_(sort_type.name), self, checkable=True)
            action.triggered.connect(partial(self.app.setSetting, "FileSorting", sort_type.name))

            if sort_type is self.getFileSortType():
                action.setChecked(True)

            ag_file_sort.addAction(action)

        act_disable_movement = QAction(_("Enable window movement workaround"), self)
        act_disable_movement.setToolTip(_("MOVEMENT_WORKAROUND_TOOLTIP"))
        act_disable_movement.setCheckable(True)
        act_disable_movement.setChecked(self.app.getSetting("DisableManualWindowMovement", False))
        self.connect(act_disable_movement, SIGNAL("triggered(bool)"), partial(self.app.setSetting, "DisableManualWindowMovement"))

        act_about = QAction(_("About"), self)
        act_about.triggered.connect(self.showAbout)

        act_help = QAction(_("Help"), self)
        act_help.triggered.connect(self.showHelp)

        act_close_all = QAction(_("Close All Windows"), self)
        act_close_all.triggered.connect(lambda: ActionDialog(self, self.app.shutdown, _("Close all windows?"), _("OK"), _("Cancel"), _("Confirmation")).show())

        act_minimize = QAction(_("Minimize"), self)
        act_minimize.triggered.connect(self.showMinimized)

        act_close = QAction(_("Close"), self)
        act_close.triggered.connect(self.close)

        # Make the menu.
        self.main_menu = QMenu(self)
        self.main_menu.setToolTipsVisible(True)

        self.main_menu.addAction(act_next_image)
        self.main_menu.addAction(act_prev_image)
        self.main_menu.addAction(act_copy_path)

        self.main_menu.addSection(_("Scaling Filter"))
        self.main_menu.addActions(ag_scale_filter.actions())

        self.main_menu.addSection(_("Scaling Levels"))
        self.main_menu.addActions(ag_scale_level_list.actions())

        self.main_menu.addSection(_("File Sorting"))
        self.main_menu.addActions(ag_file_sort.actions())

        self.main_menu.addSection(_("Session"))
        self.main_menu.addAction(act_close_all)

        self.main_menu.addSection(_("Miscellaneous"))
        self.main_menu.addMenu(self.makeLanguageMenu())
        self.main_menu.addAction(act_disable_movement)
        self.main_menu.addAction(act_about)
        self.main_menu.addAction(act_help)

        self.main_menu.addSection(_("Window"))
        self.main_menu.addAction(act_minimize)
        self.main_menu.addAction(act_close)

    def getScalingFilter(self):
        return SCALE_FILTERS[self.app.getSetting("ScalingAlgorithm", "BILINEAR")]

    def getScaleLevelList(self):
        return SCALE_LEVEL_LISTS[self.app.getSetting("ScalingList", "ADAPTIVE")]

    def getFileSortType(self):
        return FileSortType[self.app.getSetting("FileSorting", "MODIFIED_DSC")]

    # Update image scaling (if the scale level list was changed, syncs to the new list),
    # regenerates the menus, and reshows the image.
    def regenerate(self):
        new_scale_ratio = None
        new_scaling_filter = None

        if self.image_layers.getScaleRatio() not in self.getScaleLevelList():
            new_scale_ratio = closestInList(self.getScaleLevelList(), self.image_layers.getScaleRatio(), ListRounding.EITHER)

        if self.getScalingFilter() != self.image_layers.getScalingFilter():
            new_scaling_filter = self.getScalingFilter()

        if new_scale_ratio is not None or new_scaling_filter is not None:
            # If ImageMemoryException is received here, just revert to 1:1. The only reason that
            # should happen is if the image has been changed.
            try:
                self.image_layers.applyScale(new_scale_ratio, new_scaling_filter)
            except ImageMemoryException:
                self.image_layers.applyScale(1, new_scaling_filter)

        self.initMenu()
        self.updateQtImage()

    def notifySettingChanged(self, key):
        if key == "FileSorting":
            self.updateFileList(False)
        elif key == "Language":
            self.initMenu()
        else:
            self.regenerate()

    # If repopulate is true, the whole list will be reconstructed. Otherwise, it will just be
    # resorted.
    def updateFileList(self, repopulate):
        # Complete any existing threads.
        if self.file_list_thread:
            self.file_list_thread.join()
            self.file_list_thread = None

        def threadfxn(repopulate, path, sort, l):
            if repopulate and path:
                dir = os.path.dirname(path)
                for file in os.listdir(path=dir):
                    if os.path.splitext(file)[1].lower() in SUPPORTED_EXTENSIONS:
                        l.append(os.path.join(dir, file))

            if sort in (FileSortType.ALPHABETICAL_ASC, FileSortType.ALPHABETICAL_DSC):
                l.sort(key=cmp_to_key(locale.strcoll), reverse=(sort is FileSortType.ALPHABETICAL_DSC))
            elif sort in (FileSortType.MODIFIED_ASC, FileSortType.MODIFIED_DSC):
                l.sort(key=os.path.getmtime, reverse=(sort is FileSortType.MODIFIED_DSC))
            elif sort in (FileSortType.CREATED_ASC, FileSortType.CREATED_DSC):
                l.sort(key=os.path.getctime, reverse=(sort is FileSortType.CREATED_DSC))
            else:
                raise ValueError("Unhandled sorting")

        if repopulate:
            self.file_list = []

        sort = self.getFileSortType()
        self.file_list_thread = Thread(target=threadfxn, args=[repopulate, self.current_filepath, sort, self.file_list])
        self.file_list_thread.start()

    def getFileList(self):
        if self.file_list_thread:
            self.file_list_thread.join()
            self.file_list_thread = None

        return self.file_list

    def setImageFromPath(self, filepath):
        if self.current_filepath:
            # Check if the path directory is different. If so, the file list needs updated.
            old_dir = os.path.dirname(os.path.realpath(self.current_filepath))
            new_dir = os.path.dirname(os.path.realpath(filepath))
            need_file_list_update = not os.path.samefile(old_dir, new_dir)
        else:
            need_file_list_update = True

        self.image_layers.setBaseImage(PillowImage.open(filepath))
        self.current_filepath = filepath
        self.setWindowTitle(os.path.basename(filepath))

        if need_file_list_update:
            self.updateFileList(True)

        self.current_frame = 0

        if self.image_layers.hasAnimation():
            self.play_animation = True
            self.setFrameTimer()
        else: self.play_animation = False

        self.updateQtImage()

    def changeImage(self, offset):
        if offset == 0:
            return

        file_list = self.getFileList()

        # If image loading fails, we don't want to get stuck.
        # Keep iterating until we get somewhere.
        while True:
            try:
                cur_i = file_list.index(self.current_filepath)
                self.setImageFromPath(file_list[(cur_i + offset) % len(file_list)])
                return
            except (PillowUnidentifiedImageError, FileNotFoundError):
                offset += int(math.copysign(1, offset))

    def prevImage(self):
        self.changeImage(-1)

    def nextImage(self):
        self.changeImage(1)

    def updateQtImage(self):
        pixmap = QPixmap.fromImage(self.image_layers.getQtImage(self.current_frame))

        first_update = self.label.pixmap is None

        self.label.setPixmap(pixmap)

        previous_size = self.size()

        # Needed to keep the image in its current size from blocking shrinking the window.
        self.setMinimumSize(0, 0)

        # Undo the max size that would have been set below in a previous update.
        self.setMaximumSize(self.maximumWidth(), self.maximumHeight())

        self.resize(pixmap.width(), pixmap.height())

        # Prevent maximize or other window size changes.
        self.setMinimumSize(pixmap.width(), pixmap.height())
        self.setMaximumSize(pixmap.width(), pixmap.height())

        new_size = self.size()

        if not first_update:
            resize_offset = (previous_size - new_size) / 2
            self.move(self.pos() + QPoint(resize_offset.width(), resize_offset.height()))

    def animate(self, frame_increment=1):
        total_frames = self.image_layers.getFrameCount()
        self.current_frame = (self.current_frame + frame_increment) % total_frames
        self.updateQtImage()

        if self.play_animation:
            self.setFrameTimer()

    def setFrameTimer(self):
        # The timer was already set up a single-shot.
        # Gifs allow each frame to have a different speed,
        # so we use single-shot to time the next frame.
        self.animation_timer.setInterval(self.image_layers.getFrameDuration(self.current_frame))
        self.animation_timer.start()

    # 'amount' can be negative; if the current scale ratio is not in the scale list,
    # one 'amount' will be consumed to snap the scale ratio to the list.
    def incrementImageScale(self, amount):
        if type(amount) is not int:
            raise ValueError("The amount argument is scale list increments and must be an integer.")

        if amount == 0:
            return

        scale_level_list = self.getScaleLevelList()
        current_scale = self.image_layers.getScaleRatio()

        if amount > 0:
            current_in_list = scale_level_list[closestInList(scale_level_list, current_scale, ListRounding.PREFER_UP)]
        else:
            current_in_list = scale_level_list[closestInList(scale_level_list, current_scale, ListRounding.PREFER_DOWN)]

        if math.isclose(current_in_list, current_scale):
            amount - math.copysign(1, amount) # Basically, move 1 towards 0 as docs say.

        # Either way, we overwrite the actual scale we're using to make sure "in"/index()
        # work correctly.
        current_scale = current_in_list

        index = scale_level_list.index(current_scale)

        # Shift the index based on 'amount' but lock it to the ends of the list.
        # The start being 0, and the end being len(scale_level_list) - 1.
        index = min(max(index + amount, 0), len(scale_level_list) - 1)

        try:
            self.image_layers.applyScale(scale_level_list[index], None)
            self.updateQtImage()
        except ImageMemoryException:
            if math.isclose(current_scale, 1):
                # An unscaled image shouldn't be tripping ImageMemoryException in the first place.
                raise SystemError
            else:
                # Decrement amount and try again.
                amount -= int(math.copysign(1, amount))

                # This shouldn't happen, but if it does, this error prevents an endless
                # loop of this function.
                if index == 0 and amount == -1:
                    raise SystemError

                self.incrementImageScale(amount)

    def resetImageScale(self):
        self.image_layers.applyScale(1, None)
        self.updateQtImage()

    # Fits the image to the screen. If fit_larger is true, the image will be fit on its
    # proportionally (to the screen) smaller side; if it is false, it will be fit on the
    # proportionally larger side. Meaning, fit_larger=true will (probably) make the image
    # exceed the size of the screen on one side, fit_larger=false will (probably) make
    # it smaller than the screen on one side.
    #
    # If the aspect ratio of the image is the same as the (usable) screen,
    # fit_larger=true and fit_larger=false will do the same thing.
    def setScreenFill(self, fit_larger):
        screen_size = self.screen().availableSize()

        width = self.image_layers.getImageWidth()
        height = self.image_layers.getImageHeight()

        ratios = (screen_size.width() / width, screen_size.height() / height)

        if fit_larger:
            factor = max(ratios)
        else:
            factor = min(ratios)

        # Must use use accumulate_scale because the ratio is
        # based on the current scale (indirectly).
        self.image_layers.applyScale(factor, None, True)
        self.updateQtImage()

    def clearCrop(self):
        # Need to move the window to account for removing the crop.
        old_crop = self.image_layers.getCropBounds()
        new_pos = self.pos() - QPoint(old_crop[0], old_crop[1])

        self.image_layers.applyCrop((0, 0, 0, 0), False)
        self.updateQtImage()
        self.move(new_pos) # Must happen after updateQtImage(); that resizes the window

    # Qt handler.
    def wheelEvent(self, event):
        if Qt.AltModifier in event.modifiers():
            # Note: I wanted to make alt control the
            # screen fit, but it seems holding alt causes
            # the angle delta to always be 0.
            self.resetImageScale()
        elif Qt.ControlModifier in event.modifiers():
            if event.angleDelta().y() > 0:
                self.setScreenFill(True)
            else:
                self.setScreenFill(False)
        else:
            self.accum_wheel_delta = self.accum_wheel_delta + event.angleDelta().y()
            steps = self.accum_wheel_delta // WHEEL_DELTA_PER_STEP
            self.accum_wheel_delta -= steps * WHEEL_DELTA_PER_STEP
            if steps != 0:
                self.incrementImageScale(steps)

    # Qt handler.
    def mouseMoveEvent(self, event):
        if self.drawing_crop:
            pos = event.position().toPoint()
            self.rubber_band.setGeometry(QRect(self.drawing_crop_origin, pos).normalized())
        elif self.drag_down_window_offset:
            self.move(self.drag_down_window_offset + event.globalPosition().toPoint())

    # Qt handler.
    def mousePressEvent(self, event):
        if event.button() is Qt.MouseButton.MiddleButton:
            self.close()
        elif event.button() is Qt.MouseButton.LeftButton and Qt.ControlModifier in event.modifiers():
            self.close()
        elif event.button() is Qt.MouseButton.LeftButton and Qt.ShiftModifier in event.modifiers():
            origin = event.position().toPoint()

            if not self.rubber_band:
                self.rubber_band = QRubberBand(QRubberBand.Rectangle, self)

            self.drawing_crop = True
            self.drawing_crop_origin = origin

            self.rubber_band.setGeometry(QRect(origin, QSize()))
            self.rubber_band.show()
        elif event.button() is Qt.MouseButton.LeftButton and Qt.AltModifier in event.modifiers():
            self.resetImageScale()
        elif event.button() is Qt.MouseButton.LeftButton:
            if not bool(self.app.getSetting("DisableManualWindowMovement", False)):
                self.drag_down_window_offset = self.pos() - event.globalPosition().toPoint()

    # Qt handler.
    def mouseReleaseEvent(self, event):
        if event.button() is Qt.MouseButton.LeftButton and self.drawing_crop:
            final_geometry = self.rubber_band.geometry()

            self.rubber_band.hide()
            self.drawing_crop = False

            # Qt allows the geometry to be negative if dragged outside the
            # window, so we need to limit them to the image size.
            image_width = self.image_layers.getImageWidth()
            image_height = self.image_layers.getImageHeight()

            top = max(0, final_geometry.y())
            bottom = image_height - min(final_geometry.y() + final_geometry.height(), image_height)
            left = max(0, final_geometry.x())
            right = image_width - min(final_geometry.x() + final_geometry.width(), image_width)

            # The bottom/right we got above are offsets from those edges of the image/window.
            # However, for the math below, we need a bottom/right that is relative to the top/left.
            rel_bottom = image_height - bottom
            rel_right = image_width - right

            # If the selection is tiny, cancel the crop entirely.
            if (rel_right - left) < MINIMUM_CROPPED_SIZE and (rel_bottom - top) < MINIMUM_CROPPED_SIZE:
                self.clearCrop()

                return

            # Apply the crop - this is cumulative (the true arg), because the coords are
            # window-relative, so they're relative to the already-applied crop bounds.
            self.image_layers.applyCrop((left, top, right, bottom), True)

            # Calculate the position the window belongs at now. However, it
            # isn't moved until later, because updateQtImage() will resize
            # the window, which will mess with positioning.
            new_pos = QPoint(left, top) + self.pos()

            self.updateQtImage()
            self.move(new_pos)
        elif event.button() is Qt.MouseButton.LeftButton and self.drag_down_window_offset:
            self.drag_down_window_offset = None

    # Qt handler.
    def keyPressEvent(self, event):
        if event.key() in [Qt.Key_Left, Qt.Key_Up, Qt.Key_A, Qt.Key_W]:
            self.prevImage()
        elif event.key() in [Qt.Key_Right, Qt.Key_Down, Qt.Key_D, Qt.Key_S]:
            self.nextImage()
        elif event.key() in [Qt.Key_Plus, Qt.Key_Equal]:
            self.incrementImageScale(1)
        elif event.key() in [Qt.Key_Minus, Qt.Key_Underscore]:
            self.incrementImageScale(-1)
        elif event.key() in [Qt.Key_Period]:
            self.resetImageScale()
        elif event.key() in [Qt.Key_Comma, Qt.Key_Z]:
            self.clearCrop()
        elif event.key() in [Qt.Key_Space]:
            if self.play_animation:
                self.play_animation = False
                self.animation_timer.stop()
            elif self.image_layers.hasAnimation():
                self.play_animation = True
                self.setFrameTimer()
        elif event.key() in [Qt.Key_BracketLeft]:
            self.play_animation = False
            self.animation_timer.stop()
            self.animate(-1)
        elif event.key() in [Qt.Key_BracketRight]:
            self.play_animation = False
            self.animation_timer.stop()
            self.animate(1)
        elif event.key() in [Qt.Key_Escape]:
            self.close()

    # Qt handler.
    def mouseDoubleClickEvent(self, event):
        self.showMinimized()

    # Qt handler.
    def contextMenuEvent(self, event):
        self.main_menu.exec(event.globalPos())

    # Qt handler.
    def closeEvent(self, event):
        self.app.windowClosed(self)

    # Qt handler.
    def moveEvent(self, event):
        event.accept()


class ViewerApplication(QApplication):
    def __init__(self, args):
        super().__init__(args)

        # Needed to make sure the dropdown menu section header text appears on Windows.
        self.setStyle("Fusion")

        self.windows = []

        self.settings = QSettings(os.path.join(QStandardPaths.writableLocation(QStandardPaths.GenericConfigLocation), PROGRAM_NAME.lower(), SETTINGS_FILE), QSettings.IniFormat)

        # This triggers saving the recorded language strings to a JSON file on exit, if called for.
        self.language_record = None
        if LANGUAGE_RECORD:
            self.language_record = {}

            def saveLanguageTemplate():
                record_json = json.dumps(self.language_record, sort_keys=True, indent=4)
                record_file = open(os.path.join(LANGUAGE_DIRECTORY, "lang.template"), 'x', encoding="utf8")
                record_file.write(record_json)
                record_file.close()

            atexit.register(saveLanguageTemplate)

        self.languages = {}
        self.language_synonyms = {}
        self.syncLanguages()

        # Note: locale.getdefaultlocale() is deprecated, but locale.getlocale() is broken on Windows
        # and a fix doesn't seem to be coming. Actual removal of getdefaultlocale() seems to be
        # indefinitely on hold as a result (it's already been bumped versions at least twice).
        # https://github.com/python/cpython/issues/82986
        self.changeLocale(self.settings.value("Language", locale.getdefaultlocale()[0]), True)

        self.interprocess_timer = QTimer(self)
        self.interprocess_timer.timeout.connect(self.checkForNewFiles)
        self.interprocess_timer.setInterval(INTERPROCESS_INTERVAL_MSEC)
        self.interprocess_timer.start()

        self.setupApplicationIcon()

        self.setDefaultSettings()

    def setDefaultSettings(self):
        # Note: This should only set settings that change by platform, but still need to be
        # configurable. These will be entered in the settings file. Most other defaults should
        # be handled at the level of settings query, not here.
        # TODO: Might be nice to have a way to do "soft" defaults that are not written to settings.
        if self.getSetting("DisableManualWindowMovement", default=None) is None:
            # KDE/Plasma implements window dragging for frameless windows. If we detect KDE/Plasma,
            # disable window movement to avoid conflicts. Otherwise, make sure it is enabled.
            # TODO: If you know a better way to detect if this is necessary, let me know.
            # Not all KDE configurations implement this behavior, so my current check may turn
            # off window movement in some situations where it is needed.
            # Additionally, some other window managers may require this. I don't know right now.
            if os.environ.get("DESKTOP_SESSION", "").lower() == "plasmax11" or os.environ.get("XDG_SESSION_DESKTOP","").lower() == "kde":
                self.setSetting("DisableManualWindowMovement", True)
            else:
                self.setSetting("DisableManualWindowMovement", False)

    def setupApplicationIcon(self):
        self.application_icon = QIcon()

        self.application_icon.addFile(os.path.join(RESOURCE_DIRECTORY, "kiyoi8.png"), size=QSize(8, 8))
        self.application_icon.addFile(os.path.join(RESOURCE_DIRECTORY, "kiyoi16.png"), size=QSize(16, 16))
        self.application_icon.addFile(os.path.join(RESOURCE_DIRECTORY, "kiyoi32.png"), size=QSize(32, 32))
        self.application_icon.addFile(os.path.join(RESOURCE_DIRECTORY, "kiyoi48.png"), size=QSize(48, 48))
        self.application_icon.addFile(os.path.join(RESOURCE_DIRECTORY, "kiyoi64.png"), size=QSize(64, 64))
        self.application_icon.addFile(os.path.join(RESOURCE_DIRECTORY, "kiyoi128.png"), size=QSize(128, 128))
        self.application_icon.addFile(os.path.join(RESOURCE_DIRECTORY, "kiyoi256.png"), size=QSize(256, 256))

    def syncLanguages(self):
        self.languages = {}
        for file_name in os.listdir(path=LANGUAGE_DIRECTORY):
            if os.path.splitext(file_name)[1] == LANGUAGE_FILE_SUFFIX:
                lang_code = os.path.splitext(file_name)[0].lower()
                if not lang_code in self.languages:
                    path = os.path.join(LANGUAGE_DIRECTORY, file_name)
                    file = open(path, encoding="utf8")
                    self.languages[lang_code] = json.load(file)
                    file.close()

        self.language_synonyms = {}
        for file_name in os.listdir(path=LANGUAGE_SYNONYMS_DIRECTORY):
            # format is FROM.TO.syn, where FROM and TO are a language code. FROM will then use
            # the same language file as provided by TO.
            if os.path.splitext(file_name)[1] != LANGUAGE_SYNONYM_FILE_SUFFIX:
                continue

            bare_name_parts = os.path.splitext(file_name)[0].lower().split(".")

            if len(bare_name_parts) != 2:
                warnings.warn("{}: Invalid language synonym format.".format(file_name))
                continue

            if bare_name_parts[0] in self.languages:
                warnings.warn("{}: Synonym cannot be specified, FROM code '{}' exists as a defined language.".format(file_name, bare_name_parts[0]))
                continue

            if bare_name_parts[1] not in self.languages:
                warnings.warn("{}: Synonym cannot be specified, TO language '{}' does not exist.".format(file_name, bare_name_parts[1]))
                continue

            self.language_synonyms[bare_name_parts[0]] = bare_name_parts[1]

    def changeLocale(self, locale_code, dontsave=False):
        # The locale code is in the format XX[_YY]. Codes are handled case-insensitively.
        #
        # If the code does not exist within the supported languages, language synonyms are checked,
        # such as en->en_US.
        #
        # If XX_YY is not found, XX is tried. This may itself be a synonym.
        #
        # Finally, there is a fallback code that will be used if all else fails. This may happen
        # due to Python having a bad locale, which will cause it to report a "C" locale.
        #
        # XX/YY need not be two characters, but RFC 1766 ones are, and official Kiyoi languages
        # follow RFC 1766 if at all possible.
        locale_code = locale_code.lower()

        def resolveLanguageCode(lc):
            lc = lc.lower()
            if lc in self.languages:
                return lc
            elif lc in self.language_synonyms:
                return resolveLanguageCode(self.language_synonyms[lc])
            elif "_" in lc and lc.split("_")[0] in self.languages:
                return resolveLanguageCode(lc.split("_")[0])
            else:
                return resolveLanguageCode(LANGUAGE_FALLBACK_CODE.lower())

        conf_lc = resolveLanguageCode(locale_code)
        sys_lc = resolveLanguageCode(locale.getdefaultlocale()[0])

        global _
        _ = partial(replaceText, self.languages[conf_lc], record=self.language_record)

        global _sys
        _sys = partial(replaceText, self.languages[sys_lc], record=self.language_record)

        self.locale_code = conf_lc

        # Update the name of the program.
        self.setApplicationDisplayName(_(PROGRAM_FULL_NAME))

        # The locale is only saved if it was used AS GIVEN, without synonyms or fallbacks.
        if dontsave is False and locale_code == conf_lc:
            self.setSetting("Language", locale_code)

    def getCurrentLocale(self):
        return self.locale_code

    def getLocales(self):
        locales = {}
        for code, language in self.languages.items():
            locales[code] = language[LANGUAGE_NAME_STRING]
        return locales

    def getSetting(self, key, default=None):
        value = self.settings.value(key, default)

        # There is some odd behavior with QSettings bools on Windows vs. Linux, so make "true"/True
        # and "false"/False foolproof, even if it's convoluted.
        if str(value).lower() == "true":
            return True
        elif str(value).lower() == "false":
            return False

        return value

    def setSetting(self, key, value):
        self.settings.setValue(key, value)
        self.settings.sync()

        for window in self.windows:
            window.notifySettingChanged(key)

    def windowClosed(self, window):
        self.windows.remove(window)

    def shutdown(self):
        for window in self.windows:
            window.close()

        self.quit()

    def openImageFile(self, path):
        viewer = Viewer(self, path)

        viewer.setWindowIcon(self.application_icon)

        # Sidestep the window getting "stuck" to the screen edges if too large;
        # show the window first, then confiure it.
        # See: https://stackoverflow.com/a/68477844
        viewer.show()
        viewer.updateQtImage()

        # We attempt to activate the window, but note that due to how many window managers
        # attempt to prevent focus stealing, this probably won't work.
        # If I redo how the instance invocations work, this may work better.
        viewer.activateWindow()

        # Center the window.
        screen_geo = viewer.screen().geometry()
        viewer_geo = viewer.frameGeometry()
        x_pos = screen_geo.width()/2 - viewer_geo.width()/2
        y_pos = screen_geo.height()/2 - viewer_geo.height()/2
        viewer.setGeometry(x_pos, y_pos, viewer_geo.width(), viewer_geo.height())

        self.windows.append(viewer)

    def checkForNewFiles(self):
        # Get all the request files.
        request_file_list = []
        dir = os.path.dirname(getInterprocessCommunicationDir())
        for file in os.listdir(path=dir):
            if os.path.splitext(file)[1] == MAIN_INSTANCE_REQUEST_FILE_SUFFIX:
                request_file_list.append(os.path.join(dir, file))

        # Parse the request files into actual image requests.aboutToQuit
        #
        # This is broken up so that waiting on an image to open doesn't
        # cause new master instances to be incorrectly started.
        request_image_list = []
        for request_file in request_file_list:
            with open(request_file, 'r', encoding="utf8") as file:
                for line in file:
                    if line != "":
                        request_image_list.append(line)
            os.remove(request_file)

        # Actually attempt to open the image requests.
        for request_image in request_image_list:
            self.openImageFile(request_image)

        # If there are no more windows open, quit.
        if len(self.windows) == 0:
            self.quit()


def createMainInstance(path):
    try:
        os.makedirs(getInterprocessCommunicationDir())
    except:
        pass

    try:
        lockfile = open(getLockFilePath(), 'x', encoding="utf8")
    except OSError as e:
        # The file either exists or it couldn't be created.
        # Those are separate issues, so check again if it
        # exists.
        if os.path.exists(getLockFilePath()):
            # This process was stepped on by another starting process.
            # Fail, let the caller determine what to do (probably notify
            # the process that exists).
            return False
        else:
            # Something else is wrong. Reraise.
            raise OSError('Cannot create main instance lock file.') from e

    lockfile.write("Main instance PID: {}".format(os.getpid()))
    lockfile.close()

    try:
        app = ViewerApplication(sys.argv)
        app.openImageFile(path)
        app.exec()
    finally:
        os.remove(getLockFilePath())

    return True

def notifyMainInstance(path):
    request_file = MAIN_INSTANCE_REQUEST_FILE_PREFIX + str(uuid.uuid4()) + MAIN_INSTANCE_REQUEST_FILE_SUFFIX
    request_path = os.path.join(getInterprocessCommunicationDir(), request_file)
    requestfile = open(request_path, 'x', encoding="utf8")
    requestfile.write(path)
    requestfile.close()

    # We use a partially random interval to try to avoid restarting the
    # server multiple times at once, if multiple instances were all
    # opened while the main instance was dead. This isn't foolproof,
    # but it's something.
    random_sleep_msec = MAIN_INSTANCE_REQUEST_TIMEOUT_RANDOM_MSEC * random.random()
    sleep((MAIN_INSTANCE_REQUEST_TIMEOUT_MIN_MSEC + random_sleep_msec) / 1000)

    if os.path.exists(request_path):
        # The request was never received... main instance may be dead, try to
        # restart it.
        os.remove(request_path)
        os.remove(getLockFilePath())
        return False

    return True

def createOrNotifyMainInstance(path):
    if os.path.exists(getLockFilePath()):
        # No main instance, attempt to start one.
        if notifyMainInstance(path):
            return
        else:
            # Couldn't notify instance, it may have died.
            # Try again.
            createOrNotifyMainInstance(path)
    else:
        # Main instance exists (or existed), attempt to notify it.
        if createMainInstance(path):
            return
        else:
            # Creating the main instance failed, but there wasn't a critical
            # error, so it must already exist. Try to notify it.
            createOrNotifyMainInstance(path)

def kiyoi_run():
    parser = argparse.ArgumentParser(description=PROGRAM_FULL_NAME)
    parser.add_argument('path', nargs='?', help="Path to image. If not given, a file browser will be opened.")
    args = parser.parse_args()

    path = args.path

    if path is None:
        # We need to start an application to be able to show the file browser,
        # but we also don't keep it around because we may not want it.
        app = QApplication()
        path = QFileDialog.getOpenFileName(filter=BROWSER_FILTER)[0]
        app.shutdown()

    if path:
        # Because of the business with having a single master instance,
        # relative paths need resolved NOW or they may be mishandled.
        # Additionally, if the path is bad (and we can detect that),
        # we want to fail now, in the instance the user actually started,
        # rather than have the master instance spit out an unhelpful error.
        path = os.path.realpath(path)

        # Fail early if possible. We can't reasonably detect invalid images,
        # but we can detect ones that don't exist or we don't support.
        if not os.path.isfile(path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)

        if not os.path.splitext(path)[1].lower() in SUPPORTED_EXTENSIONS:
            raise ValueError("Invalid file type")

        createOrNotifyMainInstance(path)

if __name__ == "__main__":
    kiyoi_run()
