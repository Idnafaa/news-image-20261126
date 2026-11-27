"""Deliver the 26 November 2026 news poster to the platform.

render.py has already produced entry.png next to this file. This
module only copies that picture into the directory named by the
MAKEFUN_OUTPUT_DIR environment variable (default /output), so the
platform can pick it up. It uses nothing outside the standard
library.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def deliver():
    if not os.path.isfile(SOURCE):
        raise SystemExit("entry.png not found beside main.py - run render.py first")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, target)
    if os.path.getsize(target) != os.path.getsize(SOURCE):
        raise SystemExit("copied entry.png is incomplete - sizes differ")
    return target


if __name__ == "__main__":
    placed = deliver()
    print("entry.png delivered to", placed, "-", os.path.getsize(placed), "bytes")
