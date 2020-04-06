#!/usr/bin/env python3
import os

from litex.data.software import compiler_rt

print("Found compiler_rt @ version", compiler_rt.version_str, "(with data", compiler_rt.data_version_str, ")")
print()
print("Data is in", compiler_rt.data_location)
assert os.path.exists(compiler_rt.data_location)
print("Data is version", compiler_rt.data_version_str, compiler_rt.data_git_hash)
print("-"*75)
print(compiler_rt.data_git_msg)
print("-"*75)
print()
print("It contains:")
for root, dirs, files in os.walk(compiler_rt.data_location):
    dirs.sort()
    for f in sorted(files):
        path = os.path.relpath(os.path.join(root, f), compiler_rt.data_location)
        print(" -", path)
