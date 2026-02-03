import subprocess

import typer


def run(img: str = None, bmp: str = None, size: str = None):
    subprocess.run(["magick", img, "-resize", size, "-colorspace",
                   "Gray", "-dither", "None", "-colors", "2", f"BMP3:{bmp}"])


if __name__ == "__main__":
    typer.run(run)
