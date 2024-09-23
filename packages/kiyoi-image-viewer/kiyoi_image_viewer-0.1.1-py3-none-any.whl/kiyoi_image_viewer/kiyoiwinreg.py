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

# This script is ONLY for Windows. Linux should use the .desktop file provided.
#
# Additionally, this script only works system-wide: you CANNOT install Kiyoi
# if it is within a user-only Python install. That may change, but the Windows
# file association system is very cryptic and I haven't been able to
# successfully install on a user-only basis.
#
# This will write/delete (install/uninstall) the following registry keys/values:
#
# CLASS_ROOT/Applications/kiyoi_image_viewer.exe
# CLASS_ROOT/Applications/kiyoi_image_viewer.exe/SupportedTypes
# CLASS_ROOT/Applications/kiyoi_image_viewer.exe/DefaultIcon
# CLASS_ROOT/Applications/kiyoi_image_viewer.exe/DefaultIcon  (Default)
# CLASS_ROOT/Applications/kiyoi_image_viewer.exe/shell
# CLASS_ROOT/Applications/kiyoi_image_viewer.exe/shell  (Default)
# CLASS_ROOT/Applications/kiyoi_image_viewer.exe/shell/open
# CLASS_ROOT/Applications/kiyoi_image_viewer.exe/shell/open  FriendlyAppName
# CLASS_ROOT/Applications/kiyoi_image_viewer.exe/shell/open/command
# CLASS_ROOT/Applications/kiyoi_image_viewer.exe/shell/open/command  (Default)
# HKEY_LOCAL_MACHINE/SOFTWARE/Kiyoi
# HKEY_LOCAL_MACHINE/SOFTWARE/Kiyoi/Capabilities
# HKEY_LOCAL_MACHINE/SOFTWARE/Kiyoi/Capabilities  ApplicationName
# HKEY_LOCAL_MACHINE/SOFTWARE/Kiyoi/Capabilities  ApplicationDescription
# HKEY_LOCAL_MACHINE/SOFTWARE/Kiyoi/Capabilities  ApplicationIcon
# HKEY_LOCAL_MACHINE/SOFTWARE/Kiyoi/Capabilities/FileAssociations
# HKEY_LOCAL_MACHINE/SOFTWARE/RegisteredApplications  Kiyoi
# MUI_CACHE  {...}.FriendlyAppName
# MUI_CACHE  {...}.ApplicationCompany
# for ext in SUPPORTED_EXTENSIONS_NO_DOT:
#   CLASS_ROOT/Kiyoi.EXT
#   CLASS_ROOT/Kiyoi.EXT  (Default)
#   CLASS_ROOT/Kiyoi.EXT/DefaultIcon
#   CLASS_ROOT/Kiyoi.EXT/DefaultIcon  (Default)
#   CLASS_ROOT/Kiyoi.EXT/shell
#   CLASS_ROOT/Kiyoi.EXT/shell  (Default)
#   CLASS_ROOT/Kiyoi.EXT/shell/open
#   CLASS_ROOT/Kiyoi.EXT/shell/open  FriendlyAppName
#   CLASS_ROOT/Kiyoi.EXT/shell/open/command
#   CLASS_ROOT/Kiyoi.EXT/shell/open/command  (Default)
#   CLASS_ROOT/.ext/OpenWithProgids  Kiyoi.EXT
#   CLASS_ROOT/Applications/kiyoi_image_viewer.exe/SupportedTypes  .ext
#   HKEY_LOCAL_MACHINE/SOFTWARE/Kiyoi/Capabilities/FileAssociations/  .ext
#   HKEY_CURRENT_USER/SOFTWARE/Microsoft/Windows/CurrentVersion/Explorer/FileExts/.ext/OpenWithList  (next highest letter)
#   HKEY_CURRENT_USER/SOFTWARE/Microsoft/Windows/CurrentVersion/Explorer/FileExts/.ext/OpenWithList  MRUList
#
# CLASS_ROOT is HKEY_LOCAL_MACHINE/Software/Classes
# MUI_CACHE is HKEY_CURRENT_USER/SOFTWARE/Classes/Local Settings/Software/Microsoft/Windows/Shell/MuiCache

# Note that this only makes Kiyoi available in the two "Open With" lists. This does not
# automatically take over the default file association (yet).
#
# Additionally, full integration will only be added/removed for the current user due to how Windows
# loads user registry keys. Registry files for other users have to be manually loaded and referenced
# through HKEY_USERS, which this script currently does not do. If you want full support for
# multiple users, run the script as those users.
#
# TODO: Currently, the icon doesn't work right. I'm not sure if this a mistake on my part or a
# limitation in Windows.

import os
import platform
import string
import sys

from .kiyoiconstants import *

SCRIPT_PATH = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

def pythonIsSystemwide():
    return sys.executable.split(os.sep)[1].lower() != "users"

def validateEnvOrExit():
    if platform.system() != "Windows":
        print("This command is only intended for use on Windows. On Linux, use the .desktop file.")
        sys.exit()

    if not pythonIsSystemwide():
        print("This command does not support installing Kiyoi file associations if Python is not an all-users/system install.")
        sys.exit()

    import ctypes

    if ctypes.windll.shell32.IsUserAnAdmin():
        return
    else:
        # Rerun program, asking for admin permissions so we can run registry commands.
        # Note: This assumes being run through the Python-genereated .exe entry point.
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.argv[0], "", None, 1)
        sys.exit()


def disclaimerOrExit():
    disclaimer = ('THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH\n'
                  'REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY\n'
                  'AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,\n'
                  'INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM\n'
                  'LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR\n'
                  'OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR\n'
                  'PERFORMANCE OF THIS SOFTWARE.\n'
                  '\n'
                  'This is beta software that will edit your system registry.\n'
                  'Please confirm you accept all risk associated with that by entering "agree" here: ')
    
    print(disclaimer)
    if input().lower() != "agree":
        sys.exit()


def getSoftwareKey():
    import winreg
    return winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "Software")

def getClassesKey():
    import winreg
    return winreg.OpenKey(getSoftwareKey(), "Classes")

def getMuiCacheKey():
    import winreg
    return winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER, "SOFTWARE\\Classes\\Local Settings\\Software\\Microsoft\\Windows\\Shell\\MuiCache", access=winreg.KEY_WRITE)

def getOpenWithListKey(ext):
    import winreg
    ext_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\FileExts\\." + ext.lower())
    return winreg.CreateKey(ext_key, "OpenWithList")

# This is used to silently fail to delete keys that don't exist, such as due to a previous failed
# installation or new functionality which may have not previously been set up.
def suppressOSError(fxn, *args):
    try:
        fxn(*args)
    except OSError:
        pass


def kiyoi_winreg_install():
    validateEnvOrExit()
    disclaimerOrExit()

    import winreg

    executable_name = PROGRAM_FULL_NAME.replace(" ", "_").lower() + ".exe"
    executable_path = os.path.join(os.path.split(sys.executable)[0], "Scripts", executable_name)
    kiyoi_command = "\"{}\" \"%1\"".format(executable_path)
    icon_path = os.path.join(SCRIPT_PATH, "resources", "kiyoi.ico")

    classes_key = getClassesKey()

    # Create: CLASS_ROOT/Applications/kiyoi_image_viewer.exe
    kiyoi_app_key = winreg.CreateKey(classes_key, "Applications\\" + executable_name)

    # Create: CLASS_ROOT/Applications/kiyoi_image_viewer.exe/SupportedTypes
    kiyoi_app_types_key = winreg.CreateKey(kiyoi_app_key, "SupportedTypes")

    # Create: CLASS_ROOT/Applications/kiyoi_image_viewer.exe/DefaultIcon
    kiyoi_app_icon_key = winreg.CreateKey(kiyoi_app_key, "DefaultIcon")

    # CLASS_ROOT/Applications/kiyoi_image_viewer.exe/DefaultIcon  (Default)=icon_path
    winreg.SetValueEx(kiyoi_app_icon_key, "", 0, winreg.REG_SZ, icon_path)

    # Create: CLASS_ROOT/Applications/kiyoi_image_viewer.exe/shell
    app_shell_key = winreg.CreateKey(kiyoi_app_key, "shell")

    # CLASS_ROOT/Applications/kiyoi_image_viewer.exe/shell  (Default)=open
    winreg.SetValueEx(app_shell_key, "", 0, winreg.REG_SZ, "open")

    # Create: CLASS_ROOT/Applications/kiyoi_image_viewer.exe/shell/open
    app_open_key = winreg.CreateKey(app_shell_key, "open")

    # CLASS_ROOT/Applications/kiyoi_image_viewer.exe/shell/open  FriendlyAppName=PROGRAM_FULL_NAME
    winreg.SetValueEx(app_open_key, "FriendlyAppName", 0, winreg.REG_SZ, PROGRAM_FULL_NAME)

    # Create: CLASS_ROOT/Applications/kiyoi_image_viewer.exe/shell/open/command
    app_command_key = winreg.CreateKey(app_open_key, "command")

    # CLASS_ROOT/Applications/kiyoi_image_viewer.exe/shell/open/command  (Default)=kiyoi_command
    winreg.SetValueEx(app_command_key, "", 0, winreg.REG_SZ, kiyoi_command)

    software_key = getSoftwareKey()

    # Create: HKEY_LOCAL_MACHINE/SOFTWARE/Kiyoi
    kiyoi_software_key = winreg.CreateKey(software_key, PROGRAM_NAME)

    # Create: HKEY_LOCAL_MACHINE/SOFTWARE/Kiyoi/Capabilities
    software_capabilities_key = winreg.CreateKey(kiyoi_software_key, "Capabilities")

    # Set: HKEY_LOCAL_MACHINE/SOFTWARE/Kiyoi/Capabilities  ApplicationName=PROGRAM_NAME
    winreg.SetValueEx(software_capabilities_key, "ApplicationName", 0, winreg.REG_SZ, PROGRAM_NAME)

    # Set: HKEY_LOCAL_MACHINE/SOFTWARE/Kiyoi/Capabilities  ApplicationDescription=PROGRAM_FULL_NAME
    winreg.SetValueEx(software_capabilities_key, "ApplicationDescription", 0, winreg.REG_SZ, PROGRAM_FULL_NAME)

    # Set: HKEY_LOCAL_MACHINE/SOFTWARE/Kiyoi/Capabilities  ApplicationIcon=icon_path
    winreg.SetValueEx(software_capabilities_key, "ApplicationIcon", 0, winreg.REG_SZ, icon_path)

    # Create: HKEY_LOCAL_MACHINE/SOFTWARE/Kiyoi/Capabilities/FileAssociations
    software_fileassoc_key = winreg.CreateKey(software_capabilities_key, "FileAssociations")

    registered_apps_key = winreg.CreateKey(software_key, "RegisteredApplications")
    # Create: HKEY_LOCAL_MACHINE/SOFTWARE/RegisteredApplications  Kiyoi=SOFTWARE\Kiyoi\Capabilities
    winreg.SetValueEx(registered_apps_key, PROGRAM_NAME, 0, winreg.REG_SZ, "SOFTWARE\\{}\\Capabilities".format(PROGRAM_NAME))

    mui_cache_key = getMuiCacheKey()
    # MUI_CACHE  executable_path.FriendlyAppName=PROGRAM_NAME
    winreg.SetValueEx(mui_cache_key, executable_path + ".FriendlyAppName", 0, winreg.REG_SZ, PROGRAM_NAME)

    # MUI_CACHE  executable_path.ApplicationCompany=PROGRAM_NAME
    winreg.SetValueEx(mui_cache_key, executable_path + ".ApplicationCompany", 0, winreg.REG_SZ, PROGRAM_NAME)

    for ext in SUPPORTED_EXTENSIONS_NO_DOT:
        type_name = ext.upper() + " File"

        # Create: CLASS_ROOT/Kiyoi.ext
        kiyoi_class_key = winreg.CreateKey(classes_key, PROGRAM_NAME + "." + ext.lower())

        # Set: CLASS_ROOT/Kiyoi.ext  (Default)=type_name
        winreg.SetValueEx(kiyoi_class_key, "", 0, winreg.REG_SZ, type_name)

        # Create: CLASS_ROOT/Kiyoi.ext/DefaultIcon
        icon_key = winreg.CreateKey(kiyoi_class_key, "DefaultIcon")

        # Set: CLASS_ROOT/Kiyoi.ext/DefaultIcon  (Default)=icon_path
        winreg.SetValueEx(icon_key, "", 0, winreg.REG_SZ, icon_path)

        # Create: CLASS_ROOT/Kiyoi.ext/shell
        shell_key = winreg.CreateKey(kiyoi_class_key, "shell")

        # Set: CLASS_ROOT/Kiyoi.ext/shell  (Default)=open
        winreg.SetValueEx(shell_key, "", 0, winreg.REG_SZ, "open")

        # Create: CLASS_ROOT/Kiyoi.ext/shell/open
        open_key = winreg.CreateKey(shell_key, "open")

        # Set: CLASS_ROOT/Kiyoi.ext/shell/open  FriendlyAppName=PROGRAM_FULL_NAME
        winreg.SetValueEx(open_key, "FriendlyAppName", 0, winreg.REG_SZ, PROGRAM_FULL_NAME)

        # Create: CLASS_ROOT/Kiyoi.ext/shell/open/command
        command_key = winreg.CreateKey(open_key, "command")

        # Set: CLASS_ROOT/Kiyoi.ext/shell/open/command  (Default)=kiyoi_command
        winreg.SetValueEx(command_key, "", 0, winreg.REG_SZ, kiyoi_command)

        # Create: CLASS_ROOT/.ext
        ext_key = winreg.CreateKey(classes_key, "." + ext.lower())

        # Create: CLASS_ROOT/.ext/OpenWithProgids
        ext_progid_key = winreg.CreateKey(ext_key, "OpenWithProgids")

        # Set: CLASS_ROOT/.ext/OpenWithProgids  Kiyoi.ext=""
        winreg.SetValueEx(ext_progid_key, PROGRAM_NAME + "." + ext.lower(), 0, winreg.REG_SZ, "")

        # Set: CLASS_ROOT/Applications/kiyoi_image_viewer.exe/SupportedTypes  .ext=""
        winreg.SetValueEx(kiyoi_app_types_key, "." + ext.lower(), 0, winreg.REG_SZ, "")

        # Set: HKEY_LOCAL_MACHINE/SOFTWARE/Kiyoi/Capabilities/FileAssociations/  .ext=Kiyoi.ext
        winreg.SetValueEx(software_fileassoc_key, "." + ext.lower(), 0, winreg.REG_SZ, PROGRAM_NAME + "." + ext.lower())

        # Set: HKEY_CURRENT_USER/SOFTWARE/Microsoft/Windows/CurrentVersion/Explorer/FileExts/.ext/OpenWithList  (next highest letter)=executable_name
        # Set: HKEY_CURRENT_USER/SOFTWARE/Microsoft/Windows/CurrentVersion/Explorer/FileExts/.ext/OpenWithList  MRUList (update it)
        open_with_list_key = getOpenWithListKey(ext)
        letters = ""
        already_added = False
        for i in range(winreg.QueryInfoKey(open_with_list_key)[1]):
            value = winreg.EnumValue(open_with_list_key, i)
            if value[1] == executable_name:
                already_added = True
                break

            if value[0].lower() in string.ascii_lowercase:
                letters += value[0].lower()

        if len(letters) == 0:
            open_letter = 'a'
            letters = open_letter
        else:
            # This will give the lowest "open" letter.
            # Note if this goes above Z there are problems.
            open_letters = [l for l in string.ascii_lowercase if l not in letters]
            open_letters = "".join(sorted(open_letters))
            if len(open_letters) > 1:
                open_letter = open_letters[0]
                letters += open_letter
                letters = "".join(sorted(letters))

        if not already_added:
            winreg.SetValueEx(open_with_list_key, open_letter, 0, winreg.REG_SZ, executable_name)

        if len(letters) != 0:
            winreg.SetValueEx(open_with_list_key, "MRUList", 0, winreg.REG_SZ, letters)

    import ctypes
    ctypes.windll.user32.MessageBoxW(0, "Kiyoi successfully added to Windows registry", "Complete", 1)

def kiyoi_winreg_uninstall():
    validateEnvOrExit()
    disclaimerOrExit()

    import winreg

    classes_key = getClassesKey()

    executable_name = PROGRAM_FULL_NAME.replace(" ", "_").lower() + ".exe"
    executable_path = os.path.join(os.path.split(sys.executable)[0], "Scripts", executable_name)

    # Delete: CLASS_ROOT/Applications/kiyoi_image_viewer.exe/shell/open/command
    suppressOSError(winreg.DeleteKey, classes_key, "Applications\\kiyoi_image_viewer.exe\\shell\\open\\command")

    # Delete: CLASS_ROOT/Applications/kiyoi_image_viewer.exe/shell/open
    suppressOSError(winreg.DeleteKey, classes_key, "Applications\\kiyoi_image_viewer.exe\\shell\\open")

    # Delete: CLASS_ROOT/Applications/kiyoi_image_viewer.exe/shell
    suppressOSError(winreg.DeleteKey, classes_key, "Applications\\kiyoi_image_viewer.exe\\shell")

    # Delete: CLASS_ROOT/Applications/kiyoi_image_viewer.exe/SupportedTypes
    suppressOSError(winreg.DeleteKey, classes_key, "Applications\\kiyoi_image_viewer.exe\\SupportedTypes")

    # Delete: CLASS_ROOT/Applications/kiyoi_image_viewer.exe/DefaultIcon
    suppressOSError(winreg.DeleteKey, classes_key, "Applications\\kiyoi_image_viewer.exe\\DefaultIcon")

    # Delete: CLASS_ROOT/Applications/kiyoi_image_viewer.exe
    suppressOSError(winreg.DeleteKey, classes_key, "Applications\\kiyoi_image_viewer.exe")

    # Delete: HKEY_LOCAL_MACHINE/SOFTWARE/Kiyoi/Capabilities/FileAssociations
    suppressOSError(winreg.DeleteKey, winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Kiyoi\\Capabilities\\FileAssociations")

    # Delete: HKEY_LOCAL_MACHINE/SOFTWARE/Kiyoi/Capabilities
    suppressOSError(winreg.DeleteKey, winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Kiyoi\\Capabilities")

    # Delete: HKEY_LOCAL_MACHINE/SOFTWARE/Kiyoi
    suppressOSError(winreg.DeleteKey, winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Kiyoi")

    registered_apps_key = winreg.CreateKey(getSoftwareKey(), "RegisteredApplications")
    # Delete: HKEY_LOCAL_MACHINE/SOFTWARE/RegisteredApplications  Kiyoi
    suppressOSError(winreg.DeleteValue, registered_apps_key, PROGRAM_NAME)

    mui_cache_key = getMuiCacheKey()
    # Delete: MUI_CACHE  executable_path.FriendlyAppName
    suppressOSError(winreg.DeleteValue, mui_cache_key, executable_path + ".FriendlyAppName")

    # Delete: MUI_CACHE  executable_path.ApplicationCompany
    suppressOSError(winreg.DeleteValue, mui_cache_key, executable_path + ".ApplicationCompany")

    for ext in SUPPORTED_EXTENSIONS_NO_DOT:
        program_ext = PROGRAM_NAME + "." + ext.lower()

        # Delete: CLASS_ROOT/Kiyoi.ext/shell/open/command
        suppressOSError(winreg.DeleteKey, classes_key, program_ext + "\\shell\\open\\command")

        # Delete: CLASS_ROOT/Kiyoi.ext/shell/open
        suppressOSError(winreg.DeleteKey, classes_key, program_ext + "\\shell\\open")

        # Delete: CLASS_ROOT/Kiyoi.ext/shell
        suppressOSError(winreg.DeleteKey, classes_key, program_ext + "\\shell")

        # Delete: CLASS_ROOT/Kiyoi.ext/DefaultIcon
        suppressOSError(winreg.DeleteKey, classes_key, program_ext + "\\DefaultIcon")

        # Delete: CLASS_ROOT/Kiyoi.ext
        suppressOSError(winreg.DeleteKey, classes_key, program_ext)

        ext_progid_key = winreg.CreateKey(classes_key, "." + ext.lower() + "\\OpenWithProgids")

        # Delete: CLASS_ROOT/.ext/OpenWithProgids  Kiyoi.ext
        suppressOSError(winreg.DeleteValue, ext_progid_key, program_ext)

        # Delete: HKEY_CURRENT_USER/SOFTWARE/Microsoft/Windows/CurrentVersion/Explorer/FileExts/.ext/OpenWithList  (Any matching entries)
        # Set: HKEY_CURRENT_USER/SOFTWARE/Microsoft/Windows/CurrentVersion/Explorer/FileExts/.ext/OpenWithList  MRUList
        open_with_list_key = getOpenWithListKey(ext)
        remove_letters = ""
        keep_letters = ""
        for i in range(winreg.QueryInfoKey(open_with_list_key)[1]):
            value = winreg.EnumValue(open_with_list_key, i)
            if value[1] == executable_name:
                remove_letters += value[0].lower()

            if value[0].lower() in string.ascii_lowercase:
                keep_letters += value[0].lower()

        for rl in remove_letters:
            suppressOSError(winreg.DeleteValue, open_with_list_key, rl)

        if len(keep_letters) == 0:
            # No remaining associations, so delete the whole extension.
            # Delete: HKEY_CURRENT_USER/SOFTWARE/Microsoft/Windows/CurrentVersion/Explorer/FileExts/.ext/OpenWithList
            # Delete: HKEY_CURRENT_USER/SOFTWARE/Microsoft/Windows/CurrentVersion/Explorer/FileExts/.ext
            suppressOSError(winreg.DeleteKey, winreg.HKEY_CURRENT_USER, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\FileExts\\.{}\\OpenWithList".format(ext.lower()))
            suppressOSError(winreg.DeleteKey, winreg.HKEY_CURRENT_USER, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\FileExts\\.{}".format(ext.lower()))
        else:
            winreg.SetValueEx(open_with_list_key, "MRUList", 0, winreg.REG_SZ, keep_letters)

    import ctypes
    ctypes.windll.user32.MessageBoxW(0, "Kiyoi successfully removed from the Windows registry", "Complete", 1)
