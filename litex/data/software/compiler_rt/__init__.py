import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "data")
src = "https://git.llvm.org/git/compiler-rt.git/"
git_hash = "81fb4f00c2cfe13814765968e09931ffa93b5138"
git_describe = "v0.0-6140-g81fb4f00c"
version_str = "0.0.post6140"
version_tuple = (0, 0)
try:
    from packaging.version import Version as V
    pversion = V("0.0.post6140")
except ImportError:
    pass
