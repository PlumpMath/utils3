"""
file:           Path.py
Description:    Python module to manipulate files/paths in easy and fast way.

Features:
        * Path concatenations with / slash operator      
        * Special Directory Access
            * Path.home() return a path object to the current user directory
            * Path.here   Returns a path to where the current app is running 
            * Path.pwd    Gets the current directory


TODO: Set the file to PEP8

"""
from __future__ import print_function

import os
import sys
import shutil
import errno
import time
import fnmatch
import inspect
from subprocess import Popen, PIPE

import zipfile
import tarfile
import hashlib


# Linux/UNIX Modules Only
import pwd
import grp

from .check import is_unix, is_windows, is_linux
from .hof import mapl, filterl

# Non Standard Library Module
try:
    import magic
except ImportError:
    print("Missing Module magic ." + __file__)

permissions = lambda x: "".join([["-", "r"][(x & 4) >> 2], ["-", "w"][(x & 2) >> 1], ["-", "x"][x & 1]])


class Path(object):
    """
    Python path DSL that adds syntax sugar features 
    for path manipulation.
    """

    def __init__(self, path=""):
        self.path = path

    @classmethod
    def here(cls):
        """
        Returns the absolute path to the script that calls this function
        """
        return Path(os.path.abspath(inspect.stack()[1][1]))

    @classmethod
    def pwd(cls):
        """
        Return the current directory
        """
        return Path(os.getcwd())

    #
    # @property
    # @staticmethod
    @classmethod
    def home(cls):
        """
        :return: Path("~") object pointing to home directory

        Example:

         >>> u.Path.home() / "Downloads"
         /home/tux/Downloads

         """
        return Path(os.path.expanduser("~"))

    @property
    def dir(self):
        """ Return Path directory """
        return Path(os.path.dirname(self.path))

    @property
    def name(self):

        return os.path.basename(self.path)

    @property
    def top(self):
        return Path(os.path.abspath(os.path.join(self.path, '..')))

    @property
    def ext(self):
        """Return file extension """
        return os.path.splitext(self.path)[1]

    @property
    def abs(self):
        """
        Returns the absolute path of object as a Path object
        """
        return Path(os.path.abspath(self.path))


    @property
    def magic(self):
        """Return file mime type"""

        return magic.from_file(self.path, mime=True)


    def cd(self):
        """Enter in the directory or the directory where is the file"""
        if self.is_dir():
            os.chdir(self.path)
        else:
            # The path points to a file
            os.chdir(self.dir.path)

    def uid(self):
        """ Get File/Directory User ID: Works on UNIX systems only """
        return os.stat(self.path).st_uid

    def gid(self):
        """ Get File/Directory Group ID: Works on UNIX systems only """
        return os.stat(self.path).st_gid

    def owner(self):
        """ Returns the user/Owner of the file / Works on UNIX only """

        return pwd.getpwuid(os.stat(self.path).st_uid)[0]

    def group(self):
        """ Returns the Group that access the file / Works on UNIX only"""
        return grp.getgrgid(os.stat(self.path).st_gid)[0]

    def chomodx(self):
        """Equivalent to chmod +x <file> """
        stat = os.stat(self.path).st_mode
        os.chmod(self.path, stat | 0o100)

    def perms(self, flag=False):
        """
        Return file permissions rwx format
            
            usr : User/Owner permissions
            grp : Group      Permissions
            oth : Others     Permissions
        
        x: Execute Permission
        r: Read    Permission
        w: Write   Permission        
        
        :return: [usr, grp, oth] 
        
        Note: Only works on UNIX
        """
        st_mode = os.stat(self.path).st_mode

        usr = st_mode >> 6 & 7
        grp = st_mode >> 3 & 7
        oth = st_mode & 7
        p = [usr, grp, oth]

        if not flag:
            return list(map(permissions, p))
        else:
            return p

    def show_permissions(self):
        """ Return file permissions/ Works only on UNIX OS"""
        usr, grp, oth = self.perms()
        print("Owner  :", permissions(usr))
        print("Group  :", permissions(grp))
        print("Others :", permissions(oth))


    def mtime(self, flag=True):
        """ 
        Return the most recent modification of the file 
        
        :param flag: If flag is True returns the mtime in Unix timestamp 
                      format, otherwise it returns in ISO 8601 format.
        :return:     Modification time in Unix Timestamp format or ISO 8601
        :rtype:  Flag(True) --> str (ISO 8601), Flag(False) --> int (Unix)
        """
        if flag:
            return time.ctime(os.stat(self.path).st_mtime)
        else:
            return os.stat(self.path).st_mtime

    def info(self):
        """
        Print File Information      
        """
        print("Path :", self)

        if is_unix():
            print("\nModification Time :", self.mtime())
            print("\n\nOwner: ", self.owner(), "- Uid: ", self.uid())
            print("Group: ", self.group(), "- Gid: ", self.gid())
            print("\nPermissions: {}{}{}".format(*self.perms(1)))
            print("\tOwner: {}\tGroup: {}\tOthers: {}".format(*self.perms()))

            print("\n\nSize: {} Megabytes".format(self.size() / 1024))

    def __str__(self):
        return self.path

    def __repr__(self):
        return self.path

    def list(self, abs=False):
        """
        :param abs: Flag, If true returns files with absolute path
        :param time: Flag. If true returns the files sorted by time creation.

        """

        if not abs:
            return os.listdir(self.path)
        else:
            return mapl(lambda x: os.path.join(self.path, x), os.listdir(self.path))


    def list_archive(self):
        """
        List the content of compressed file if
        self.path is pointing to a compressed
        file like *.zip or *.tar.gz, *.tar, *.tar.bz2
        """
        if self.is_zip():
            zf = zipfile.ZipFile(self.path, 'r')
            files = zf.namelist()
            zf.close()
            return files

        if self.is_tar():
            tar = tarfile.open(self.path)
            files = tar.getnames()
            tar.close()
            return files


    def walk(self, pattern="*"):
        """
        Return list of all subdirectories and 
        all files in subdirectories
        """

        filelist = []
        # dirlist  = []

        for root, dirs, files in os.walk(self.path):
            files_ = list(map(lambda x: os.path.join(root, x), files))
            list(map(filelist.append, files_))
            #dirs_ = list(map(lambda x: os.path.join(root, x), dirs))            
            #list(map(dirlist.append, dirs_))

        return fnmatch.filter(filelist, pattern)

    def walk_dirs(self, pattern="*"):
        """ Return all subdirectories of a directory"""

        dirlist = []

        for root, dirs, files in os.walk(self.path):
            dirs_ = mapl(lambda x: os.path.join(root, x), dirs)
            mapl(dirlist.append, dirs_)

        return fnmatch.filter(dirlist, pattern)


    def list_dirs(self, abs=False):
        dirs = filterl(os.path.isdir, self.list(True))

        if not abs:
            return mapl(os.path.basename, dirs)
        else:
            return dirs

    def list_files(self, abs=False):
        files = list(filter(os.path.isfile, self.list(True)))

        if not abs:
            return list(map(os.path.basename, files))
        else:
            return files


    def newest(self):
        """
        Returns the newest file in the directory.
        """
        if self.is_dir():
            return Path(max(self.list(True), key=lambda x: os.stat(x).st_mtime))
        else:
            return Path(max(self.dir.list(True), key=lambda x: os.stat(x).st_mtime))

    def __truediv__(self, other):

        if isinstance(other, Path):
            return Path(os.path.join(self.path, other.path))
        elif isinstance(other, str):
            return Path(os.path.join(self.path, other))
        else:
            raise Exception("Expected type: str or Path object")

    def __floordiv__(self, other):

        if isinstance(other, Path):
            return Path(os.path.relpath(self.path, other.path))
        elif isinstance(other, str):
            return Path(os.path.relpath(self.path, other))
        else:
            raise Exception("Expected type: str or Path object")


    def is_dir(self):
        return os.path.isdir(self.path)

    def is_file(self):
        return os.path.isfile(self.path)

    def is_link(self):
        return os.path.islink(self.path)

    def is_mount(self):
        return os.path.ismount(self.path)

    def is_zip(self):
        return zipfile.is_zipfile(self.path)

    def is_tar(self):
        return tarfile.is_tarfile(self.path)


    def exists(self):
        return os.path.exists(self.path)

    def mkdir(self):
        if not self.is_dir():
            os.mkdir(self.path)
            return True
        return False

    def __contains__(self, filename):
        """ if something in Path.home()  """
        return filename in self.list()
        # raise Exception("Not Implemented")

    def open(self, flags=None):
        """
        Open as a file
        """
        return open(self.path, flags)

    def read(self, filename=None):

        if self.is_file():
            return open(self.path).read()

        if filename is not None:

            if self.is_zip():

                import zipfile

                zf = zipfile.ZipFile(self.path)
                content = zf.read(filename)
                zf.close()
                return content

            elif self.is_dir():

                p = self / filename
                return p.read()

    def extract(self, path):
        if self.is_zip():
            zf = zipfile.ZipFile(self.path)
            zf.extractall(path=path)
            zf.close()

        if self.is_tar():
            tar = tarfile.open(self.path)
            tar.extractall(path)
            tar.close()

        return Path(path)


    def rm(self):
        try:
            if self.is_file():
                os.remove(self.path)
            elif self.is_dir():
                shutil.rmtree(self.path)
            return True
        except:
            return False


    def cp(self, dest):
        """
        Credits: http://www.pythoncentral.io/how-to-recursively-copy-a-directory-folder-in-python/?PageSpeed=noscript
        """
        src = self.path

        try:
            shutil.copytree(src, dest)
        except OSError as e:
            # If the error was caused because the source wasn't a directory
            if e.errno == errno.ENOTDIR:
                shutil.copy(src, dest)
            else:
                print('Directory not copied. Error: %s' % e)

        return Path(dest)

    def size(self):
        return os.path.getsize(self.path)


    def get(self, filename):
        return Path(os.path.join(self.path, filename))

    def mktgz(self, output_filename):
        """Compress directory to .tgz"""

        if not self.is_dir():
            raise Exception("Path must be a directory")

        with tarfile.open(output_filename, "w:gz") as tar:
            tar.add(self.path, arcname=os.path.basename(self.path))

    def md5(self):
        return hashlib.md5(self.path.encode('utf-8')).hexdigest()


    def link(self, dest):
        """
        Creates a Symbolic Link at dest
        path.
        
        :Warning: Only works on UNIX
        """
        os.symlink(self.path, dest)

    def addpath(self):
        """
        Add path to sys.path so you can import 
        any module or package in the self.path directory
        """
        sys.path.append(self.path)

    def execfile(self):
        """Execute Python Script"""
        exec(self.read())

    def execute(self):
        """
        Execute self.path, runs it as a command.

        """
        pid = Popen([self.path])
        return pid

    @classmethod
    def datafile(cls, filename=""):
        """
        Get file that is in the same package as
        the script.

        package/
            script.py
            data/
                resource1.txt
                resource2.txt

        resouce1 = Path.datafile("resource1.txt")

        """
        here = os.path.abspath(inspect.stack()[1][1])
        return Path(os.path.join(here, "data", filename))

    @classmethod
    def interpreter(cls):
        """
        Returns the path where is the Python interpreter

        :return: Path(sys.executable) object pointing to python executable
        :rtype:  Path
        """
        return Path(sys.executable)



