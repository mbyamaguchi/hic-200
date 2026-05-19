from pathlib import Path
import math
import click

@click.command()
@click.argument("path", type=str)
@click.argument("outputpath", type=str)
@click.option("--resolution", default=200, type=int)
@click.option("--nchroms", default=3, type=int)
def make_bin_def(path: Path, outputpath: Path, resolution=200, nchroms=3) -> None:

    print(f"the file {outputpath} exists.")
    prompt = input("overwrite? [y/N]")
    if not (prompt == 'y' or prompt == 'Y'):
        return

    chroms = []
    with open(path, mode='rt', encoding="utf-8") as f:
        for _ in range(nchroms):
            _, nread = f.readline().rstrip().split()
            # print(nread)
            chroms.append(int(nread))

        # print(chroms)

    bins_chroms = []
    for i in range(nchroms):
        bins_chroms.append(math.floor(chroms[i] / resolution) + 1)
    
    mapping = {
        0: 'I',
        1: 'II',
        2: 'III',
    }

    with open(outputpath, mode='wt', encoding="utf-8") as f:
        header = "bin\tchrom\tstart\tend\tbinsize\n"
        f.write(header)
        bin_start = 0
        for binn in range(bins_chroms[0]):
            bin_end = min(bin_start + resolution - 1, chroms[0] - 1)
            binsize = bin_end - bin_start + 1
            line = f'{binn+1}\tI\t{bin_start}\t{bin_end}\t{binsize}\n'
            f.write(line)
            bin_start += resolution
        bin_start = chroms[0]
        for chrom in range(1, nchroms):
            for binn in range(sum(bins_chroms[0:chrom]), sum(bins_chroms[0:chrom+1])):
                bin_end = min(bin_start + resolution - 1, sum(chroms[0:chrom+1]) - 1)
                binsize = bin_end - bin_start + 1
                line = f'{binn+1}\t{mapping[chrom]}\t{bin_start}\t{bin_end}\t{binsize}\n'
                f.write(line)
                bin_start += resolution
                bin_start = min(bin_start, sum(chroms[0:chrom+1]) - 1)
            bin_start = sum(chroms[0:chrom+1])

if __name__ == "__main__":
    make_bin_def()
