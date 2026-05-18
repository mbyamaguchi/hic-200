import click
import gzip
from pathlib import Path

# ================================
# === exception ==================
# ================================
class FileNotSpecified(Exception):
    pass



# ================================
# === main =======================
# ================================
@click.command()
@click.option("--binpath", "-b", default=None, help="bin configuration file")
@click.argument("inputpath")
@click.argument("outputpath")
def main(binpath, inputpath, outputpath):
    if binpath is None:
        raise FileNotSpecified("bin file not specified.")
    pass

if __name__ == '__main__':
    main()