import subprocess
import click

def aggregate_sorted_file(sorted_file, output_file):
    with open(sorted_file) as fin, open(output_file, 'w') as fout:
        fout.write("bin1\tbin2\tscore\n")

        prev_b1 = None
        prev_b2 = None
        total = 0

        for line in fin:
            line = line.strip()
            if not line:
                continue
            if line.startswith("bin1"):
                continue

            b1, b2, score = line.split()[:3]
            b1 = int(b1)
            b2 = int(b2)
            score = int(score)

            if prev_b1 is None:
                prev_b1, prev_b2, total = b1, b2, score
            elif b1 == prev_b1 and b2 == prev_b2:
                total += score
            else:
                fout.write(f"{prev_b1}\t{prev_b2}\t{total}\n")
                prev_b1, prev_b2, total = b1, b2, score
            
        if prev_b1 is not None:
            fout.write(f"{prev_b1}\t{prev_b2}\t{total}\n")

def dump_to_sort_impl(tmppairs, output, sorted, sortmemory, tmpdir):
    sort_cmd = [
        "sort",
        "-S", sortmemory,
        "-T", tmpdir,
        "-k1,1n",
        "-k2,2n",
        tmppairs,
        "-o", sorted
    ]

    subprocess.run(sort_cmd, check=True)
    aggregate_sorted_file(sorted, output)

@click.command()
@click.argument("tmppairs")
@click.argument("output")
@click.option("--sorted")
@click.option("--sortmemory", default="1G")
@click.option("--tmpdir", default="/tmp")
def dump_to_sort(tmppairs, output, sorted, sortmemory, tmpdir):
    dump_to_sort_impl(tmppairs, output, sorted, sortmemory, tmpdir)

if __name__ == "__main__":
    dump_to_sort()
