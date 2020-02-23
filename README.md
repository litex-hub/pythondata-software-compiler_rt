# litex-data-software-compiler_rt

Non-Python data files required to use the compiler_rt with
[LiteX](https://github.com/enjoy-digital/litex.git).

The data files can be found under the Python module `litex.data.software.compiler_rt`. The
`litex.data.software.compiler_rt.location` value can be used to find the files on the file system.
For example;

```python
import litex.data.software.compiler_rt

my_data_file = "abc.txt"

with open(os.path.join(litex.data.software.compiler_rt.location, my_data_file)) as f:
    print(f.read())
```

The data files come from https://git.llvm.org/git/compiler-rt.git/
and are imported using `git subtrees` to the directory
[litex/data/software/compiler_rt/data](litex/data/software/compiler_rt/data].

## Installing

## Manually

You can install the package manually, however this is **not** recommended.

```
git clone https://github.com/litex-hub/litex-data-software-compiler_rt.git
cd litex-data-software-compiler_rt
sudo python setup.py install
```

## Using [pip](https://pip.pypa.io/)

You can use [pip](https://pip.pypa.io/) to install the data package directly
from github using;

```
pip install --user git+https://github.com/litex-hub/litex-data-software-compiler_rt.git
```

If you want to install for the whole system rather than just the current user,
you need to remove the `--user` argument and run as sudo like so;

```
sudo pip install git+https://github.com/litex-hub/litex-data-software-compiler_rt.git
```

You can install a specific revision of the repository using;
```
pip install --user git+https://github.com/litex-hub/litex-data-software-compiler_rt.git@<tag>
pip install --user git+https://github.com/litex-hub/litex-data-software-compiler_rt.git@<branch>
pip install --user git+https://github.com/litex-hub/litex-data-software-compiler_rt.git@<hash>
```

### With `requirements.txt` file

Add to your Python `requirements.txt` file using;
```
-e git+https://github.com/litex-hub/litex-data-software-compiler_rt.git
```

To use a specific revision of the repository, use the following;
```
-e https://github.com/litex-hub/litex-data-software-compiler_rt.git@<hash>
```