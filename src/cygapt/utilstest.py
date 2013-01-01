"""
"""

import unittest
import os
import tempfile

class TestCase(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self._var_tmpdir = tempfile.mkdtemp()
        self._var_old_cwd = os.getcwd()
        os.chdir(self._var_tmpdir)
        self._var_exename = "cyg-apt"
        self._var_mirror = "http://cygwin.xl-mirror.nl/"
        self._var_old_env = os.environ
        
        # unix tree
        self._dir_mtroot = self._var_tmpdir + "/"
        self._dir_tmp = os.path.join(self._dir_mtroot, "tmp")
        self._dir_prefix = os.path.join(self._dir_mtroot, "usr")
        self._dir_sysconf = os.path.join(self._dir_mtroot, "etc")
        self._dir_localstate = os.path.join(self._dir_mtroot, "var")
        self._dir_home = os.path.join(self._dir_mtroot, "home")
        self._dir_libexec = os.path.join(self._dir_prefix, "lib")
        self._dir_data = os.path.join(self._dir_prefix, "share")
        self._dir_man = os.path.join(self._dir_data, "man")
        self._dir_info = os.path.join(self._dir_data, "info")
        # bulld unix tree
        os.mkdir(self._dir_tmp)
        os.mkdir(self._dir_prefix)
        os.mkdir(self._dir_sysconf)
        os.mkdir(self._dir_localstate)
        os.mkdir(self._dir_home)
        os.mkdir(self._dir_libexec)
        os.mkdir(self._dir_data)
        os.mkdir(self._dir_man)
        os.mkdir(self._dir_info)
        
        # exe tree
        self._dir_confsetup = os.path.join(self._dir_sysconf, "setup")
        self._dir_user = os.path.join(self._dir_home, "user")
        self._dir_execache = os.path.join(self._dir_localstate, "cache",
                                          self._var_exename)
        self._dir_exedata = os.path.join(self._dir_data, self._var_exename)
        # build exe tree
        os.mkdir(self._dir_confsetup)
        os.mkdir(self._dir_user)
        os.makedirs(self._dir_execache)
        os.mkdir(self._dir_exedata)
        
        # exe files
        self._file_cygwin_sig   = os.path.join(self._dir_exedata,
                                               "cygwin.sig")
        self._file_installed_db = os.path.join(self._dir_confsetup,
                                               "installed.db")
        self._file_setup_ini    = os.path.join(self._dir_confsetup,
                                               "setup.ini")
        self._file_setup_rc     = os.path.join(self._dir_confsetup,
                                               "setup.rc")
        self._file_user_config  = os.path.join(self._dir_user,
                                               "." + self._var_exename)
        
        open(self._file_setup_rc, "wb").write(r"""
last-cache
{2}{0}
mirrors-lst
{2}http://mirrors.163.com/cygwin/;mirrors.163.com;Asia;China
{2}http://cygwin.mirrors.hoobly.com/;cygwin.mirrors.hoobly.com;United States;Pennsylvania
{2}http://cygwin.xl-mirror.nl/;cygwin.xl-mirror.nl;Europe;Netherlands
new-cygwin-version
{2}1
avahi
{2}1
mDNSResponder
{2}1
chooser_window_settings
{2}44,2,3,4294935296,4294935296,4294967295,4294967295,371,316,909,709
last-mirror
{2}{1}
net-method
{2}Direct
last-action
{2}Download,Install
""".format(self._dir_execache, self._var_mirror, "\t"))
                
        os.environ['TMP'] = self._dir_tmp
        os.environ['HOME'] = self._dir_user
        
        self._var_setupIni = SetupIniProvider()

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        
        os.environ = self._var_old_env
        os.chdir(self._var_old_cwd)
        def rmtree(path):
            files = os.listdir(path)
            for filename in files:
                subpath = os.path.join(path, filename)
                if os.path.isdir(subpath):
                    rmtree(subpath)
                else:
                    os.remove(subpath)
            os.rmdir(path)
        rmtree(self._var_tmpdir)
        
class SetupIniProvider():
    """Create a fictif setup.ini"""
    def __init__(self):
        self.pkg = PackageIni()
        
        self.contents = r"""
# This file is automatically generated.  If you edit it, your
# edits will be discarded next time the file is generated.
# See http://cygwin.com/setup.html for details.
#
setup-timestamp: 1356999079
setup-version: 2.774

{pkg}
""".format(pkg=self.pkg.ini_contents)
        
        self.dists = DistNameStruct()
        self.dists.curr = {self.pkg.name: self.pkg.dists.curr.__dict__}
        self.dists.prev = {self.pkg.name: self.pkg.dists.prev.__dict__}
        self.dists.test = {self.pkg.name: self.pkg.dists.test.__dict__}

class PackageIni():
    def __init__(self, pkgid="A"):
        self.name = ""
        self.category = ""
        self.shortDesc = ""
        self.longDesc = ""
        self.requires = ""
        self.install = DistNameStruct()
        self.source = DistNameStruct()
        self.version = DistNameStruct()
        self.ini_contents = ""
        self.dists = DistsStruct()
        
        self._build(pkgid)
        
    def _build(self, pkgid="A"):
        self.name = "pkg" + pkgid
        self.category = "cat" + pkgid
        self.shortDesc = "\"Short description for " + pkgid + "\""
        self.longDesc = "\"Long description\nfor " + pkgid + "\""
        self.requires = "reqpkg" + pkgid
        
        self.version.prev = "1.0.1-1"
        self.version.curr = "2.0.1-1"
        self.version.test = "3.0.1-1"
        
        for distname in self.install.__dict__:
            self.install.__dict__[distname] = "path/to/pkg/" + \
                            self.name + \
                            "-"+ \
                            self.version.__dict__[distname] + \
                            ".tar.bz2" + \
                            " 1024 hashmd5"
        
        for distname in self.source.__dict__:
            self.source.__dict__[distname] = "path/to/pkg/" + \
                            self.name + \
                            "-"+ \
                            self.version.__dict__[distname] + \
                            ".src.tar.bz2" + \
                            " 1024 hashmd5"
        
        self.ini_contents = r"""@ {name}
sdesc: {sdesc}
ldesc: {ldesc}
category: {category}
requires: {requires}
version: {curr_version}
install: {curr_install}
source: {curr_source}
[prev]
version: {prev_version}
install: {prev_install}
source: {prev_source}
[test]
version: {test_version}
install: {test_install}
source: {test_source}""".format(name=self.name,
                                sdesc=self.shortDesc,
                                ldesc=self.longDesc,
                                category=self.category,
                                requires=self.requires,
                                curr_version=self.version.curr,
                                prev_version=self.version.prev,
                                test_version=self.version.test,
                                curr_install=self.install.curr,
                                prev_install=self.install.prev,
                                test_install=self.install.test,
                                curr_source=self.source.curr,
                                prev_source=self.source.prev,
                                test_source=self.source.test)
        
        for distname in self.dists.__dict__:
            self.dists.__dict__[distname].category = self.category
            self.dists.__dict__[distname].ldesc = self.longDesc
            self.dists.__dict__[distname].sdesc = self.shortDesc
            self.dists.__dict__[distname].requires = self.requires
        
        for distname in self.dists.__dict__:
            self.dists.__dict__[distname].version = self.version.__dict__[distname]
        for distname in self.dists.__dict__:
            self.dists.__dict__[distname].install = self.install.__dict__[distname]
        for distname in self.dists.__dict__:
            self.dists.__dict__[distname].source = self.source.__dict__[distname]

class DistNameStruct():
    def __init__(self):
        self.curr = None
        self.prev = None
        self.test = None

class DistStruct():
    def __init__(self):
        self.category = None
        self.sdesc = None
        self.ldesc = None
        self.requires = None
        self.version = None
        self.install = None
        self.source = None
        
class DistsStruct(DistNameStruct):
    def __init__(self):
        self.curr = DistStruct()
        self.prev = DistStruct()
        self.test = DistStruct()
        