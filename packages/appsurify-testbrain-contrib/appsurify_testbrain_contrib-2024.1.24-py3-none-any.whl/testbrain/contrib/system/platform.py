import collections
import itertools
import os as _os
import re
import sys

_ver_stages = {
    # any string not found in this dict, will get 0 assigned
    "dev": 10,
    "alpha": 20,
    "a": 20,
    "beta": 30,
    "b": 30,
    "c": 40,
    "RC": 50,
    "rc": 50,
    # number, will get 100 assigned
    "pl": 200,
    "p": 200,
}

_component_re = re.compile(r"([0-9]+|[._+-])")


def _comparable_version(version):  # noqa
    result = []
    for v in _component_re.split(version):
        if v not in "._+-":
            try:
                v = int(v, 10)
                t = 100
            except ValueError:
                t = _ver_stages.get(v, 0)
            result.extend((t, v))
    return result


_NOT_FOUND = object()


class CachedProperty:
    def __init__(self, func):
        self.func = func
        self.attrname = None
        self.__doc__ = func.__doc__

    def __set_name__(self, owner, name):
        if self.attrname is None:
            self.attrname = name
        elif name != self.attrname:
            raise TypeError(
                f"Cannot assign the same cached_property "
                f"to two different names ({self.attrname!r} and {name!r})."
            )

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        if self.attrname is None:
            raise TypeError(
                "Cannot use cached_property instance "
                "without calling __set_name__ on it."
            )
        try:
            cache = instance.__dict__
        except (
            AttributeError
        ):  # not all objects have __dict__ (e.g. class defines slots)
            msg = (
                f"No '__dict__' attribute on {type(instance).__name__!r} "
                f"instance to cache {self.attrname!r} property."
            )
            raise TypeError(msg)
        val = cache.get(self.attrname, _NOT_FOUND)
        if val is _NOT_FOUND:
            val = self.func(instance)
            try:
                cache[self.attrname] = val
            except TypeError:
                msg = (
                    f"The '__dict__' attribute on {type(instance).__name__!r} "
                    f"instance does not support item assignment "
                    f"for caching {self.attrname!r} property."
                )
                raise TypeError(msg)
        return val

    __class_getitem__ = classmethod(object)


cached_property = CachedProperty

# Platform specific APIs

_libc_search = re.compile(
    b"(__libc_init)"
    b"|"
    b"(GLIBC_([0-9.]+))"
    b"|"
    rb"(libc(_\w+)?\.so(?:\.(\d[0-9.]*))?)"
)


def libc_ver(executable=None, lib="", version="", chunksize=16384):
    """Tries to determine the libc version that the file executable
    (which defaults to the Python interpreter) is linked against.

    Returns a tuple of strings (lib,version) which default to the
    given parameters in case the lookup fails.

    Note that the function has intimate knowledge of how different
    libc versions add symbols to the executable and thus is probably
    only usable for executables compiled using gcc.

    The file is read and scanned in chunks of chunksize bytes.

    """
    if not executable:
        try:
            ver = _os.confstr("CS_GNU_LIBC_VERSION")
            # parse 'glibc 2.28' as ('glibc', '2.28')
            parts = ver.split(maxsplit=1)
            if len(parts) == 2:
                return tuple(parts)
        except (AttributeError, ValueError, OSError):
            # _os.confstr() or CS_GNU_LIBC_VERSION value not available
            pass

        executable = sys.executable

        if not executable:
            # sys.executable is not set.
            return lib, version

    v = _comparable_version
    # We use _os.path.realpath()
    # here to work around problems with Cygwin not being
    # able to open symlinks for reading
    executable = _os.path.realpath(executable)
    with open(executable, "rb") as f:
        binary = f.read(chunksize)
        pos = 0
        while pos < len(binary):
            if b"libc" in binary or b"GLIBC" in binary:
                m = _libc_search.search(binary, pos)
            else:
                m = None
            if not m or m.end() == len(binary):
                chunk = f.read(chunksize)
                if chunk:
                    binary = binary[max(pos, len(binary) - 1000) :] + chunk  # noqa
                    pos = 0
                    continue
                if not m:
                    break
            libcinit, glibc, glibcversion, so, threads, soversion = [
                s.decode("latin1") if s is not None else s for s in m.groups()
            ]
            if libcinit and not lib:
                lib = "libc"
            elif glibc:
                if lib != "glibc":
                    lib = "glibc"
                    version = glibcversion
                elif v(glibcversion) > v(version):
                    version = glibcversion
            elif so:
                if lib != "glibc":
                    lib = "libc"
                    if soversion and (not version or v(soversion) > v(version)):
                        version = soversion
                    if threads and version[-len(threads) :] != threads:  # noqa
                        version = version + threads
            pos = m.end()
    return lib, version


def _norm_version(version, build=""):  # noqa
    """Normalize the version and build strings and return a single
    version string using the format major.minor.build (or patchlevel).
    """
    l: list = version.split(".")  # noqa :E741
    if build:
        l.append(build)
    try:
        strings = list(map(str, map(int, l)))
    except ValueError:
        strings = l
    version = ".".join(strings[:3])  # noqa
    return version


_ver_output = re.compile(r"(?:([\w ]+) ([\w.]+) " r".*" r"\[.* ([\d.]+)\])")  # noqa

# Examples of VER command output:
#
#   Windows 2000:  Microsoft Windows 2000 [Version 5.00.2195]
#   Windows XP:    Microsoft Windows XP [Version 5.1.2600]
#   Windows Vista: Microsoft Windows [Version 6.0.6002]
#
# Note that the "Version" string gets localized on different
# Windows versions.


def _syscmd_ver(
    system="",  # noqa
    release="",  # noqa
    version="",  # noqa
    supported_platforms=("win32", "win16", "dos"),
):
    """Tries to figure out the OS version used and returns
    a tuple (system, release, version).

    It uses the "ver" shell command for this which is known
    to exists on Windows, DOS. XXX Others too ?

    In case this fails, the given parameters are used as
    defaults.

    """
    if sys.platform not in supported_platforms:
        return system, release, version

    # Try some common cmd strings
    import subprocess

    info = ""

    for cmd in ("ver", "command /c ver", "cmd /c ver"):
        try:
            info = subprocess.check_output(
                cmd,
                stdin=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                text=True,
                shell=True,
            )
        except (OSError, subprocess.CalledProcessError):
            continue
        else:
            break
    else:
        return system, release, version

    # Parse the output
    info = info.strip()  # noqa
    m = _ver_output.match(info)
    if m is not None:
        system, release, version = m.groups()
        # Strip trailing dots from version and release
        if release[-1] == ".":
            release = release[:-1]
        if version[-1] == ".":
            version = version[:-1]
        # Normalize the version and build strings (eliminating additional
        # zeros)
        version = _norm_version(version)
    return system, release, version


_WIN32_CLIENT_RELEASES = {
    (5, 0): "2000",
    (5, 1): "XP",
    # Strictly, 5.2 client is XP 64-bit, but platform.py historically
    # has always called it 2003 Server
    (5, 2): "2003Server",
    (5, None): "post2003",
    (6, 0): "Vista",
    (6, 1): "7",
    (6, 2): "8",
    (6, 3): "8.1",
    (6, None): "post8.1",
    (10, 0): "10",
    (10, None): "post10",
}

# Server release name lookup will default to client names if necessary
_WIN32_SERVER_RELEASES = {
    (5, 2): "2003Server",
    (6, 0): "2008Server",
    (6, 1): "2008ServerR2",
    (6, 2): "2012Server",
    (6, 3): "2012ServerR2",
    (6, None): "post2012ServerR2",
}


def win32_is_iot():
    return win32_edition() in (
        "IoTUAP",
        "NanoServer",
        "WindowsCoreHeadless",
        "IoTEdgeOS",
    )


def win32_edition():
    try:
        try:
            import winreg
        except ImportError:
            import _winreg as winreg
    except ImportError:
        pass
    else:
        try:
            cvkey = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion"
            with winreg.OpenKeyEx(winreg.HKEY_LOCAL_MACHINE, cvkey) as key:
                return winreg.QueryValueEx(key, "EditionId")[0]
        except OSError:
            pass

    return None


def win32_ver(release="", version="", csd="", ptype=""):
    try:
        from sys import getwindowsversion
    except ImportError:
        return release, version, csd, ptype

    winver = getwindowsversion()
    try:
        major, minor, build = map(int, _syscmd_ver()[2].split("."))
    except ValueError:
        major, minor, build = winver.platform_version or winver[:3]
    version = f"{major}.{minor}.{build}"

    release = (
        _WIN32_CLIENT_RELEASES.get((major, minor))
        or _WIN32_CLIENT_RELEASES.get((major, None))
        or release
    )

    # getwindowsversion() reflect the compatibility mode Python is
    # running under, and so the service pack value is only going to be
    # valid if the versions match.
    if winver[:2] == (major, minor):
        try:
            csd = f"SP{winver.service_pack_major}"
        except AttributeError:
            if csd[:13] == "Service Pack ":
                csd = "SP" + csd[13:]

    # VER_NT_SERVER = 3
    if getattr(winver, "product_type", None) == 3:
        release = (
            _WIN32_SERVER_RELEASES.get((major, minor))
            or _WIN32_SERVER_RELEASES.get((major, None))
            or release
        )

    try:
        try:
            import winreg
        except ImportError:
            import _winreg as winreg
    except ImportError:
        pass
    else:
        try:
            cvkey = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion"
            with winreg.OpenKeyEx(winreg.HKEY_LOCAL_MACHINE, cvkey) as key:
                ptype = winreg.QueryValueEx(key, "CurrentType")[0]
        except OSError:
            pass

    return release, version, csd, ptype


def _mac_ver_xml():
    fn = "/System/Library/CoreServices/SystemVersion.plist"
    if not _os.path.exists(fn):
        return None

    try:
        import plistlib
    except ImportError:
        return None

    with open(fn, "rb") as f:
        pl = plistlib.load(f)
    release = pl["ProductVersion"]
    versioninfo = ("", "", "")
    machine = _os.uname().machine
    if machine in ("ppc", "Power Macintosh"):
        # Canonical name
        machine = "PowerPC"

    return release, versioninfo, machine


def mac_ver(release="", versioninfo=("", "", ""), machine=""):
    """Get macOS version information and return it as tuple (release,
    versioninfo, machine) with versioninfo being a tuple (version,
    dev_stage, non_release_version).

    Entries which cannot be determined are set to the parameter values
    which default to ''. All tuple entries are strings.
    """

    # First try reading the information from an XML file which should
    # always be present
    info = _mac_ver_xml()
    if info is not None:
        return info

    # If that also doesn't work return the default values
    return release, versioninfo, machine


def _java_getprop(name, default):
    from java.lang import System  # noqa

    try:
        value = System.getProperty(name)
        if value is None:
            return default
        return value
    except AttributeError:
        return default


def java_ver(release="", vendor="", vminfo=("", "", ""), osinfo=("", "", "")):
    """Version interface for Jython.

    Returns a tuple (release, vendor, vminfo, osinfo) with vminfo being
    a tuple (vm_name, vm_release, vm_vendor) and osinfo being a
    tuple (os_name, os_version, os_arch).

    Values which cannot be determined are set to the defaults
    given as parameters (which all default to '').

    """
    # Import the needed APIs
    try:
        import java.lang
    except ImportError:
        return release, vendor, vminfo, osinfo

    vendor = _java_getprop("java.vendor", vendor)
    release = _java_getprop("java.version", release)
    vm_name, vm_release, vm_vendor = vminfo
    vm_name = _java_getprop("java.vm.name", vm_name)
    vm_vendor = _java_getprop("java.vm.vendor", vm_vendor)
    vm_release = _java_getprop("java.vm.version", vm_release)
    vminfo = vm_name, vm_release, vm_vendor
    os_name, os_version, os_arch = osinfo
    os_arch = _java_getprop("java.os.arch", os_arch)
    os_name = _java_getprop("java.os.name", os_name)
    os_version = _java_getprop("java.os.version", os_version)
    osinfo = os_name, os_version, os_arch

    return release, vendor, vminfo, osinfo


# System name aliasing


def system_alias(system, release, version):
    """Returns (system, release, version) aliased to common
    marketing names used for some systems.

    It also does some reordering of the information in some cases
    where it would otherwise cause confusion.

    """
    if system == "SunOS":
        # Sun's OS
        if release < "5":
            # These releases use the old name SunOS
            return system, release, version
        # Modify release (marketing release = SunOS release - 3)
        l: list = release.split(".")  # noqa :E741
        if l:
            try:
                major = int(l[0])
            except ValueError:
                pass
            else:
                major = major - 3
                l[0] = str(major)
                release = ".".join(l)
        if release < "6":
            system = "Solaris"
        else:
            # XXX Whatever the new SunOS marketing name is...
            system = "Solaris"

    elif system in ("win32", "win16"):
        # In case one of the other tricks
        system = "Windows"

    # bpo-35516: Don't replace Darwin with macOS since input release and
    # version arguments can be different than the currently running version.

    return system, release, version


# Various internal helpers


def _platform(*args):
    """Helper to format the platform string in a filename
    compatible format e.g. "system-version-machine".
    """
    # Format the platform string
    platform = "-".join(x.strip() for x in filter(len, args))

    # Cleanup some possible filename obstacles...
    platform = platform.replace(" ", "_")
    platform = platform.replace("/", "-")
    platform = platform.replace("\\", "-")
    platform = platform.replace(":", "-")
    platform = platform.replace(";", "-")
    platform = platform.replace('"', "-")
    platform = platform.replace("(", "-")
    platform = platform.replace(")", "-")

    # No need to report 'unknown' information...
    platform = platform.replace("unknown", "")

    # Fold '--'s and remove trailing '-'
    while 1:
        cleaned = platform.replace("--", "-")
        if cleaned == platform:
            break
        platform = cleaned
    while platform[-1] == "-":
        platform = platform[:-1]

    return platform


def _node(default=""):
    """Helper to determine the node name of this machine."""
    try:
        import socket
    except ImportError:
        # No sockets...
        return default
    try:
        return socket.gethostname()
    except OSError:
        # Still not working...
        return default


def _follow_symlinks(filepath):
    """In case filepath is a symlink, follow it until a
    real file is reached.
    """
    filepath = _os.path.abspath(filepath)
    while _os.path.islink(filepath):
        filepath = _os.path.normpath(
            _os.path.join(_os.path.dirname(filepath), _os.readlink(filepath))
        )
    return filepath


def _syscmd_file(target, default=""):
    """Interface to the system's file command.

    The function uses the -b option of the file command to have it
    omit the filename in its output. Follow the symlinks. It returns
    default in case the command should fail.

    """
    if sys.platform in ("dos", "win32", "win16"):
        # XXX Others too ?
        return default

    try:
        import subprocess
    except ImportError:
        return default
    target = _follow_symlinks(target)
    # "file" output is locale dependent: force the usage of the C locale
    # to get deterministic behavior.
    env = dict(_os.environ, LC_ALL="C")
    try:
        # -b: do not prepend filenames to output lines (brief mode)
        output = subprocess.check_output(
            ["file", "-b", target], stderr=subprocess.DEVNULL, env=env
        )
    except (OSError, subprocess.CalledProcessError):
        return default
    if not output:
        return default
    # With the C locale, the output should be mostly ASCII-compatible.
    # Decode from Latin-1 to prevent Unicode decode error.
    return output.decode("latin-1")


# Information about the used architecture

# Default values for architecture; non-empty strings override the
# defaults given as parameters
_default_architecture = {
    "win32": ("", "WindowsPE"),
    "win16": ("", "Windows"),
    "dos": ("", "MSDOS"),
}


def architecture(executable=sys.executable, bits="", linkage=""):
    """Queries the given executable (defaults to the Python interpreter
    binary) for various architecture information.

    Returns a tuple (bits, linkage) which contains information about
    the bit architecture and the linkage format used for the
    executable. Both values are returned as strings.

    Values that cannot be determined are returned as given by the
    parameter presets. If bits is given as '', the sizeof(pointer)
    (or sizeof(long) on Python version < 1.5.2) is used as
    indicator for the supported pointer size.

    The function relies on the system's "file" command to do the
    actual work. This is available on most if not all Unix
    platforms. On some non-Unix platforms where the "file" command
    does not exist and the executable is set to the Python interpreter
    binary defaults from _default_architecture are used.

    """
    # Use the sizeof(pointer) as default number of bits if nothing
    # else is given as default.
    if not bits:
        import struct

        size = struct.calcsize("P")
        bits = str(size * 8) + "bit"

    # Get data from the 'file' system command
    if executable:
        fileout = _syscmd_file(executable, "")
    else:
        fileout = ""

    if not fileout and executable == sys.executable:
        if sys.platform in _default_architecture:
            bits, linkage = _default_architecture[sys.platform]
        return bits, linkage

    if "executable" not in fileout and "shared object" not in fileout:
        # Format not supported
        return bits, linkage

    # Bits
    if "32-bit" in fileout:
        bits = "32bit"
    elif "64-bit" in fileout:
        bits = "64bit"

    # Linkage
    if "ELF" in fileout:
        linkage = "ELF"
    elif "PE" in fileout:
        # E.g. Windows uses this format
        if "Windows" in fileout:
            linkage = "WindowsPE"
        else:
            linkage = "PE"
    elif "COFF" in fileout:
        linkage = "COFF"
    elif "MS-DOS" in fileout:
        linkage = "MSDOS"
    else:
        # XXX the A.OUT format also falls under this class...
        pass

    return bits, linkage


def _get_machine_win32():
    # WOW64 processes mask the native architecture
    return _os.environ.get("PROCESSOR_ARCHITEW6432", "") or _os.environ.get(
        "PROCESSOR_ARCHITECTURE", ""
    )


class _Processor(object):
    def __init__(self):
        ...

    @classmethod
    def get(cls):
        func = getattr(cls, f"get_{sys.platform}", cls.from_subprocess)
        return func() or ""

    @staticmethod
    def get_win32():
        return _os.environ.get("PROCESSOR_IDENTIFIER", _get_machine_win32())

    @staticmethod
    def get_open_vms():
        try:
            import vms_lib
        except ImportError:
            pass
        else:
            csid, cpu_number = vms_lib.getsyi("SYI$_CPU", 0)
            return "Alpha" if cpu_number >= 128 else "VAX"

    @staticmethod
    def from_subprocess():
        """
        Fall back to `uname -p`
        """
        try:
            import subprocess
        except ImportError:
            return None
        try:
            return subprocess.check_output(
                ["uname", "-p"],
                stderr=subprocess.DEVNULL,
                text=True,
            ).strip()
        except (OSError, subprocess.CalledProcessError):
            pass


def _unknown_as_blank(val):
    return "" if val == "unknown" else val


# Portable uname() interface

field_names = "os version system release node machine"


class UnameResult(collections.namedtuple("uname_result_base", field_names)):
    """
    A uname_result that's largely compatible with a
    simple namedtuple except that 'processor' is
    resolved late and cached to avoid calling "uname"
    except when needed.
    """

    _fields = ("os", "version", "system", "release", "node", "machine", "processor")

    # "macOS, 14.0, Darwin, 23.0.0, localhost, x86_64, i386"
    # "Windows, 10.0.22621, Windows, 10, localhost, AMD64, Intel64"
    # "Ubuntu, 22.04, Linux, 5.15.0-40-generic, localhost, x86_64"
    # Ubuntu-22.04-Linux-5.15.0-40-generic-x86_64-i386-64bit
    @CachedProperty
    def processor(self):
        _processor = _Processor.get()
        return _unknown_as_blank(str(_processor))

    def __iter__(self):
        return itertools.chain(super().__iter__(), (self.processor,))

    @classmethod
    def _make(cls, iterable):
        # override factory to affect length check
        num_fields = len(cls._fields) - 1
        result = cls.__new__(cls, *iterable)
        if len(result) != num_fields + 1:
            msg = f"Expected {num_fields} arguments, got {len(result)}"
            raise TypeError(msg)
        return result

    def __getitem__(self, key):
        return tuple(self)[key]

    def __len__(self):
        return len(tuple(iter(self)))

    def __reduce__(self):
        return UnameResult, tuple(self)[: len(self._fields) - 1]


uname_result = UnameResult
_uname_cache = None


def uname():
    """Fairly portable uname interface. Returns a tuple
    of strings (system, node, release, version, machine, processor)
    identifying the underlying platform.

    Note that unlike the os.uname function this also returns
    possible processor information as an additional tuple entry.

    Entries which cannot be determined are set to ''.

    """
    global _uname_cache

    if _uname_cache is not None:
        return _uname_cache

    os = ""  # noqa
    # Get some infos from the builtin _os.uname API...
    try:
        system, node, release, version, machine = infos = _os.uname()
    except AttributeError:
        system = sys.platform
        node = _node()
        release = version = machine = ""
        infos = ()

    os = system

    if not any(infos):
        # uname is not available

        # Try win32_ver() on win32 platforms
        if system == "win32":
            release, version, csd, ptype = win32_ver()
            machine = machine or _get_machine_win32()

        # Try the 'ver' system command available on some
        # platforms
        if not (release and version):
            system, release, version = _syscmd_ver(system)
            # Normalize system to what win32_ver() normally returns
            # (_syscmd_ver() tends to return the vendor name as well)
            if system == "Microsoft Windows":
                system = "Windows"
            elif system == "Microsoft" and release == "Windows":
                # Under Windows Vista and Windows Server 2008,
                # Microsoft changed the output of the ver command. The
                # release is no longer printed.  This causes the
                # system and release to be misidentified.
                system = "Windows"
                if "6.0" == version[:3]:
                    release = "Vista"
                else:
                    release = ""

        # In case we still don't know anything useful, we'll try to
        # help ourselves
        if system in ("win32", "win16"):
            if not version:
                if system == "win32":
                    version = "32bit"
                else:
                    version = "16bit"
            system = "Windows"

        elif system[:4] == "java":
            release, vendor, vminfo, osinfo = java_ver()
            system = "Java"
            version = ", ".join(vminfo)
            if not version:
                version = vendor

    # System specific extensions
    if system == "OpenVMS":
        # OpenVMS seems to have release and version mixed up
        if not release or release == "0":
            release = version
            version = ""

    # normalize name
    if system == "Microsoft" and release == "Windows":
        system = "Windows"
        release = "Vista"

    # Reformat info
    if system == "Darwin":
        # macOS (darwin kernel)
        macos_release = mac_ver()[0]
        if macos_release:
            os = "macOS"
            version = macos_release

    elif system == "Windows":
        # MS platforms
        rel, vers, csd, ptype = win32_ver(version)
        os, version, release = system, rel, vers

    elif system in ("Linux",):
        os_release = linux_os_release()
        os = os_release.get("NAME", "Linux").split(" ", 1)[0]
        version = os_release.get("VERSION_ID", release)

    elif system == "Java":
        # Java platforms
        r, v, vminfo, _ = java_ver()
        os = vminfo[0].split(",", 1)[0]
        version = r
    else:
        # bits, linkage = architecture(sys.executable)
        ...

    vals = os, version, system, release, node, machine
    # Replace 'unknown' values with the more portable ''
    _uname_cache = UnameResult(*map(_unknown_as_blank, vals))
    return _uname_cache


# Direct interfaces to some of the uname() return values


def os():
    """Returns the system/OS name, e.g. 'Linux', 'Windows' or 'Java'.

    An empty string is returned if the value cannot be determined.

    """
    return uname().os


def system():
    """Returns the system/OS name, e.g. 'Linux', 'Windows' or 'Java'.

    An empty string is returned if the value cannot be determined.

    """
    return uname().system


def node():
    """Returns the computer's network name (which may not be fully
    qualified)

    An empty string is returned if the value cannot be determined.

    """
    return uname().node


def release():
    """Returns the system's release, e.g. '2.2.0' or 'NT'

    An empty string is returned if the value cannot be determined.

    """
    return uname().release


def version():
    """Returns the system's release version, e.g. '#3 on degas'

    An empty string is returned if the value cannot be determined.

    """
    return uname().version


def machine():
    """Returns the machine type, e.g. 'i386'

    An empty string is returned if the value cannot be determined.

    """
    return uname().machine


def processor():
    """Returns the (true) processor name, e.g. 'amdk6'

    An empty string is returned if the value cannot be
    determined. Note that many platforms do not provide this
    information or simply return the same value as for machine(),
    e.g.  NetBSD does this.

    """
    return uname().processor


# Various APIs for extracting information from sys.version

_sys_version_parser = re.compile(
    r"([\w.+]+)\s*"  # "version<space>"
    r"\(#?([^,]+)"  # "(#buildno"
    r"(?:,\s*([\w ]*)"  # ", builddate"
    r"(?:,\s*([\w :]*))?)?\)\s*"  # ", buildtime)<space>"
    r"\[([^\]]+)\]?"
)  # "[compiler]"

_ironpython_sys_version_parser = re.compile(
    r"IronPython\s*" r"([\d\.]+)" r"(?: \(([\d\.]+)\))?" r" on (.NET [\d\.]+)"
)

# IronPython covering 2.6 and 2.7
_ironpython26_sys_version_parser = re.compile(
    r"([\d.]+)\s*"
    r"\(IronPython\s*"
    r"[\d.]+\s*"
    r"\(([\d.]+)\) on ([\w.]+ [\d.]+(?: \(\d+-bit\))?)\)"
)

_pypy_sys_version_parser = re.compile(
    r"([\w.+]+)\s*" r"\(#?([^,]+),\s*([\w ]+),\s*([\w :]+)\)\s*" r"\[PyPy [^\]]+\]?"
)

_sys_version_cache = {}


def _sys_version(sys_version=None):
    """Returns a parsed version of Python's sys.version as tuple
    (name, version, branch, revision, build_no, build_date, compiler)
    referring to the Python implementation name, version, branch,
    revision, build number, build date/time as string and the compiler
    identification string.

    Note that unlike the Python sys.version, the returned value
    for the Python version will always include the patchlevel (it
    defaults to '.0').

    The function returns empty strings for tuple entries that
    cannot be determined.

    sys_version may be given to parse an alternative version
    string, e.g. if the version was read from a different Python
    interpreter.

    """
    # Get the Python version
    if sys_version is None:
        sys_version = sys.version

    # Try the cache first
    result = _sys_version_cache.get(sys_version, None)
    if result is not None:
        return result

    # Parse it
    if "IronPython" in sys_version:
        # IronPython
        name = "IronPython"
        if sys_version.startswith("IronPython"):
            match = _ironpython_sys_version_parser.match(sys_version)
        else:
            match = _ironpython26_sys_version_parser.match(sys_version)

        if match is None:
            raise ValueError(f"failed to parse IronPython sys.version: {sys_version!r}")

        version, alt_version, compiler = match.groups()
        build_no = ""
        build_date = ""

    elif sys.platform.startswith("java"):
        # Jython
        name = "Jython"
        match = _sys_version_parser.match(sys_version)
        if match is None:
            raise ValueError(f"failed to parse Jython sys.version: {sys_version!r}")
        version, build_no, build_date, build_time, _ = match.groups()
        if build_date is None:
            build_date = ""
        compiler = sys.platform

    elif "PyPy" in sys_version:
        # PyPy
        name = "PyPy"
        match = _pypy_sys_version_parser.match(sys_version)
        if match is None:
            raise ValueError(f"failed to parse PyPy sys.version: {sys_version!r}")
        version, build_no, build_date, build_time = match.groups()
        compiler = ""

    else:
        # CPython
        match = _sys_version_parser.match(sys_version)
        if match is None:
            raise ValueError(r"failed to parse CPython sys.version: {sys_version!r}")
        version, build_no, build_date, build_time, compiler = match.groups()
        name = "CPython"
        if build_date is None:
            build_date = ""
        elif build_time:
            build_date = build_date + " " + build_time

    if hasattr(sys, "_git"):
        _, branch, revision = sys._git  # noqa
    elif hasattr(sys, "_mercurial"):
        _, branch, revision = sys._mercurial  # noqa
    else:
        branch = ""
        revision = ""

    # Add the patch level version if missing
    l: list = version.split(".")  # noqa :E741
    if len(l) == 2:
        l.append("0")
        version = ".".join(l)

    # Build and cache the result
    result = (name, version, branch, revision, build_no, build_date, compiler)
    _sys_version_cache[sys_version] = result
    return result


def python_implementation():
    """Returns a string identifying the Python implementation.

    Currently, the following implementations are identified:
      'CPython' (C implementation of Python),
      'IronPython' (.NET implementation of Python),
      'Jython' (Java implementation of Python),
      'PyPy' (Python implementation of Python).

    """
    return _sys_version()[0]


def python_version():
    """Returns the Python version as string 'major.minor.patchlevel'

    Note that unlike the Python sys.version, the returned value
    will always include the patchlevel (it defaults to 0).

    """
    return _sys_version()[1]


def python_version_tuple():
    """Returns the Python version as tuple (major, minor, patchlevel)
    of strings.

    Note that unlike the Python sys.version, the returned value
    will always include the patchlevel (it defaults to 0).

    """
    return tuple(_sys_version()[1].split("."))


def python_branch():
    """Returns a string identifying the Python implementation
    branch.

    For CPython this is the SCM branch from which the
    Python binary was built.

    If not available, an empty string is returned.

    """

    return _sys_version()[2]


def python_revision():
    """Returns a string identifying the Python implementation
    revision.

    For CPython this is the SCM revision from which the
    Python binary was built.

    If not available, an empty string is returned.

    """
    return _sys_version()[3]


def python_build():
    """Returns a tuple (buildno, builddate) stating the Python
    build number and date as strings.

    """
    return _sys_version()[4:6]


def python_compiler():
    """Returns a string identifying the compiler used for compiling
    Python.

    """
    return _sys_version()[6]


# The Opus Magnum of platform strings :-)

_platform_cache = {}


def platform(aliased=0, terse=0):
    """Returns a single string identifying the underlying platform
    with as much useful information as possible (but no more :).

    The output is intended to be human readable rather than
    machine parseable. It may look different on different
    platforms and this is intended.

    If "aliased" is true, the function will use aliases for
    various platforms that report system names which differ from
    their common names, e.g. SunOS will be reported as
    Solaris. The system_alias() function is used to implement
    this.

    Setting terse to true causes the function to return only the
    absolute minimum information needed to identify the platform.

    """
    result = _platform_cache.get((aliased, terse), None)
    if result is not None:
        return result

    # Get uname information and then apply platform specific cosmetics
    # to it...
    os, version, system, release, node, machine, processor = uname()

    if machine == processor:
        processor = ""

    if aliased:
        system, release, version = system_alias(system, release, version)

    if system == "Windows":
        # MS platforms
        rel, vers, csd, ptype = win32_ver(version)
        if terse:
            platform = _platform(system, version, machine)
        else:
            bits, linkage = architecture(sys.executable)
            platform = _platform(system, version, release, csd, machine, linkage, bits)

    elif system in ("Linux",):
        # check for libc vs. glibc
        libcname, libcversion = libc_ver()
        platform = _platform(
            os,
            version,
            system,
            release,
            machine,
            processor,
            "with",
            libcname + libcversion,
        )
    elif system == "Java":
        # Java platforms
        r, v, vminfo, (os_name, os_version, os_arch) = java_ver()
        if terse or not os_name:
            platform = _platform(system, release, version)
        else:
            platform = _platform(
                system, release, version, "on", os_name, os_version, os_arch
            )

    else:
        # Generic handler
        if terse:
            platform = _platform(os, version, system, release)
        else:
            bits, linkage = architecture(sys.executable)
            platform = _platform(
                os, version, system, release, machine, processor, bits, linkage
            )

    _platform_cache[(aliased, terse)] = platform
    return platform


# freedesktop.org os-release standard
# https://www.freedesktop.org/software/systemd/man/os-release.html

# NAME=value with optional quotes (' or "). The regular expression is less
# strict than shell lexer, but that's ok.
_os_release_line = re.compile(
    "^(?P<name>[a-zA-Z0-9_]+)=(?P<quote>[\"']?)(?P<value>.*)(?P=quote)$"
)
# unescape five special characters mentioned in the standard
_os_release_unescape = re.compile(r"\\([\\\$\"\'`])")
# /etc takes precedence over /usr/lib
_os_release_candidates = ("/etc/os-release", "/usr/lib/os-release")
_os_release_cache = None


def _parse_os_release(lines):
    # These fields are mandatory fields with well-known defaults
    # in practice all Linux distributions override NAME, ID, and PRETTY_NAME.
    info = {
        "NAME": "Linux",
        "ID": "linux",
        "PRETTY_NAME": "Linux",
    }

    for line in lines:
        mo = _os_release_line.match(line)
        if mo is not None:
            info[mo.group("name")] = _os_release_unescape.sub(r"\1", mo.group("value"))

    return info


def linux_os_release():
    """Return operation system identification from freedesktop.org os-release"""
    global _os_release_cache

    if _os_release_cache is None:
        for candidate in _os_release_candidates:
            try:
                with open(candidate, encoding="utf-8") as f:
                    _os_release_cache = _parse_os_release(f)
                break
            except OSError:
                pass
        else:
            pass

    return _os_release_cache.copy()


# FLAGS
SYSTEM = system()
IS_MACOS = SYSTEM == "Darwin"
IS_WINDOWS = SYSTEM == "Windows"
IS_LINUX = SYSTEM == "Linux"

PY_VERSION = python_version()

PY_VERSION_MAJOR = sys.version_info[0]
IS_PY2 = PY_VERSION_MAJOR == 2
IS_PY3 = PY_VERSION_MAJOR == 3


PY_COMPILER_TUPLE = str(python_compiler()).split(" ", 2)
PY_COMPILER_NAME = PY_COMPILER_TUPLE[0]
PY_COMPILER_VERSION = PY_COMPILER_TUPLE[1]

_PY_COMPILER = python_compiler().lower().replace(" ", "-")

PY_PLATFORM = f"PY-{PY_VERSION}-{_PY_COMPILER}"

OS_PLATFORM = (
    f"{os()}"
    f"-{version()}"
    f"-{system()}"
    f"-{release()}"
    f"-{processor()}"
    f"-{machine()}"
)


# Command line interface
if __name__ == "__main__":
    # Default is to print the aliased verbose platform string
    terse = "terse" in sys.argv or "--terse" in sys.argv
    aliased = "nonaliased" not in sys.argv and "--nonaliased" not in sys.argv
    print(platform(aliased, terse))
    sys.exit(0)
