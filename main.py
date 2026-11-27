"""Entry point for the 26 November 2026 news poster.

The artwork already sits beside this file as entry.png, rendered by
render.py. Running this module simply delivers that picture to the
directory the platform names in MAKEFUN_OUTPUT_DIR, falling back to
/output when the variable is absent. Standard library only.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def deliver():
    if not os.path.isfile(SOURCE):
        raise SystemExit("entry.png is missing beside main.py; run render.py first")
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, "entry.png")
    shutil.copyfile(SOURCE, target)
    return target


if __name__ == "__main__":
    placed = deliver()
    print("entry.png delivered to", placed, "-", os.path.getsize(placed), "bytes")
