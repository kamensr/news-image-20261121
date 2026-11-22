"""Entry point for make.fun news-image-20261121.

Copies the poster (entry.png, shipped in this repository) to the output
directory the harness names in MAKEFUN_OUTPUT_DIR. Standard library only,
no network, fully deterministic: every run writes the same bytes.
"""

import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
