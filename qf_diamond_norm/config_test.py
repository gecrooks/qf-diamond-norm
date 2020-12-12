# Copyright 2019-2021, Gavin E. Crooks and contributors
#
# This source code is licensed under the Apache License 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.

import glob
import io
import subprocess

import qf_diamond_norm as pkg


def test_version() -> None:
    assert pkg.__version__


def test_about() -> None:
    out = io.StringIO()
    pkg.about(out)
    print(out)


def test_about_main() -> None:
    rval = subprocess.call(["python", "-m", f"{pkg.__name__}.about"])
    assert rval == 0


def test_copyright() -> None:
    """Check that source code files contain a copyright line"""
    exclude = set([f"{pkg.__name__}/version.py"])
    for fname in glob.glob(f"{pkg.__name__}/**/*.py", recursive=True):
        if fname in exclude:
            continue
        print("Checking " + fname + " for copyright header")

        with open(fname) as f:
            for line in f.readlines():
                if not line.strip():
                    continue
                assert line.startswith("# Copyright")
                break
