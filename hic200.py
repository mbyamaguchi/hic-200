import click
import gzip
from pathlib import Path
from utils.make_bin_def2 import make_bin_def2
from src.read_and_dump2 import read_and_dump2
from src.dump_to_sort import dump_to_sort

# ================================
# === exception ==================
# ================================


# ================================
# === main =======================
# ================================
@click.command()
@click.option("--tmpdir", type=str, default="./tmp")
@click.argument("site_file", required=True, type=click.Path(exists=True))
@click.argument("binpath", required=True, type=click.Path(exists=True))
@click.argument("inputpath", required=True, type=click.Path(exists=True))
@click.argument("outputpath", required=True, type=click.Path)
def main(tmpdir, site_file, binpath, inputpath, outputpath):
    # default
    bindefpath = f"{tmpdir}/tmp_bindef.txt"
    make_bin_def2(binsize=200, chroms="I,II,III",
                  site_file=site_file, output_bin_file=bindefpath)

    tmppairpath = f"{tmpdir}/tmp_pair.txt"
    read_and_dump2(bin_file=bindefpath, max_distance=1_000_000,
                   input_gz=inputpath, output_file=tmppairpath)
    
    sortedpath = f"{tmpdir}/tmp_sorted.txt"
    dump_to_sort(tmppairs=tmppairpath, output=outputpath,
                 sorted=sortedpath)



if __name__ == '__main__':
    main()