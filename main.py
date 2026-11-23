"""Copy the drawn page for Monday 23 November 2026 to $MAKEFUN_OUTPUT_DIR/entry.png (default /output).

The page itself is drawn by tools/build.py; this entry point only ships it.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(os.path.join(HERE, "assets", "entry.png"), os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
