'''
    This module provides utilities to get the absolute filenames so that we can be sure that:
        - The case of a file will match the actual file in the filesystem (otherwise breakpoints won't be hit).
        - Providing means for the user to make path conversions when doing a remote debugging session in
          one machine and debugging in another.
'''

import os.path

os_normcase = os.path.normcase
basename = os.path.basename
join = os.path.join
rPath = os.path.realpath  # @UndefinedVariable
normcase = os_normcase  # May be rebound on set_ide_os

# caches filled as requested during the debug session
NORM_PATHS_CONTAINER = {}
NORM_PATHS_AND_BASE_CONTAINER = {}


# Returns tuple of absolute path and real path for given filename
def _norm_paths(filename):
    try:
        return NORM_PATHS_CONTAINER[filename]
    except KeyError:
        abs_path = _norm_path(filename, os.path.abspath)
        real_path = _norm_path(filename, rPath)

        NORM_PATHS_CONTAINER[filename] = abs_path, real_path
        return abs_path, real_path


def _norm_path(filename, normpath):
    r = normpath(filename)
    # cache it for fast access later
    ind = r.find('.zip')
    if ind == -1:
        ind = r.find('.egg')
    if ind != -1:
        ind += 4
        zip_path = r[:ind]
        if r[ind] == "!":
            ind += 1
        inner_path = r[ind:]
        if inner_path.startswith('/') or inner_path.startswith('\\'):
            inner_path = inner_path[1:]
        r = join(normcase(zip_path), inner_path)
    else:
        r = normcase(r)
    return r


# For given file f returns tuple of its absolute path, real path and base name
def get_abs_path_real_path_and_base_from_file(f):
    try:
        return NORM_PATHS_AND_BASE_CONTAINER[f]
    except:
        abs_path, real_path = _norm_paths(f)
        base = basename(real_path)
        ret = abs_path, real_path, base
        NORM_PATHS_AND_BASE_CONTAINER[f] = ret
        return ret


def get_abs_path_real_path_and_base_from_frame(frame):
    try:
        return NORM_PATHS_AND_BASE_CONTAINER[frame.f_code.co_filename]
    except:
        # This one is just internal (so, does not need any kind of client-server translation)
        f = frame.f_code.co_filename
        if f is not None and f.startswith(('build/bdist.', 'build\\bdist.')):
            # files from eggs in Python 2.7 have paths like build/bdist.linux-x86_64/egg/<path-inside-egg>
            f = frame.f_globals['__file__']
        if f is not None and f.endswith('.pyc'):
            f = f[:-1]
        ret = get_abs_path_real_path_and_base_from_file(f)
        # Also cache based on the frame.f_code.co_filename (if we had it inside build/bdist it can make a difference).
        NORM_PATHS_AND_BASE_CONTAINER[frame.f_code.co_filename] = ret
        return ret
