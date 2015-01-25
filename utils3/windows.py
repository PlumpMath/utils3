"""
Windows Specific functions

"""
#---------------------------------------------#
#       WINDOWS FUNCTIONS                     #
#---------------------------------------------#

import time

try:
    import win32api
    import win32con
    import ctypes

    OpenClipboard = ctypes.windll.user32.OpenClipboard
    EmptyClipboard = ctypes.windll.user32.EmptyClipboard
    GetClipboardData = ctypes.windll.user32.GetClipboardData
    SetClipboardData = ctypes.windll.user32.SetClipboardData
    CloseClipboard = ctypes.windll.user32.CloseClipboard
    GlobalLock = ctypes.windll.kernel32.GlobalLock
    GlobalAlloc = ctypes.windll.kernel32.GlobalAlloc
    GlobalUnlock = ctypes.windll.kernel32.GlobalUnlock
    memcpy = ctypes.cdll.msvcrt.memcpy
except:
    pass

""" Abbreviations for readability """

""" Windows Clipboard utilities """


def GetClipboardText():
    text = ""
    if OpenClipboard(0):
        hClipMem = GetClipboardData(win32con.CF_TEXT)
        GlobalLock.restype = ctypes.c_char_p
        text = GlobalLock(hClipMem)
        GlobalUnlock(hClipMem)
        CloseClipboard()
    return text


def SetClipboardText(text):
    buffer = ctypes.c_buffer(text)
    bufferSize = ctypes.sizeof(buffer)
    hGlobalMem = GlobalAlloc(win32con.GHND, bufferSize)
    GlobalLock.restype = ctypes.c_void_p
    lpGlobalMem = GlobalLock(hGlobalMem)
    memcpy(lpGlobalMem, ctypes.addressof(buffer), bufferSize)
    GlobalUnlock(hGlobalMem)
    if OpenClipboard(0):
        EmptyClipboard()
        SetClipboardData(win32con.CF_TEXT, hGlobalMem)
        CloseClipboard()


""" Windows Registry utilities """


def OpenRegistryKey(hiveKey, key):
    keyHandle = None
    try:
        curKey = ""
        keyItems = key.split('\\')
        for keyItem in keyItems:
            if curKey:
                curKey = curKey + "\\" + keyItem
            else:
                curKey = keyItem
            keyHandle = win32api.RegCreateKey(hiveKey, curKey)
    except Exception as e:
        keyHandle = None
        print("OpenRegistryKey failed:", e)
    return keyHandle


def ReadRegistryValue(hiveKey, key, name):
    """ Simple api to read one value from Windows registry.
    If 'name' is empty string, reads default value."""
    data = typeId = None
    try:
        hKey = win32api.RegOpenKeyEx(hiveKey, key, 0, win32con.KEY_ALL_ACCESS)
        data, typeId = win32api.RegQueryValueEx(hKey, name)
        win32api.RegCloseKey(hKey)
    except Exception as e:
        print("ReadRegistryValue failed:", e)
    return data, typeId


def WriteRegistryValue(hiveKey, key, name, typeId, data):
    """ Simple api to write one value to Windows registry.
    If 'name' is empty string, writes to default value."""
    try:
        keyHandle = OpenRegistryKey(hiveKey, key)
        win32api.RegSetValueEx(keyHandle, name, 0, typeId, data)
        win32api.RegCloseKey(keyHandle)
    except Exception as e:
        print("WriteRegistry failed:", e)


""" misc utilities """


def GetPythonwExePath():
    """ Get path to current version of pythonw.exe """
    pythonExePath = ""
    try:
        pythonwExeName = "pythonw.exe"
        pythonInstallHiveKey = win32con.HKEY_LOCAL_MACHINE
        pythonInstallKey = r"Software\Python\PythonCore\%s\InstallPath" % sys.winver
        pythonInstallDir, typeId = ReadRegistryValue(pythonInstallHiveKey, pythonInstallKey, "")
        pythonwExePath = os.path.join(pythonInstallDir, pythonwExeName)
    except Exception as e:
        print("GetPythonExePath failed:", e)
    return pythonwExePath


def get_desktop_path():
    """
    Returns the desktop directory.

    ------------------
    It could be used the environement variables,
    however it is not compatibel with locales
    differents from English.
    """
    from win32com.shell import shell, shellcon

    return shell.SHGetFolderPath(0, shellcon.CSIDL_DESKTOP, None, 0)


def get_appdata_path():
    from win32com.shell import shell, shellcon

    return shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, None, 0)


def get_facvorites_path():
    from win32com.shell import shell, shellcon

    print(shell.SHGetFolderPath(0, shellcon.CSIDL_FAVORITES, None, 0))


def get_drivers():
    """
    Return Windows drivers:

    >>> get_drivers()
    ['C:\\', 'D:\\', 'Z:\\']
    """
    import win32api

    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]
    return drives


def create_link(orig, dest, descripion=""):
    """
    Create Linking to File:
        orig: Origin File or directory
        dest: Destination directory
    """

    import os, sys
    import pythoncom
    from win32com.shell import shell, shellcon

    fpath, fname = os.path.split(orig)
    linkname = fname.split('.')[0] + ".lnk"

    shortcut = pythoncom.CoCreateInstance(
        shell.CLSID_ShellLink,
        None,
        pythoncom.CLSCTX_INPROC_SERVER,
        shell.IID_IShellLink
    )
    shortcut.SetPath(orig)
    shortcut.SetDescription(descripion)
    shortcut.SetIconLocation(orig, 0)

    desktop_path = shell.SHGetFolderPath(0, shellcon.CSIDL_DESKTOP, 0, 0)
    persist_file = shortcut.QueryInterface(pythoncom.IID_IPersistFile)
    persist_file.Save(os.path.join(dest, linkname), 0)


def get_shares():
    """ Get Windows Share Directories """

    import win32net
    import win32netcon

    COMPUTER_NAME = ""  # look at this machine
    INFO_LEVEL = 2

    shares_ = []

    resume = 0
    while 1:
        (shares, total, resume) = \
            win32net.NetShareEnum(
                COMPUTER_NAME,
                INFO_LEVEL,
                resume,
                win32netcon.MAX_PREFERRED_LENGTH
            )
        for share in shares:
            shares_.append(share)
            #print share

        if not resume:
            break

    return shares_


def elevate_privilege(python_script):
    import win32api

    win32api.ShellExecute(0,  # parent window
                          "runas",  # need this to force UAC to act
                          "C:\\python27\\python.exe",
                          python_script,
                          "C:\\python27",  # base dir
                          1)  # window visibility - 1: visible, 0: backgroun


if __name__ == "__main__":

    print("is_windows() ", is_windows())
    print("is_unix() ", is_unix())

    if is_windows():
        print(get_appdata_path())

        print(GetClipboardText())

        print("get_drivers() ", get_drivers())


        #create_link("C:\Python27", get_desktop_path(), "Python directory")

