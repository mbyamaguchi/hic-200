# hic-200 (hic200.py)

## Usage

### Simple usage

```sh
pixi run python hic200.py \
    --tmpdir [TMPDIR] \
    [BINPATH] [INPUTPATH] [OUTPUTPATH]
```

- tmpdir: specify the directory for temporary use.
- binpath: bin definition file
- inputpath: count score file
- outputpath: file for output

### 1. pixi setup

Firstly, get pixi and run:

```sh
pixi install
```

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
