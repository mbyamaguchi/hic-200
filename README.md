# hic-200 (hic200.py)

## Usage

We use python==3.11.* for the scripts.

### Simple usage

```sh
pixi run python hic200.py \
    --tmpdir [TMPDIR] \
    [SITEPATH] [INPUTPATH] [OUTPUTPATH]
```

Example:

```sh
pixi run python hic200.py \
    --tmpdir ./tmp \
    path/to/site_file.txt path/to/fragment_pair.txt.gz path/to/output.txt
```

- tmpdir: specify the directory for temporary use.
- sitepath: restriction enzyme site file
- inputpath: count score file
- outputpath: file for output

### 1. pixi setup

Firstly, get pixi from [pixi installation](https://pixi.prefix.dev/latest/installation/) and run:

```sh
pixi install
```

to set up the environment.

### 2. make bin definition file.

```sh
pixi run python utils/make_bin_def2.py \
    --bin-size BINSIZE --chroms I,II,III \
    [site_file] [ouptut_bin_file]

```

### 3. make temp pair file.

```sh
pixi run python src/read_and_dump2.py \
    --bin BIN_FILE --max-distance 1000000 \
    [INPUT_GZ] [OUTPUT_FILE]
```

### 4. sort and make final file.

Finally, run this script to sort bins and summarise.

```sh
pixi run python src/dump_to_sort.py \
    [TMPPAIRS] [OUTPUT] \
    --sorted [SORTED] --sortmemory 1G --tmpdir /tmp
```
