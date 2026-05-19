import gzip
import click

def load_bin_metadata(bin_file):
    """
    bin definition
    bin chr start end
    1 I 0 199
    2 I 200 399
    """

    chr_meta = {}

    with open(bin_file) as f:
        # header = next(f)
        _ = next(f)

        for line in f:
            line = line.strip()
            if not line:
                continue

            bin_id, chrom, start, end = line.split()

            bin_id = int(bin_id)
            start = int(start)
            end = int(end)

            if chrom not in chr_meta:
                chr_meta[chrom] = {
                    "first_bin": bin_id,
                    "last_end": end,
                }
            else:
                if end > chr_meta[chrom]["last_end"]:
                    chr_meta[chrom]["last_end"] = end
    return chr_meta


def midpoint(start, end):
    return (start + end) // 2

def midpoint_to_bin(chrom, mid, chr_meta):
    meta = chr_meta[chrom]

    if mid > meta["last_end"]:
        return None
    
    local_index = mid // 200
    return meta["first_bin"] + local_index

@click.command()
@click.option(
    "--bin",
    "bin_file",
    required=True,
    type=click.Path(exists=True),
    help="Bin definition file"
)
@click.option(
    "--max-distance",
    default=1_000_000,
    show_default=True,
    type=int,
    help="Maximum cis genomic distance"
)
@click.argument(
    "input_gz",
    type=click.Path(exists=True)
)
@click.argument(
    "output_file",
    type=click.Path()
)
def main(bin_file, max_distance, input_gz, output_file):
    chr_meta = load_bin_metadata(bin_file)

    valid_chr = {"I", "II", "III"}

    with gzip.open(input_gz, "rt") as fin, open(output_file, "w") as fout:
        fout.write("bin1\tbin2\tscore\n")

        # header = next(fin)
        _ = next(fin)

        for line_num, line in enumerate(fin, start=2):
            line = line.strip()
            if not line:
                continue

            fields = line.split()

            if len(fields) < 9:
                continue

            chrom1 = fields[0]
            start1 = int(fields[1])
            end1 = int(fields[2])

            chrom2 = fields[4]
            start2 = int(fields[5])
            end2 = int(fields[6])

            score = fields[8]

            if chrom1 != chrom2:
                continue

            mid1 = midpoint(start1, end1)
            mid2 = midpoint(start2, end2)

            if abs(mid1 - mid2) > max_distance:
                continue

            bin1 = midpoint_to_bin(chrom1, mid1, chr_meta)
            bin2 = midpoint_to_bin(chrom2, mid2, chr_meta)

            if bin1 is None or bin2 is None:
                bin1, bin2 = bin2, bin1
            
            fout.write(f"{bin1}\t{bin2}\t{score}\n")

if __name__ == "__main__":
    main()