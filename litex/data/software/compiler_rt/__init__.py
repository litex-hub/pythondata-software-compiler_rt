import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "data")
src = "https://git.llvm.org/git/compiler-rt.git/"
git_hash = "1dd2eb5ffc3a86c9d38ec6beaef179f00460be70"
git_describe = "v0.0-11908-g1dd2eb5ff"
version_str = "0.0.post11908"
version_tuple = (0, 0)
try:
    from packaging.version import Version as V
    pversion = V("0.0.post11908")
except ImportError:
    pass