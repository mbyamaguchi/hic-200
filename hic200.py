import os
import click
from utils.make_bin_def2 import make_bin_def2_impl
from src.read_and_dump2 import read_and_dump2_impl
from src.dump_to_sort import dump_to_sort_impl


# ================================
# === exception ==================
# ================================


# ================================
# === main =======================
# ================================
@click.command()
@click.option("--tmpdir", type=str, default="./tmp")
@click.argument("site_file", required=True, type=click.Path(exists=True))
# @click.argument("binpath", required=True, type=click.Path(exists=True))
@click.argument("inputpath", required=True, type=click.Path(exists=True))
@click.argument("outputpath", required=True, type=click.Path(exists=False))
def main(tmpdir, site_file, inputpath, outputpath):
    if not os.path.isdir(tmpdir):
        print(f"directory {tmpdir} does not exists.")
        ans = input(f"proceed to make {tmpdir}? [y/N]")
        if ans not in {'Y', 'y'}:
            print("exit.")
            return
        os.makedirs(tmpdir)
    # default
    bindefpath = f"{tmpdir}/tmp_bindef.txt"
    make_bin_def2_impl(bin_size=200, chroms="I,II,III", site_file=site_file, output_bin_file=bindefpath)

    tmppairpath = f"{tmpdir}/tmp_pair.txt"
    read_and_dump2_impl(bin_file=bindefpath, max_distance=1_000_000,
                   input_gz=inputpath, output_file=tmppairpath)
    
    sortedpath = f"{tmpdir}/tmp_sorted.txt"
    dump_to_sort_impl(tmppairs=tmppairpath, output=outputpath,
                 sorted=sortedpath, sortmemory="1G", tmpdir=tmpdir)



if __name__ == '__main__':
    main()