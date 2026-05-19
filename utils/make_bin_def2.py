import click

def read_chromosome_length(site_file, target_chroms):
    """
    Input format:
    #number chr position    length_before   length_after
    1   III   0 0   17

    chromosome length is inferred as:
        max(position + length_after)
    """

    chrom_lengths = {}

    with open(site_file) as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            if line.startswith("#"):
                continue

            fields = line.split()

            if len(fields) < 5:
                continue

            _, chrom, position, _, length_after = fields[:5]

            if chrom not in target_chroms:
                continue

            position = int(position)
            length_after = int(length_after)

            chrom_end = position + length_after

            if chrom not in chrom_lengths:
                chrom_lengths[chrom] = chrom_end
            else:
                chrom_lengths[chrom] = max(chrom_lengths[chrom], chrom_end)

    return chrom_lengths

@click.command()
@click.option(
    "--bin-size",
    default=200,
    show_default=True,
    type=int,
    help="Bin size in bp."
)
@click.option(
    "--chroms",
    default="I,II,III",
    show_default=True,
    help="Comma-separated chromosome names to include."
)
@click.argument(
    "site_file",
    type=click.Path(exists=True)
)
@click.argument(
    "output_bin_file",
    type=click.Path()
)
def main(bin_size, chroms, site_file, output_bin_file):
    target_chroms = chroms.split(",")

    chrom_lengths = read_chromosome_length(
        site_file,
        set(target_chroms)
    )

    missing = [chrom for chrom in target_chroms if chrom not in chrom_lengths]

    if missing:
        raise click.ClickException(
            f"Chromosome(s) not found in site file: {', '.join(missing)}"
        )
    
    bin_id = 1

    with open(output_bin_file, "w") as fout:
        fout.write("bin\tchr\tstart\tend\n")

        for chrom in target_chroms:
            chrom_length = chrom_lengths[chrom]

            for start in range(0, chrom_length, bin_size):
                end = min(start + bin_size - 1, chrom_length - 1)

                fout.write(f"{bin_id}\t{chrom}\t{start}\t{end}\n")
                bin_id += 1

if __name__ == "__main__":
    main()