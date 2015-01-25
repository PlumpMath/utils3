import sys
import os

from io import StringIO
import re


#-----------------------------#
#  OPERATING SYSTEM FUNCTIONS #
#-----------------------------#



def execute(commands, nowait=False):
    """
    Execute shell command and get output
    """
    from subprocess import Popen, PIPE


    if type(commands) == list:
        commands = " ".join(commands)

    p = Popen(commands, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)

    if not nowait:
        out, err = p.communicate()
        out = out.decode("utf-8")
        err = err.decode("utf-8")

        return out, err
    else:
        return None


def mkdir(path):
    if not os.path.isdir(path):
        os.mkdir(path)


def get_hostname():
    import platform;

    return platform.uname()[1]


def set_proc_name(newname):
    if not is_linux():
        return
    from ctypes import cdll, byref, create_string_buffer

    libc = cdll.LoadLibrary('libc.so.6')  #Loading a 3rd party library C
    buff = create_string_buffer(len(newname) + 1)  #Note: One larger than the name (man prctl says that)
    buff.value = newname  #Null terminated string as it should be
    libc.prctl(15, byref(buff), 0, 0,
               0)  #Refer to "#define" of "/usr/include/linux/prctl.h" for the misterious value 16 & arg[3..5] are zero as the man page says.

    # from ctypes import cdll, byref, create_string_buffer
    # libc = cdll.LoadLibrary('libc.so.6')
    # buff = create_string_buffer(len(newname)+1)
    # buff.value = newname
    # libc.prctl(15, byref(buff), 0, 0, 0)


def get_proc_name():
    """
    Get Process Name.
    Only works on Linux
    """
    if not is_linux():
        return

    from ctypes import cdll, byref, create_string_buffer

    libc = cdll.LoadLibrary('libc.so.6')
    buff = create_string_buffer(128)
    # 16 == PR_GET_NAME from <linux/prctl.h>
    libc.prctl(16, byref(buff), 0, 0, 0)
    return buff.value


#---------------------------------------#
#       USER NOTIFICATION               #
#---------------------------------------#


def notify(summary, body='', app_name='', app_icon='',
           timeout=5000, actions=[], hints=[], replaces_id=0):
    import dbus

    """
    System notification message:

    Example:
    notify("Touchpad Disabled")
    """
    _bus_name = 'org.freedesktop.Notifications'
    _object_path = '/org/freedesktop/Notifications'
    _interface_name = _bus_name

    session_bus = dbus.SessionBus()
    obj = session_bus.get_object(_bus_name, _object_path)
    interface = dbus.Interface(obj, _interface_name)
    interface.Notify(app_name, replaces_id, app_icon,
                     summary, body, actions, hints, timeout)


def msgbox_error(msg, title="gtkBuilder Selector"):
    import gtk

    dlg = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE)
    dlg.set_title(title)
    dlg.set_markup(msg)
    dlg.run()
    dlg.destroy()


def msgbox_ok(msg, title):
    import gtk

    dlg = gtk.MessageDialog(type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK)
    dlg.set_title(title)
    dlg.set_markup(msg)
    dlg.run()
    dlg.destroy()


def msgbox_info(msg, title="INFO"):
    import gtk

    parent = None
    md = gtk.MessageDialog(parent, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, gtk.BUTTONS_CLOSE,
                           "Download completed")
    md.set_title(title)
    md.run()
    md.destroy()


def msgbox_question(question, title="Question"):
    import gtk

    dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL,
                               gtk.MESSAGE_INFO, gtk.BUTTONS_YES_NO,
                               question)
    dialog.set_title(title)
    response = dialog.run()
    dialog.destroy()

    if response == gtk.RESPONSE_YES:
        return True
    else:
        return False


def get_external_ip():
    import urllib.request, urllib.parse, urllib.error
    import re

    site = urllib.request.urlopen("http://checkip.dyndns.org/").read()
    grab = re.findall('([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', site)
    address = grab[0]
    return address


def get_tinyurl(url):
    """
    Get Compressed URL
    """
    import urllib.request, urllib.parse, urllib.error

    tpl = "http://tinyurl.com/api-create.php?url={url}"
    url_ = tpl.format(url=url)
    tinyurl = urllib.request.urlopen(url_).read()
    return tinyurl



def xclip():
    """
    Run clipboard command
    :return:
    """
    if platform.startswith("linux"):
        output = execute("xclip -selection clipboard -o")
    else:
        raise Exception("Not implemented yet to this platform")

    return output[0]



def exec_output(code, namespace={}):
    """
    Execute code in __main__
    global dictionary (namespace)
    and return output.

    """

    buffer = StringIO()
    sys.stdout = buffer
    exec(code, namespace)
    sys.stdout = sys.__stdout__

    return buffer.getvalue()


def run_example(code):
    import inspect

    _globals = inspect.currentframe().f_back.f_globals

    lines = code.splitlines()
    #_code = joinstr(lines, '\n>>> ')
    #print _code

    for line in lines:
        if line.startswith('#'):
            print('\n' + line[1:])
        else:
            printc("{g}>>> ", line)
            #if EXECUTE_STEP: raw_input(">> Enter to RETURN to continue")

            output = exec_output(line, _globals)
            if output:
                printc("{r}", output)


def run_block(code):
    import inspect

    _globals = inspect.currentframe().f_back.f_globals
    _code = joinstr(code.splitlines(), '\n>>> ')

    printc("{g}", _code)
    output = exec_output(code, _globals)
    printc("{r}", output)


def paste_run():
    #import re
    #from utils import xclip
    txt = xclip()
    txt = txt.strip('\n').strip('\r')



    # Replace bad character
    txt = txt.replace(r'’', "'").replace(r'‘', "'").replace(r'′', "'").replace(r'−', '-')

    # Remove lines non starting with >>>
    lines = [x for x in txt.splitlines() if x.startswith(">>>")]

    # Remove >>> from beginning of lines
    lines = [x.split(">>>")[1].strip() for x in lines]


    #print "\n".join(lines)

    #nextxt = "\n".join(lines)
    #exec(nextxt)

    #print "----------------"

    for line in lines:

        print(">>> ", line)

        if not line:
            continue

        if re.match(".*=.*", line) or re.match("^from.*import", line) or re.match("^import", line):
            exec(line)
        else:
            print(eval(line))
