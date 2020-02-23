#!/usr/bin/env python3
import os

from litex.data.software import compiler_rt

print("Found compiler_rt @ version", compiler_rt.version_str, "("+compiler_rt.git_hash+")")
print("Data is in", compiler_rt.data_location)
assert os.path.exists(compiler_rt.data_location)
print("It contains:\n -", end=" ")
print("\n - ".join(os.listdir(compiler_rt.data_location)))