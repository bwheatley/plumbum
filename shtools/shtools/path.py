import os


class Path(object):
    def __init__(self, *paths):
        self._path = os.path.abspath(os.path.join(*(str(p) for p in paths)))
        self.basename = os.path.basename(self._path)
        self.dirname = os.path.dirname(self._path)
    def __str__(self):
        return self._path
    def __repr__(self):
        return "<Path %r>" % (self._path,)
    def __div__(self, other):
        return Path(self, other)
    def __iter__(self):
        return iter(self.list())
    def __eq__(self, other):
        return self._path == str(other)
    def __ne__(self, other):
        return self._path != str(other)
    def __hash__(self):
        return hash(self._path)

    def up(self):
        return Path(self.dirname)
    def list(self): #@ReservedAssignment
        return [self / fn for fn in os.listdir(self._path)]
    def traverse(self, filter = lambda p: True): #@ReservedAssignment
        for p in self:
            if filter(p):
                yield p
            if p.isdir() and filter(p):
                for p2 in p.walk():
                    yield p2
    def isdir(self):
        return os.path.isdir(self._path)
    def isfile(self):
        return os.path.isfile(self._path)
    def exists(self):
        return os.path.exists(self._path)
    def stat(self):
        return os.stat(self._path)

# copy, move rename, delete, open

#def copy(self, dst, override = False):
#    dst = dst if isinstance(dst, Path) else Path(str(dst))
#    if override:
#        Path(dst).remove()
#    if self.isdir():
#        shutil.copytree(self.path, str(dst))
#    else:
#        shutil.copy2(self.path, str(dst))
#    return dst
#def move(self, dst):
#    shutil.move(self.path, str(dst))
#    return dst if isinstance(dst, Path) else Path(str(dst))
#def rename(self, newname):
#    """Renames the last element in the path. 
#    Example::
#    
#        >>> p = Path("/foo/bar/spam.txt")
#        >>> p2 = p.rename("bacon.txt")
#        >>> p2 == "/foo/bar/bacon.txt"
#        True
#    """
#    return self.move(Path(self.dirname, newname))
#def remove(self):
#    """removes the given path, if it exists; if this path is a directory, removes recursively"""
#    if not self.exists():
#        return
#    if self.isdir():
#        shutil.rmtree(self.path)
#    else:
#        os.remove(self.path)
#def mkdir(self):
#    """make a directory on this path (including all needed intermediate directories), if this
#    path doesn't already exist"""
#    if not self.exists():
#        os.makedirs(self.path)
#
#def open(self, fn, *args):
#    """opens a file at this path"""
#    return open(str(self / fn), *args)


class SshPath(object):
    def __init__(self, session, path):
        self._session = session
        self._path = path
    def list(self):
        return self._session.execute("\\ls").splitlines()


class Multimethod(object):
    def __init__(self, name):
        self.name = name
        self._overloads = {}
    def __repr__(self):
        return "Multimethod(%r)" % (self.name,)
    def overload(self, *args):
        def overloader(func):
            self._overloads[args] = func
            return self
        return overloader
    def __call__(self, *args):
        sig = tuple(type(a) for a in args)
        if sig not in self._overloads:
            raise TypeError("%r cannot apply to %s" % (self, sig))
        return self._overloads[self](*args)


def multimethod(*args):
    def deco(func):
        mm = Multimethod(func.__name__)
        mm.overload(*args)(func)
        return mm
    return deco

@multimethod(str, str)
def copy(src, dst, override = True):
    if override:
        Path(dst).remove()
    if src.isdir():
        shutil.copytree(src, dst)
    else:
        shutil.copy2(src, dst)
    return dst

@copy.overload(Path, Path)
def copy(src, dst):
    copy(str(src), str(dst))
    return dst

@copy.overload(Path, str)
def copy(src, dst):
    copy(str(src), str(dst))
    return Path(dst)

@copy.overload(str, Path)
def copy(src, dst):
    copy(str(src), str(dst))
    return Path(dst)

















