import gzip
from pathlib import Path
import math
from typing import Dict

def find_bin_offset_by_chrom(binpath: Path) -> Dict:
    with open(binpath, mode='rt', encoding="utf-8") as f:
        # dict to store bin offset
        # bin offset starts from 1, hence 1-base
        bin_offset = {}
        bin_offset['I'] = 1

        # skip header
        f.readline()

        chroms = ['I', 'II', 'III']

        chrom = 0
        present_chrom = chroms[chrom]
        for line in f:
            lineelems = line.rstrip().split()
            if lineelems[1] != present_chrom:
                # print("[log] present chromosome:", present_chrom)
                # print("[log] bin_offset:", lineelems[0])
                chrom += 1
                if chrom >= len(chroms):
                    break
                present_chrom = chroms[chrom]
                bin_offset[present_chrom] = int(lineelems[0])
                
        return bin_offset


def read_and_dump(path: Path, binpath: Path, outpath: Path, resolution: int, readlimit: int=1000000) -> None:

    chr_offset = find_bin_offset_by_chrom(binpath)

    with gzip.open(path, mode='rt', encoding="utf-8") as fi, open(outpath, mode='wt', encoding="utf-8") as fo:
        fo.write("bin1\tbin2\tscore\n")
        fi.readline()
        for line in fi:
            lineelems = line.rstrip().split()
            chr1, chr2 = lineelems[0], lineelems[4]
            [start1, end1, fragNum1] = list(map(int, lineelems[1:4]))
            [start2, end2, fragNum2, score] = list(map(int, lineelems[5:]))
            
            # if inter-chromosomal, continue (skip) it
            if chr1 != chr2:
                continue
            
            # if chromosome is neither 1 nor 2 nor 3,
            # continue
            if chr1 not in {'I', 'II', 'III'}:
                continue

            # calculate midpoint: position of the fragment
            midpoint1 = math.floor((start1 + end1) / 2)
            midpoint2 = math.floor((start2 + end2) / 2)

            # find local bin index (not global)
            # local bin idx starts from `0`
            local_bin_idx1 = math.floor(midpoint1 / resolution)
            local_bin_idx2 = math.floor(midpoint2 / resolution)

            print("[log] local_bin_idx1:", local_bin_idx1)
            print("[log] local_bin_idx2:", local_bin_idx2)

            global_bin_idx1 = local_bin_idx1 + chr_offset[chr1]
            global_bin_idx2 = local_bin_idx2 + chr_offset[chr2]

            print("[log] global_bin_idx1:", global_bin_idx1)
            print("[log] global_bin_idx1:", global_bin_idx1)

            return

            if (global_bin_idx1 <= global_bin_idx2) \
                and ((global_bin_idx2 - global_bin_idx1) >= readlimit) \
                and score != 0:
                writeln = f"{global_bin_idx1}\t{global_bin_idx2}\t{score}\n"
                fo.write(writeln)